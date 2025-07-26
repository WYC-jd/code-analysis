import json
import os
from datetime import datetime

class Memory:
    def __init__(self, memory_folder="memory",memory_file="memory.json"):
        # 创建 memory 文件夹（如果不存在）
        self.memory_folder = memory_folder
        os.makedirs(self.memory_folder, exist_ok=True)

        self.memory_file = os.path.join(self.memory_folder, memory_file)
        self.memory_data = self.load_memory()

    def load_memory(self):
        """从文件加载记忆数据"""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"thoughts": [], "executions": []}

    def save_memory(self):
        """保存记忆数据到文件"""
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory_data, f, ensure_ascii=False, indent=4)

    def add_thought(self, thought: str):
        """添加思考过程到记忆"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.memory_data["thoughts"].append({"timestamp": timestamp, "thought": thought})
        self.save_memory()

    def add_execution(self, action: str, result: str):
        """添加执行过程到记忆"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.memory_data["executions"].append({"timestamp": timestamp, "action": action, "result": result})
        self.save_memory()

    def get_thoughts(self):
        """获取所有思考记录"""
        return self.memory_data.get("thoughts", [])

    def get_executions(self):
        """获取所有执行记录"""
        return self.memory_data.get("executions", [])

    def clear_memory(self):
        """清空记忆数据"""
        self.memory_data = {"thoughts": [], "executions": []}
        self.save_memory()
