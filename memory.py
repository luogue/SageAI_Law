import json
import os

class Memory:
    def __init__(self, memory_file='memory.json'):
        self.memory_file = memory_file
        self.memories = self.load_memory()
    
    def load_memory(self):
        """
        加载记忆
        :return: 记忆数据
        """
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载记忆失败: {e}")
                return []
        return []
    
    def save_memory(self):
        """
        保存记忆
        """
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memories, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存记忆失败: {e}")
    
    def add_memory(self, item):
        """
        添加记忆
        :param item: 记忆项
        """
        self.memories.append(item)
        self.save_memory()
    
    def get_memories(self):
        """
        获取所有记忆
        :return: 记忆列表
        """
        return self.memories
    
    def clear_memory(self):
        """
        清空记忆
        """
        self.memories = []
        self.save_memory()
