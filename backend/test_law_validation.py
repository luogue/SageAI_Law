"""从测试文件中提取法条并调用接口校验"""
import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.chinese_law_mcp_client import get_mcp_client

# 法条引用正则表达式
LEGAL_CITATION_PATTERN = re.compile(
    r'《([^》]+)》\s*第\s*(\d+)\s*条(?:\s*第\s*(\d+)\s*款)?'
)

def extract_citations_from_file(filepath):
    """从文件中提取所有法条引用"""
    citations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = LEGAL_CITATION_PATTERN.findall(content)
            for match in matches:
                law_name = match[0]
                article_num = match[1]
                paragraph_num = match[2] if match[2] else ""
                citations.append({
                    'law_name': law_name,
                    'article_num': article_num,
                    'paragraph_num': paragraph_num,
                    'full_text': f"《{law_name}》第{article_num}条{('第' + paragraph_num + '款') if paragraph_num else ''}"
                })
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return citations

def validate_all_citations(citations):
    """批量校验法条引用"""
    client = get_mcp_client()
    results = []
    
    print("=" * 80)
    print("Starting law citation validation...")
    print(f"Total citations to validate: {len(citations)}")
    print("=" * 80)
    
    for idx, citation in enumerate(citations, 1):
        print(f"\n[{idx}/{len(citations)}] Validating: {citation['full_text']}")
        
        try:
            result = client.validate_citation(
                citation['law_name'],
                citation['article_num'],
                content=""
            )
            
            print(f"  Status: {result.status}")
            print(f"  Message: {result.message}")
            
            if result.law_article:
                print(f"  Law Name: {result.law_article.law_name}")
                print(f"  Article: {result.law_article.article_num}")
                print(f"  Is Valid: {result.law_article.is_valid}")
                print(f"  Version: {result.law_article.version}")
                if result.law_article.content:
                    content_preview = result.law_article.content[:100] + "..." if len(result.law_article.content) > 100 else result.law_article.content
                    print(f"  Content: {content_preview}")
            
            results.append({
                'citation': citation,
                'validation': result,
                'success': result.status in ['ok', 'corrected', 'replaced']
            })
            
        except Exception as e:
            print(f"  [ERROR] Validation failed: {e}")
            results.append({
                'citation': citation,
                'validation': None,
                'success': False,
                'error': str(e)
            })
    
    return results

def main():
    # 测试文件路径
    test_files = [
        r"f:\ai\Sage\测试文件\同一房屋买卖合同签订三份“阴阳合同”，法院如何认定效力？_审查结果.txt",
        r"f:\ai\Sage\测试文件\退休人员返聘协议（模板）.docx_review.txt",
        r"f:\ai\Sage\测试文件\指导案例171号：中天建设集团有限公司诉河南恒和置业有限公司建设工程施工合同纠纷案_审查结果.txt"
    ]
    
    # 提取所有法条引用
    all_citations = []
    for filepath in test_files:
        if os.path.exists(filepath):
            print(f"Extracting citations from: {os.path.basename(filepath)}")
            citations = extract_citations_from_file(filepath)
            all_citations.extend(citations)
            print(f"  Found {len(citations)} citations")
        else:
            print(f"File not found: {filepath}")
    
    # 去重
    unique_citations = []
    seen = set()
    for cite in all_citations:
        key = (cite['law_name'], cite['article_num'], cite['paragraph_num'])
        if key not in seen:
            seen.add(key)
            unique_citations.append(cite)
    
    print(f"\nTotal unique citations: {len(unique_citations)}")
    
    # 校验所有法条
    results = validate_all_citations(unique_citations)
    
    # 输出汇总报告
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY REPORT")
    print("=" * 80)
    
    success_count = sum(1 for r in results if r['success'])
    fail_count = len(results) - success_count
    
    print(f"\nTotal Citations: {len(results)}")
    print(f"Validated Successfully: {success_count}")
    print(f"Validation Failed: {fail_count}")
    
    print("\n--- Detailed Results ---")
    for result in results:
        cite = result['citation']
        status = "✓" if result['success'] else "✗"
        validation = result['validation']
        
        if validation:
            print(f"{status} {cite['full_text']} - {validation.status}: {validation.message}")
        else:
            print(f"{status} {cite['full_text']} - ERROR: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
