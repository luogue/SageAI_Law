import asyncio
import io
import zipfile
from pathlib import Path

import pytest
from docx import Document
from fastapi import HTTPException

from layers.input_layer import InputLayer
from review_v2.clause_parser import parse_contract_clauses, strip_non_contract_tail
from review_v2.input_integrity import build_input_integrity_diagnostics
from review_v2.technology_service_analysis import classify_technology_transaction
from routers.review_v2 import review_v2_file


ROOT = Path(__file__).resolve().parents[2]
# Keep the original field-only upload at the workspace root.  The test_data
# copy now contains the complete contract used by the end-to-end regression.
FIELD_ONLY_FIXTURE = ROOT / "37 专利技术许可合同.docx"


FULL_PATENT_LICENSE = """涉外专利实施许可合同
许可方：Meyer Industrial Technologies GmbH
接受方：中国华科智能装备有限公司

第一条 专利技术
许可方确认其为专利号ZL201910876543.2的合法专利权人，许可标的是工业机器人高精度视觉定位与自适应控制专利技术。

第二条 许可性质和实施范围
许可方授予接受方在中华人民共和国境内非独占、不可转让的专利实施许可。接受方有权使用该专利技术制造、使用和销售合同产品，但无权转让专利权或向第三方再许可。

第三条 许可使用费
接受方按照合同产品年度净销售额乘以5%的提成率向许可方支付提成费，净销售额按照销售收入扣除税费和退货后计算。

第四条 支付机制
接受方应在每个会计年度结束后十个工作日内提交销售报表和提成费计算表，并在收到合法发票后三十日内支付许可使用费。许可方可以委托独立审计机构核验净销售额。

第五条 专利资料交付和后续改进
许可方应在合同生效后十五日内交付专利资料、设计图纸、控制参数、测试数据和操作手册，并提供技术指导。双方对后续改进应相互书面通知，改进成果归改进方所有，另一方需要使用的应另行协商许可条件。

第六条 权利保证、专利维持和侵权责任
许可方保证有权授予本合同项下许可，保证专利在签约时合法有效且不存在未披露的权利负担。许可方应按时缴纳专利费用和专利年费并维持专利有效性。接受方按约实施专利遭遇第三方侵权主张时，许可方应负责应诉、排除妨碍并承担相应侵权责任和合理费用。

第七条 保密及出口合规
双方对履约中知悉的技术秘密承担保密义务；跨境交付专利资料时应依法办理技术进出口审批、登记或备案。

第八条 不可抗力
不可抗力包括战争、严重洪水、火灾、台风、地震及其他不能预见、不能避免且不能克服的事件。受影响方应及时通知对方，并在十四日内提供有效证明。不可抗力持续影响超过120天的，双方应协商继续履行、变更或者终止合同。

第九条 争议解决
因本合同产生的争议应先协商解决；协商不成的，提交中国国际经济贸易仲裁委员会仲裁，适用申请仲裁时有效的仲裁规则，仲裁裁决为终局。

第十条 专利失效和终止后处理
专利失效后，许可方应立即书面通知接受方，双方按照失效原因和时间停止或调整后续许可使用费。
10.4 专利失效后的继续使用和费用处理：接受方可以继续使用已经进入公有领域的技术；失效日后不再支付提成费，许可方应返还失效后已收取的费用。
"""


STRUCTURED_SHORT_CONTRACT = """合同编号：TEST-2026-001
签订地点：上海
甲方：某技术公司
乙方：某制造公司
联系人：张三
联系电话：021-00000000
项目名称：控制系统使用项目
币种：人民币
付款方式：银行转账
有效期限：三年
1. 合同标的
甲方应向乙方提供控制系统及配套文件，乙方有权依约在约定场所使用。
2. 双方权利义务
甲方应保证交付内容可以正常运行，乙方不得超出合同范围使用。
3. 费用与支付
乙方应在合同生效后十日内支付首期费用，余款在验收后结算。
4. 交付与验收
甲方应交付操作手册和测试资料，乙方应在收到后十五日内完成验收。
5. 违约责任
任何一方违反本合同造成对方损失的，应承担相应违约责任。
6. 保密
双方对履约中知悉的商业秘密承担保密义务，未经同意不得披露。
7. 争议解决
协商不成的，任何一方可以向有管辖权的人民法院提起诉讼。
8. 生效与终止
本合同经双方签字盖章后生效，期限届满或者依法解除时终止。
"""


class _Upload:
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self.file = io.BytesIO(content)


def _docx_bytes(text: str) -> bytes:
    document = Document()
    for line in text.splitlines():
        document.add_paragraph(line)
    output = io.BytesIO()
    document.save(output)
    return output.getvalue()


def _docx_with_textbox_payload(text: str) -> bytes:
    """Put substantive text in a Word text box, which python-docx omits."""

    base = _docx_bytes("合同编号：TEXTBOX-001\n甲方：某公司\n乙方：某公司")
    source = io.BytesIO(base)
    target = io.BytesIO()
    with zipfile.ZipFile(source) as original, zipfile.ZipFile(target, "w") as rewritten:
        for info in original.infolist():
            payload = original.read(info.filename)
            if info.filename == "word/document.xml":
                textbox = (
                    '<w:p><w:r><w:pict><v:shape xmlns:v="urn:schemas-microsoft-com:vml">'
                    '<v:textbox><w:txbxContent><w:p><w:r><w:t xml:space="preserve">'
                    + text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    + '</w:t></w:r></w:p></w:txbxContent></v:textbox></v:shape></w:pict></w:r></w:p>'
                ).encode("utf-8")
                payload = payload.replace(b"</w:body>", textbox + b"</w:body>")
            rewritten.writestr(info, payload)
    return target.getvalue()


def _review_bytes(content: bytes, filename: str = "patent-license.docx") -> dict:
    return asyncio.run(review_v2_file(
        file=_Upload(filename, content),
        contract_type="sale",
        include_low_risk=True,
        use_llm=False,
        profile_json='{"user_identity":"接受方"}',
        current_user={"id": "input-integrity-test"},
    ))


def test_current_uploaded_fixture_is_field_page_and_is_blocked_before_review():
    upload = _Upload(FIELD_ONLY_FIXTURE.name, FIELD_ONLY_FIXTURE.read_bytes())
    text, source = InputLayer().extract_text_with_diagnostics(upload)

    assert len(text) == 740
    assert source["source_text_character_count"] == 740
    assert source["completeness"]["status"] == "INCOMPLETE_INPUT"
    assert source["completeness"]["reason"] == "FIELD_ONLY_EXCERPT"
    assert source["completeness"]["formal_heading_count"] == 0
    assert source["completeness"]["field_label_count"] >= 20

    with pytest.raises(HTTPException) as raised:
        _review_bytes(FIELD_ONLY_FIXTURE.read_bytes(), FIELD_ONLY_FIXTURE.name)
    assert raised.value.status_code == 422
    assert raised.value.detail["code"] == "CONTRACT_INPUT_INTEGRITY_FAILED"
    assert raised.value.detail["input_integrity"]["status"] == "BLOCKED"


def test_anchor_loss_between_raw_classifier_or_rule_input_blocks_pipeline():
    normalized = strip_non_contract_tail(FULL_PATENT_LICENSE)
    classifier_input = normalized.replace("中国国际经济贸易仲裁委员会", "")
    rule_input = normalized.replace("不可抗力", "")

    diagnostics = build_input_integrity_diagnostics(
        extracted_text=FULL_PATENT_LICENSE,
        normalized_text=normalized,
        classifier_input=classifier_input,
        rule_engine_input=rule_input,
    )

    assert diagnostics["status"] == "BLOCKED"
    assert any(
        row["code"] == "CLASSIFIER_INPUT_ANCHOR_LOSS"
        and row["anchor"] == "中国国际经济贸易仲裁委员会"
        for row in diagnostics["failures"]
    )
    assert any(
        row["code"] == "RULE_ENGINE_INPUT_ANCHOR_LOSS"
        and row["anchor"] == "不可抗力"
        for row in diagnostics["failures"]
    )


def test_diagnostics_cover_every_consumer_and_detect_non_anchor_replacement():
    normalized = strip_non_contract_tail(STRUCTURED_SHORT_CONTRACT)
    summary = "合同编号：TEST-2026-001\n甲方：某技术公司\n乙方：某制造公司"
    diagnostics = build_input_integrity_diagnostics(
        extracted_text=STRUCTURED_SHORT_CONTRACT,
        normalized_text=normalized,
        classifier_input=summary,
        clause_extraction_input=normalized,
        rule_engine_input=normalized,
        search_audit_input=summary,
    )

    assert diagnostics["status"] == "BLOCKED"
    assert any(
        row["code"] == "CLASSIFIER_INPUT_TEXT_MISMATCH"
        for row in diagnostics["failures"]
    )
    assert any(
        row["code"] == "SEARCH_AUDIT_INPUT_TEXT_MISMATCH"
        for row in diagnostics["failures"]
    )
    assert set(diagnostics["stages"]) >= {
        "source_document",
        "extracted_full_text",
        "normalized_full_text",
        "classifier_input",
        "clause_extraction_input",
        "rule_engine_input",
        "search_audit_input",
    }
    assert diagnostics["stages"]["normalized_full_text"]["nonempty_paragraph_count"] >= 10


def test_generic_retention_checks_identify_extraction_and_normalization_loss():
    full_text = (STRUCTURED_SHORT_CONTRACT + "\n") * 4
    extraction_loss = build_input_integrity_diagnostics(
        extracted_text=full_text[:350],
        normalized_text=full_text[:350],
        classifier_input=full_text[:350],
        rule_engine_input=full_text[:350],
        source_diagnostics={
            "source_visible_text": full_text,
            "completeness": {"status": "PASS"},
        },
    )
    assert any(
        row["code"] == "DOCUMENT_EXTRACTION_TEXT_LOSS"
        for row in extraction_loss["failures"]
    )

    normalized_excerpt = full_text[:500]
    normalization_loss = build_input_integrity_diagnostics(
        extracted_text=full_text,
        normalized_text=normalized_excerpt,
        classifier_input=normalized_excerpt,
        rule_engine_input=normalized_excerpt,
        source_diagnostics={
            "source_visible_text": full_text,
            "completeness": {"status": "PASS"},
        },
    )
    assert any(
        row["code"] == "NORMALIZATION_TEXT_LOSS"
        for row in normalization_loss["failures"]
    )


def test_structured_short_contract_with_many_fields_is_not_a_field_summary():
    upload = _Upload("structured-short.docx", _docx_bytes(STRUCTURED_SHORT_CONTRACT))
    text, source = InputLayer().extract_text_with_diagnostics(upload)
    shape = source["completeness"]

    assert len(text) < 2000
    assert shape["field_label_count"] >= 8
    assert shape["formal_heading_count"] >= 8
    assert shape["structure_category_count"] >= 6
    assert shape["has_continuous_contract_body"] is True
    assert shape["status"] == "PASS"


def test_ooxml_textbox_body_is_recovered_before_completeness_check():
    payload = STRUCTURED_SHORT_CONTRACT + "\n" + FULL_PATENT_LICENSE
    upload = _Upload("textbox-contract.docx", _docx_with_textbox_payload(payload))
    text, source = InputLayer().extract_text_with_diagnostics(upload)

    assert "中国国际经济贸易仲裁委员会" in text
    assert "不可抗力持续影响超过120天" in text
    assert source["source_text_character_count"] == len(text)
    assert source["completeness"]["status"] == "PASS"


def test_complete_patent_license_uses_one_full_text_and_never_loads_sale_rules():
    output = _review_bytes(_docx_bytes(FULL_PATENT_LICENSE))
    classification = output["deterministic_analysis"]["technology_classification"]
    review_ids = [row["item_id"] for row in output["items"]]
    integrity = output["input_integrity"]

    assert output["success"] is True
    assert output["contract_type"] == "technology"
    assert output["selected_contract_type"] == "sale"
    assert output["report_context"]["contract_type_label"] == "技术合同—技术许可合同—专利实施许可"
    assert classification["primary_subtype"] == "TECHNOLOGY_LICENSE"
    assert classification["tertiary_subtype"] == "PATENT_LICENSE"
    assert classification["primary_contract_type"] == "technology_license_patent"
    assert classification["primary_transaction_model"]["type"] == "TECHNOLOGY_LICENSE"
    assert classification["primary_transaction_model"]["sale_semantics"]["independent_economic_value"] is False
    assert not any(review_id.startswith("S-") for review_id in review_ids)

    assert integrity["status"] == "PASS"
    assert integrity["lineage"]["single_full_text_source"] is True
    assert integrity["stages"]["classifier_input"]["used_by_stage"] is True
    assert integrity["stages"]["clause_extraction_input"]["used_by_stage"] is True
    assert integrity["stages"]["rule_engine_input"]["used_by_stage"] is True
    assert integrity["stages"]["search_audit_input"]["used_by_stage"] is True
    assert integrity["stages"]["clause_extraction_output"]["used_by_stage"] is True
    assert all(
        row["classifier_input"]
        and row["clause_extraction_input"]
        and row["rule_engine_input"]
        and row["search_audit_input"]
        for row in integrity["anchor_matrix"].values()
    )

    parsed_text = "\n".join(clause.text for clause in parse_contract_clauses(FULL_PATENT_LICENSE))
    assert "中国国际经济贸易仲裁委员会" in parsed_text
    assert "不可抗力持续影响超过120天" in parsed_text

    all_evidence = "\n".join(
        evidence.get("text", "")
        for row in output["items"]
        for evidence in row.get("evidence_clauses") or []
    )
    for expected in (
        "净销售额乘以5%的提成率",
        "专利资料、设计图纸",
        "按时缴纳专利费用和专利年费",
        "第三方侵权主张",
        "专利失效后的继续使用和费用处理",
    ):
        assert expected in all_evidence
    assert "提成费开始计算时间：" not in all_evidence

    license_facts = output["deterministic_analysis"]["patent_license_consistency"]
    assert license_facts["license_type"] == "NON_EXCLUSIVE"
    assert license_facts["patent_invalidity_occurs"] is True
    assert license_facts["continued_use_after_patent_invalidity"] is True
    assert license_facts["royalty_stops_after_patent_invalidity"] is True
    assert license_facts["paid_fee_refunded_after_patent_invalidity"] is True
    assert license_facts["patent_invalidity_fee_conflict"] is False


def test_acceptance_party_is_a_licensee_role_not_a_sale_role():
    classification = classify_technology_transaction(FULL_PATENT_LICENSE)
    model = classification["primary_transaction_model"]

    assert model["license_semantics"]["roles"] is True
    assert model["sale_semantics"]["roles"] is False
    assert model["type"] == "TECHNOLOGY_LICENSE"
    assert classification["tertiary_subtype"] == "PATENT_LICENSE"
