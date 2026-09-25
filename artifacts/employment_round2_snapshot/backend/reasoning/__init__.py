"""推理层：支持多领域扩展"""
import os

def get_supported_domains() -> list:
    """获取所有支持的领域列表"""
    reasoning_dir = os.path.dirname(__file__)
    domains = []

    for entry in os.listdir(reasoning_dir):
        entry_path = os.path.join(reasoning_dir, entry)
        if os.path.isdir(entry_path) and not entry.startswith('_') and entry != '__pycache__':
            domains.append(entry)

    return domains

def load_reasoning_module(domain: str):
    """加载指定领域的推理模块（保留接口但不再使用）"""
    raise NotImplementedError("推理模块已重构，请使用 inference_layer.run_inference()")
