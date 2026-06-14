"""测试法律知识库校验接口"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.chinese_law_mcp_client import (
    ChineseLawMCPClientSync,
    get_mcp_client,
    CHINESE_LAW_MCP_URL,
    CHINESE_LAW_API_KEY
)

def test_detect():
    """测试检测接口"""
    print("=" * 60)
    print("Testing Law Knowledge Base API")
    print("API URL: " + CHINESE_LAW_MCP_URL)
    print("API Key: " + CHINESE_LAW_API_KEY[:10] + "...")
    print("=" * 60)
    
    client = get_mcp_client()
    
    # Test 1: Detect law citation
    print("\n[Test 1] Detect law citation")
    test_text = "《中华人民共和国民法典》第143条"
    try:
        result = client.detect(test_text)
        print("Input: " + test_text)
        print("Result: ")
        print("  regulations count: " + str(len(result.get("regulations", []))))
        if result.get("regulations"):
            reg = result["regulations"][0]
            print("  name: " + reg.get("name", ""))
            print("  clause: " + reg.get("clause", ""))
            print("  validity_status: " + reg.get("validity_status", ""))
            print("  implement_date: " + reg.get("implement_date", ""))
            content = reg.get("think_tank_content", "")
            if content:
                print("  content (first 100 chars): " + content[:100])
        print("[OK] Detection successful")
    except Exception as e:
        print("[FAILED] Detection failed: " + str(e))
    
    # Test 2: Detect contract text
    print("\n[Test 2] Detect contract text")
    test_text = "根据《民法典》第502条规定，依法成立的合同自成立时生效。"
    try:
        result = client.detect(test_text)
        print("Input: " + test_text)
        print("Result has " + str(len(result.get("regulations", []))) + " regulations")
        print("[OK] Detection successful")
    except Exception as e:
        print("[FAILED] Detection failed: " + str(e))
    
    # Test 3: Get article content
    print("\n[Test 3] Get article content")
    try:
        article = client.get_article("民法典", "143")
        if article:
            print("Law Name: " + article.law_name)
            print("Article Number: " + article.article_num)
            print("Content (first 100 chars): " + article.content[:100])
            print("Version: " + article.version)
            print("Is Valid: " + str(article.is_valid))
            print("[OK] Get article successful")
        else:
            print("[FAILED] Get article failed: Article not found")
    except Exception as e:
        print("[FAILED] Get article failed: " + str(e))
    
    # Test 4: Validate citation
    print("\n[Test 4] Validate citation")
    try:
        result = client.validate_citation("民法典", "143", "具备下列条件的民事法律行为有效")
        print("Original Citation: " + result.original_citation)
        print("Status: " + result.status)
        print("Corrected Citation: " + result.corrected_citation)
        print("Message: " + result.message)
        print("[OK] Validation successful")
    except Exception as e:
        print("[FAILED] Validation failed: " + str(e))
    
    print("\n" + "=" * 60)
    print("All tests completed")

if __name__ == "__main__":
    test_detect()
