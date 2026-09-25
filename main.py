from sage_engine import SageEngine

def main():
    """
    主函数
    """
    # 初始化Sage引擎
    sage = SageEngine()
    
    print("=== Sage AI Agent ===")
    print("基于 DeepSeek 云端模型的逻辑推理系统")
    print("核心流程: 输入问题→抽象本质→抓主要矛盾→逻辑推导→输出结论")
    print("封装方法: abstract、main_contradiction、boundary、verify")
    print("实践循环: 理论→验证→反馈→迭代")
    print("=====================")
    
    while True:
        # 获取用户输入
        problem = input("\n请输入问题 (输入 'exit' 退出): ")
        
        if problem.lower() == 'exit':
            print("退出Sage AI Agent")
            break
        
        # 处理问题
        print(f"\n处理问题: {problem}")
        conclusion = sage.process(problem)
        
        # 显示结果
        print(f"\n最终结论: {conclusion}")
    
    # 显示历史记录
    print("\n历史处理记录:")
    history = sage.get_history()
    for i, item in enumerate(history, 1):
        print(f"{i}. 问题: {item['problem']}")
        print(f"   结论: {item['conclusion']}")

if __name__ == "__main__":
    main()
