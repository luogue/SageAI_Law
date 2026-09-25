"""输入层：负责接收原始输入，提取关键事实"""
import re
import io
import hashlib
import zipfile
from typing import Any, Dict, Optional, Tuple
from xml.etree import ElementTree

class InputLayer:
    ALLOWED_EXTENSIONS = ('.doc', '.docx', '.txt', '.pdf')
    MIN_TEXT_LENGTH = 100
    OLE_MAGIC = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
    
    def __init__(self):
        pass
    
    def validate_file_format(self, filename: str) -> bool:
        """校验文件格式"""
        return filename.lower().endswith(self.ALLOWED_EXTENSIONS)
    
    def extract_text_from_file(self, file) -> str:
        """从文件中提取文本内容"""
        text, _ = self.extract_text_with_diagnostics(file)
        return text

    def extract_text_with_diagnostics(self, file) -> Tuple[str, Dict[str, Any]]:
        """Extract text and retain source-package lineage diagnostics.

        The diagnostics are request-local.  They make it possible to
        distinguish an extraction loss from a source file that itself only
        contains a cover sheet or structured field summary.
        """
        filename = file.filename.lower()

        if not self.validate_file_format(filename):
            raise ValueError("不支持的文件格式，请上传.docx/.txt/.pdf文件")

        try:
            file_content = file.file.read()

            if filename.endswith('.txt'):
                text = self._extract_from_txt_content(file_content)

            elif filename.endswith(('.doc', '.docx')):
                text = self._extract_from_docx_content(file_content)

            elif filename.endswith('.pdf'):
                text = self._extract_from_pdf_content(file_content)

            else:
                raise ValueError("不支持的文件格式，请上传.doc/.docx/.txt/.pdf文件")

            diagnostics = self._build_source_diagnostics(filename, file_content, text)
            return text, diagnostics

        except ValueError as e:
            raise ValueError(f"{str(e)}")
        except Exception as e:
            raise ValueError(f"文件格式损坏，无法读取：{str(e)}")

    def _build_source_diagnostics(
        self,
        filename: str,
        file_content: bytes,
        extracted_text: str,
    ) -> Dict[str, Any]:
        source_visible_text = extracted_text or ""
        source_parts: Dict[str, int] = {}
        package_diagnostics: Dict[str, Any] = {}
        if filename.endswith(('.doc', '.docx')) and zipfile.is_zipfile(io.BytesIO(file_content)):
            source_visible_text, source_parts = self._extract_ooxml_visible_text(file_content)
            with zipfile.ZipFile(io.BytesIO(file_content)) as package:
                package_names = package.namelist()
                document_xml = package.read("word/document.xml") if "word/document.xml" in package_names else b""
                package_diagnostics = {
                    "word_xml_part_count": sum(
                        name.startswith("word/") and name.endswith(".xml")
                        for name in package_names
                    ),
                    "media_part_count": sum(name.startswith("word/media/") for name in package_names),
                    "embedding_part_count": sum(name.startswith("word/embeddings/") for name in package_names),
                    "alt_chunk_count": len(re.findall(rb"<w:altChunk\b", document_xml)),
                }

        shape = self._document_shape(source_visible_text or extracted_text)
        if (
            shape["status"] == "INCOMPLETE_INPUT"
            and (
                int(package_diagnostics.get("embedding_part_count") or 0) > 0
                or int(package_diagnostics.get("alt_chunk_count") or 0) > 0
                or int(package_diagnostics.get("media_part_count") or 0) >= 2
            )
        ):
            shape = {
                **shape,
                "status": "EXTRACTION_SUSPECTED",
                "reason": "UNEXTRACTED_DOCUMENT_CONTENT",
                "message": "源文件包含嵌入对象、替代正文或多页图像，但当前可提取文本仅呈现字段摘要；疑似需要继续解析或OCR。",
            }
        return {
            "filename": filename,
            "format": filename.rsplit('.', 1)[-1] if '.' in filename else "",
            "file_byte_length": len(file_content),
            "file_sha256": hashlib.sha256(file_content).hexdigest(),
            "source_text_character_count": len(source_visible_text),
            "extracted_text_character_count": len(extracted_text or ""),
            "source_part_character_counts": source_parts,
            "source_package": package_diagnostics,
            "completeness": shape,
            # Private comparison material.  The public integrity builder removes
            # this field after calculating hashes, previews and anchor parity.
            "source_visible_text": source_visible_text,
        }

    def _extract_ooxml_visible_text(self, content: bytes) -> Tuple[str, Dict[str, int]]:
        namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        texts = []
        part_counts: Dict[str, int] = {}
        with zipfile.ZipFile(io.BytesIO(content)) as package:
            names = [
                name for name in package.namelist()
                if re.fullmatch(
                    r"word/(?:document|header\d+|footer\d+|footnotes|endnotes)\.xml",
                    name,
                )
            ]
            for name in names:
                try:
                    root = ElementTree.fromstring(package.read(name))
                except ElementTree.ParseError:
                    continue
                parent_map = {
                    child: parent
                    for parent in root.iter()
                    for child in parent
                }
                paragraphs = []
                for paragraph in root.iter(f"{namespace}p"):
                    values = []
                    for node in paragraph.iter(f"{namespace}t"):
                        # Text boxes contain nested w:p nodes.  Attribute each
                        # text node to its nearest paragraph so the outer
                        # drawing paragraph cannot duplicate the text-box body.
                        ancestor = parent_map.get(node)
                        nested_in_other_paragraph = False
                        while ancestor is not None and ancestor is not paragraph:
                            if ancestor.tag == f"{namespace}p":
                                nested_in_other_paragraph = True
                                break
                            ancestor = parent_map.get(ancestor)
                        if not nested_in_other_paragraph:
                            values.append(node.text or "")
                    value = "".join(values).strip()
                    if value:
                        if not paragraphs or paragraphs[-1] != value:
                            paragraphs.append(value)
                part_text = "\n".join(paragraphs)
                if part_text:
                    texts.append(part_text)
                    part_counts[name] = len(part_text)
        return "\n".join(texts), part_counts

    def _document_shape(self, text: str) -> Dict[str, Any]:
        lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
        heading_pattern = re.compile(
            r"^(?:第[一二三四五六七八九十百零〇\d]+条|"
            r"[一二三四五六七八九十百零〇]+、|"
            r"\d+(?:\.\d+)*(?:[\.．、]|\s+[一-龥A-Za-z]))"
        )
        formal_heading_flags = [bool(heading_pattern.match(line)) for line in lines]
        formal_heading_count = sum(formal_heading_flags)
        field_label_count = sum(bool(re.match(r"^[^。；;]{1,30}[：:]\s*.{0,100}$", line)) for line in lines)
        sentence_like_count = sum(
            len(line) >= 20 and bool(re.search(r"[。；;！？!?]", line))
            for line in lines
        )
        long_narrative_count = sum(len(line) >= 60 for line in lines)
        obligation_pattern = re.compile(
            r"应当|应在|应于|应向|应由|应负责|必须|有权|无权|不得|负责|保证|承担|"
            r"支付|交付|提供|通知|赔偿|履行|终止|解除|生效"
        )
        substantive_paragraph_flags = [
            len(line) >= 20
            and (
                bool(re.search(r"[。；;！？!?]", line))
                or bool(obligation_pattern.search(line))
            )
            for line in lines
        ]
        substantive_paragraph_count = sum(substantive_paragraph_flags)
        max_consecutive_substantive_paragraphs = 0
        current_run = 0
        for is_substantive in substantive_paragraph_flags:
            current_run = current_run + 1 if is_substantive else 0
            max_consecutive_substantive_paragraphs = max(
                max_consecutive_substantive_paragraphs,
                current_run,
            )

        structure_categories = {
            "definitions_or_subject": r"定义|术语|合同标的|项目内容|服务内容|工作内容|许可范围|实施范围",
            "rights_and_obligations": r"权利义务|应当|应在|应于|有权|不得|负责|保证|承担",
            "payment_or_settlement": r"价款|费用|报酬|支付|付款|结算|提成|租金",
            "delivery_or_acceptance": r"交付|验收|质量|技术资料|成果",
            "liability_or_infringement": r"违约|赔偿|责任|侵权",
            "term_or_termination": r"期限|有效期|终止|解除|生效",
            "dispute_resolution": r"争议|仲裁|诉讼|法院|管辖",
            "force_majeure_or_confidentiality": r"不可抗力|保密|商业秘密|技术秘密",
        }
        compact_text = "\n".join(lines)
        structure_category_hits = {
            category: bool(re.search(pattern, compact_text))
            for category, pattern in structure_categories.items()
        }
        structure_category_count = sum(structure_category_hits.values())
        field_ratio = round(field_label_count / len(lines), 4) if lines else 0.0

        # A complete structured contract may be concise and may begin with many
        # fill-in fields.  Positive contract-body structure therefore overrides
        # the field-density heuristic.  Conversely, a long list of populated
        # fields is not treated as a body merely because its values are verbose.
        has_continuous_contract_body = bool(
            (formal_heading_count >= 3 and substantive_paragraph_count >= 3)
            or (
                substantive_paragraph_count >= 5
                and max_consecutive_substantive_paragraphs >= 3
                and structure_category_count >= 3
            )
            or (
                sentence_like_count >= 6
                and structure_category_count >= 4
            )
        )
        field_only = bool(
            len(lines) >= 8
            and formal_heading_count == 0
            and field_label_count >= 8
            and field_ratio >= 0.2
            and substantive_paragraph_count <= 2
            and structure_category_count <= 2
            and not has_continuous_contract_body
        ) or bool(
            len(lines) >= 12
            and formal_heading_count <= 1
            and field_label_count >= 10
            and field_ratio >= 0.35
            and substantive_paragraph_count <= 3
            and structure_category_count <= 2
            and not has_continuous_contract_body
        )
        return {
            "status": "INCOMPLETE_INPUT" if field_only else "PASS",
            "reason": "FIELD_ONLY_EXCERPT" if field_only else "",
            "message": (
                "上传文件仅检测到封面/填空字段，未检测到可审查的连续合同条款；请重新上传包含完整正文和附件的原文件。"
                if field_only else "源文档包含可进入审查链路的正文结构。"
            ),
            "character_count": len(text or ""),
            "nonempty_line_count": len(lines),
            "formal_heading_count": formal_heading_count,
            "field_label_count": field_label_count,
            "field_label_ratio": field_ratio,
            "sentence_like_count": sentence_like_count,
            "long_narrative_count": long_narrative_count,
            "substantive_paragraph_count": substantive_paragraph_count,
            "max_consecutive_substantive_paragraphs": max_consecutive_substantive_paragraphs,
            "structure_category_count": structure_category_count,
            "structure_category_hits": structure_category_hits,
            "has_continuous_contract_body": has_continuous_contract_body,
        }

    def _extract_from_txt_content(self, content: bytes) -> str:
        """从TXT文件内容提取文本"""
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                text = content.decode('gbk', errors='replace')  # 添加 errors='replace' 处理不支持的字符
            except UnicodeDecodeError:
                text = content.decode('gb2312', errors='replace')
        return self._normalize_extracted_text(text)

    def _normalize_extracted_text(self, text: str) -> str:
        """Normalize markup artifacts introduced by fixture conversion."""
        return (text or "").replace("**", "")

    def _extract_from_docx_content(self, content: bytes) -> str:
        """从DOCX文件内容提取文本"""
        if content.startswith(self.OLE_MAGIC):
            return self._extract_from_ole_word_content(content)
        if not zipfile.is_zipfile(io.BytesIO(content)):
            raise ValueError("DOCX文件解析失败：文件不是标准Word文档。请确认文件未损坏，或将老版.doc文件另存为.docx后再上传")
        try:
            from docx import Document
            from docx.table import Table
            from docx.text.paragraph import Paragraph
            document = Document(io.BytesIO(content))
            blocks = []
            for child in document.element.body.iterchildren():
                if child.tag.endswith("}p"):
                    value = Paragraph(child, document).text.strip()
                    if value:
                        blocks.append(value)
                elif child.tag.endswith("}tbl"):
                    table = Table(child, document)
                    for row in table.rows:
                        cells = [re.sub(r"\s+", " ", cell.text).strip() for cell in row.cells]
                        if any(cells):
                            blocks.append(" | ".join(cells))
            text = '\n'.join(blocks)
            ooxml_text, _ = self._extract_ooxml_visible_text(content)
            python_compact_length = len("".join(text.split()))
            ooxml_compact_length = len("".join(ooxml_text.split()))
            if (
                ooxml_compact_length >= python_compact_length + 80
                and ooxml_compact_length >= int(max(1, python_compact_length) * 1.05)
            ):
                # python-docx does not expose every Word text carrier (notably
                # drawing text boxes and some header/footer structures).  Use
                # the source-package stream when it demonstrably recovers more
                # visible text; no vocabulary-dependent rule is involved.
                text = ooxml_text
            if not text.strip():
                raise ValueError("文件内容为空")
            return self._normalize_extracted_text(text)
        except ImportError:
            raise ValueError("缺少python-docx依赖，请安装：pip install python-docx")
        except Exception as e:
            raise ValueError(f"DOCX文件解析失败：{str(e)}")

    def _extract_from_ole_word_content(self, content: bytes) -> str:
        """Best-effort extraction for legacy .doc files renamed as .docx."""
        candidates = []
        for encoding in ("utf-16le", "gb18030"):
            decoded = content.decode(encoding, errors="ignore")
            chunks = re.findall(
                r"[\u4e00-\u9fffA-Za-z0-9，。；：、（）()《》“”‘’【】\[\]！？,.!?;:/\\\-—_#*☑□ \t\r\n]{8,}",
                decoded,
            )
            cleaned_chunks = []
            for chunk in chunks:
                line = re.sub(r"[ \t\r\n]+", " ", chunk).strip()
                line = line.replace("**", "")
                if not line:
                    continue
                chinese_count = len(re.findall(r"[\u4e00-\u9fff]", line))
                if chinese_count >= 4 or ("合同" in line and len(line) >= 8):
                    cleaned_chunks.append(line)
            text = "\n".join(dict.fromkeys(cleaned_chunks))
            if len(text) > len("\n".join(candidates)):
                candidates = cleaned_chunks

        extracted = "\n".join(dict.fromkeys(candidates)).strip()
        if len(extracted) < self.MIN_TEXT_LENGTH:
            raise ValueError(
                "检测到老版Word .doc/OLE文件，但当前环境无法完整解析。请用Word打开后另存为标准.docx再上传"
            )
        return self._normalize_extracted_text(extracted)

    def _extract_from_pdf_content(self, content: bytes) -> str:
        """从PDF文件内容提取文本"""
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(content))

            if reader.is_encrypted:
                raise ValueError("PDF文件已加密，无法读取")

            text = ''
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'

            if not text.strip():
                raise ValueError("PDF文件内容为空或无法提取文本")
            return self._normalize_extracted_text(text)
        except ImportError:
            raise ValueError("缺少pypdf依赖，请安装：pip install pypdf")
        except Exception as e:
            raise ValueError(f"PDF文件解析失败：{str(e)}")
    
    def validate_content(self, text: str) -> bool:
        """校验内容非空"""
        if not text or len(text.strip()) < self.MIN_TEXT_LENGTH:
            return False
        return True
    
    def extract_key_facts(self, contract_text: str) -> Dict:
        """从合同文本中提取关键事实"""
        facts = {
            "basic_info": self._extract_basic_info(contract_text),
            "key_clauses": self._extract_key_clauses(contract_text),
            "dispute_focus": self._extract_dispute_focus(contract_text)
        }
        return facts
    
    def _extract_basic_info(self, text: str) -> Dict:
        """提取基本案情信息"""
        info = {
            "contract_type": self._extract_contract_type(text),
            "parties": self._extract_parties(text),
            "subject_matter": self._extract_subject_matter(text),
            "amount": self._extract_amount(text),
            "sign_date": self._extract_sign_date(text),
            "validity_period": self._extract_validity_period(text)
        }
        return info
    
    def _extract_contract_type(self, text: str) -> str:
        """提取合同类型"""
        patterns = [
            r'(买卖合同|租赁合同|服务合同|借款合同|劳动合同|合作协议|保密协议)',
            r'合同名称[：:]?\s*([^\n]+)',
            r'鉴于[^\n]*([^\n]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return "未明确"
    
    def _extract_parties(self, text: str) -> str:
        """提取双方当事人"""
        patterns = [
            r'(甲方|甲方：|甲方名称)[：:]?\s*([^\n]+)',
            r'(乙方|乙方：|乙方名称)[：:]?\s*([^\n]+)',
            r'(出卖人|买受人|出租人|承租人|债权人|债务人)[：:]?\s*([^\n]+)'
        ]
        parties = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                parties.append(f"{match[0]}: {match[1].strip()}")
        return "; ".join(parties) if parties else "未明确"
    
    def _extract_subject_matter(self, text: str) -> str:
        """提取合同标的"""
        patterns = [
            r'标的[：:]?\s*([^\n]+)',
            r'合同标的[：:]?\s*([^\n]+)',
            r'标的物[：:]?\s*([^\n]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return "未明确"
    
    def _extract_amount(self, text: str) -> str:
        """提取合同金额"""
        patterns = [
            r'(?:人民币|￥|¥)\s*([\d,.]+)',
            r'金额[：:]?\s*(人民币)?\s*([\d,.]+)',
            r'价款[：:]?\s*(人民币)?\s*([\d,.]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1) if match.group(1) else match.group(2)
        return "未明确"
    
    def _extract_sign_date(self, text: str) -> str:
        """提取签订日期"""
        pattern = r'(签订日期|签署日期|合同日期)[：:]?\s*(\d{4}[\-/年]\d{1,2}[\-/月]\d{1,2}[日号]?)'
        match = re.search(pattern, text)
        if match:
            return match.group(2).strip()
        return "未明确"
    
    def _extract_validity_period(self, text: str) -> str:
        """提取有效期"""
        patterns = [
            r'有效期[：:]?\s*([^\n]+)',
            r'期限[：:]?\s*([^\n]+)',
            r'自(\d{4}[\-/年]\d{1,2}[\-/月]\d{1,2})至(\d{4}[\-/年]\d{1,2}[\-/月]\d{1,2})'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return "未明确"
    
    def _extract_key_clauses(self, text: str) -> Dict:
        """提取主要条款"""
        clauses = {
            "payment_terms": self._extract_payment_terms(text),
            "liability": self._extract_liability(text),
            "termination": self._extract_termination(text),
            "confidentiality": self._extract_confidentiality(text),
            "dispute_resolution": self._extract_dispute_resolution(text)
        }
        return clauses
    
    def _extract_payment_terms(self, text: str) -> str:
        """提取付款条款"""
        pattern = r'(付款方式|付款时间|结算方式)[：:]?\s*([^\n]+)'
        match = re.search(pattern, text)
        if match:
            return match.group(2).strip()
        return "未明确"
    
    def _extract_liability(self, text: str) -> str:
        """提取违约责任"""
        pattern = r'(违约责任|违约条款)[：:]?\s*([^\n]+)'
        match = re.search(pattern, text)
        if match:
            return match.group(2).strip()
        return "未明确"
    
    def _extract_termination(self, text: str) -> str:
        """提取终止条款"""
        pattern = r'(合同解除|终止条款|解除条件)[：:]?\s*([^\n]+)'
        match = re.search(pattern, text)
        if match:
            return match.group(2).strip()
        return "未明确"
    
    def _extract_confidentiality(self, text: str) -> str:
        """提取保密条款"""
        pattern = r'(保密条款|保密义务)[：:]?\s*([^\n]+)'
        match = re.search(pattern, text)
        if match:
            return match.group(2).strip()
        return "未明确"
    
    def _extract_dispute_resolution(self, text: str) -> str:
        """提取争议解决"""
        pattern = r'(争议解决|管辖法院|仲裁)[：:]?\s*([^\n]+)'
        match = re.search(pattern, text)
        if match:
            return match.group(2).strip()
        return "未明确"
    
    def _extract_dispute_focus(self, text: str) -> str:
        """提取争议焦点"""
        patterns = [
            r'(争议焦点|争议事项)[：:]?\s*([^\n]+)',
            r'(双方争议|主要分歧)[：:]?\s*([^\n]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(2).strip()
        return "未明确"
    
    def process(self, file, additional_instructions: Optional[str] = "") -> Dict:
        """处理输入，返回结构化JSON数据"""
        try:
            # 提取文本（已包含文件格式校验和编码异常捕获）
            contract_text = self.extract_text_from_file(file)
            
            # 内容非空校验
            if not self.validate_content(contract_text):
                return {
                    "status": "error",
                    "message": "合同内容过短，请确认文件是否正确"
                }
            
            # 提取关键事实
            facts = self.extract_key_facts(contract_text)
            
            # 构建结构化输出
            result = {
                "contract_text": contract_text,
                "facts": facts,
                "user_instructions": additional_instructions or "无",
                "status": "success"
            }
            
            return result
            
        except ValueError as e:
            # 已知的校验错误
            return {
                "status": "error",
                "message": str(e)
            }
        except Exception as e:
            # 未知错误
            return {
                "status": "error",
                "message": f"文件处理失败：{str(e)}"
            }
