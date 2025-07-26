from agents.agent import Agent
from memory.memory import Memory
import os

if __name__ == "__main__":
    api_key = os.getenv("DEEPSEEK_API_KEY")
    memory = Memory()

    # 示例1: 仓库链接 "https://gitee.com/ByteDance/trae-agent", "https://gitee.com/devine/OpenHands", r"D:\sjtu_class\暑期实习\第三周\trae-agent"
    repo_url = "https://gitee.com/devine/OpenHands" # 用户提供的仓库链接
    agent = Agent(api_key, memory)
    report = agent.analyze_project(repo_url)

    ## 示例2：分析单个文件
    #file_path = r"D:\sjtu_class\暑期实习\第三周\sequential_thinking_tool\sequential_thinking_tool.py"
    #agent = Agent(api_key, memory)
    #report = agent.analyze_project(file_path=file_path)

    ## 示例3：分析单段代码
    #code_snippet = """
    #def hello_world():
    #    print("Hello, world!")
    #"""
    #agent = Agent(api_key, memory)
    #report = agent.analyze_project(None, code_snippet=code_snippet)

    ## 示例4：根据leetcode题目编号获得解答
    #agent = Agent(api_key, memory)
    ## 输入题目编号
    #question_id = int(input("请输入题目编号："))
    #solution = agent.analyze_leetcode_solution(question_id)

    ## 错误示例1
    #repo_url = "https://gitee.com/devine/OpenHands"
    #file_path = r"D:\sjtu_class\暑期实习\第三周\sequential_thinking_tool\sequential_thinking_tool.py"
    #code_snippet = """
    #def hello_world():
    #    print("Hello, world!")
    #"""
    #agent = Agent(api_key, memory)
    #report = agent.analyze_project(repo_url, file_path=file_path, code_snippet=code_snippet)

    ## 错误示例2
    #agent = Agent(api_key, memory)
    #report = agent.analyze_project(repo_url=None, file_path=None, code_snippet=None)

    

    # 查看智能体的思考和执行记录
    print("最新的思考记录:")
    thoughts = memory.get_thoughts()
    if thoughts:
        latest_thought = thoughts[-3]  # 获取最后3条思考记录
        print(f"[{latest_thought['timestamp']}] 思考: {latest_thought['thought']}")
    else:
        print("没有思考记录。")

    print("\n最新的执行记录:")
    executions = memory.get_executions()
    if executions:
        latest_execution = executions[-3]  # 获取最后3条执行记录
        print(f"[{latest_execution['timestamp']}] 执行: {latest_execution['action']} -> {latest_execution['result']}")
    else:
        print("没有执行记录。")