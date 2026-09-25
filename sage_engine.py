"""Sage 推理引擎 - 已切换为纯云端 API 模式（DeepSeek）"""
from methods import abstract, main_contradiction, boundary, verify, classify_domain
from memory import Memory

from backend.model_settings import configuration

class SageEngine:
    def __init__(self):
        self.memory = Memory()
        self.model = configuration()['model']
        print("云端 DeepSeek 模式：" + ("已配置" if configuration()['key'] else "未配置"))

    def process(self, problem):
        domain, domain_desc = classify_domain(problem)
        print(f"1. 定位领域: [{domain}] - {domain_desc}")

        essence = abstract(problem)
        print(f"2. 抽象本质: {essence}")

        contradiction = main_contradiction(problem)
        print(f"3. 抓主要矛盾: {contradiction}")

        # 推理通过云端 API 完成，由后端 inference_layer 统一调用
        reasoning_result = boundary(problem)
        print(f"4. 定义边界: {reasoning_result}")

        conclusion = f"基于[{domain}]领域分析，问题 '{problem}' 的解决方案"
        print(f"5. 输出结论: {conclusion}")

        verification = verify(conclusion, problem)
        print(f"6. 验证: {verification}")

        memory_item = {
            "problem": problem,
            "domain": domain,
            "essence": essence,
            "contradiction": contradiction,
            "reasoning": reasoning_result,
            "conclusion": conclusion,
            "verification": verification
        }
        self.memory.add_memory(memory_item)

        print("\n7. 实践循环:")
        print("   - 理论: 基于分析形成解决方案")
        print("   - 验证: 验证解决方案的有效性")
        print("   - 反馈: 收集反馈信息")
        print("   - 迭代: 根据反馈优化解决方案")

        return conclusion

    def get_history(self):
        return self.memory.get_memories()