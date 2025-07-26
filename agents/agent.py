from tools.tools_list import tools
from memory.memory import Memory
import os

class Agent:
    def __init__(self, api_key: str, memory: Memory):
        self.api_key = api_key
        self.memory = memory

    def analyze_project(self, repo_url: str = None, file_path: str = None, code_snippet: str = None):
        """
        使用不同的工具来分析项目或代码段, 支持远程仓库、本地仓库、文件路径或代码段
        """

        # 检查参数有效性
        if not any([repo_url, file_path, code_snippet]):
            raise ValueError("必须提供 repo_url、file_path、code_snippet之一进行分析。")
    
        if repo_url and file_path:
            raise ValueError("不能同时提供 repo_url 和 file_path。请仅选择其中一个进行分析。")
    
        if repo_url and code_snippet:
            raise ValueError("不能同时提供 repo_url 和 code_snippet。请仅选择其中一个进行分析。")
    
        if file_path and code_snippet:
            raise ValueError("不能同时提供 file_path 和 code_snippet。请仅选择其中一个进行分析。")

        context = {}

        # 第一步：克隆仓库
        if repo_url.startswith("http://") or repo_url.startswith("https://"):
            # 思考过程
            self.memory.add_thought(f"正在分析项目: {repo_url}")
            clone_dir = "./temp_repo"  # 临时克隆的目录
            self.memory.add_thought(f"克隆 Git 仓库到 {clone_dir}")

            try:
                self.run_tool("CloneRepo", repo_url, clone_dir)
                repo_root = clone_dir
                self.memory.add_execution("克隆仓库", f"成功克隆到 {clone_dir}")
            except Exception as e:
                self.memory.add_execution("克隆仓库", f"失败: {str(e)}")

        elif os.path.exists(repo_url):
            # 如果提供了本地仓库路径
            repo_root = repo_url
            self.memory.add_thought(f"使用本地仓库路径进行分析: {repo_root}")

        else:
            repo_root = None

        # 第二步：收集项目上下文
        context = self.run_tool("CollectRepoContext", repo_root, file_path, code_snippet)
        self.memory.add_thought(f"读取文件内容")
        
        if context:
            self.memory.add_execution("读取文件", "成功读取文件内容")
        else:
            self.memory.add_execution("读取文件", "读取失败,文件不存在")


        # 第三步：构建分析报告
        prompt = self.run_tool("BuildPrompt", context, file_path, code_snippet)
        self.memory.add_thought(f"根据文件内容生成分析报告的提示词")

        # 使用 LLM 生成分析报告
        try:
            report = self.run_tool("GenerateReport", prompt, self.api_key)
            self.memory.add_execution("生成报告", f"成功生成报告")
            self.memory.add_thought(f"生成的报告内容: {report[:100]}...")  # 保存报告的部分内容（避免超长）
        except Exception as e:
            self.memory.add_execution("生成报告", f"失败: {str(e)}")

        # 第四步：保存报告
        self.run_tool("SaveReport", report)
        self.memory.add_thought(f"报告已保存")

        # 删除临时克隆的仓库
        if repo_root and repo_root != repo_url:
            self.run_tool("RemoveClonedRepo", repo_root)

        return report

    def analyze_leetcode_solution(self, question_id: int):
        """
        分析 LeetCode 题目代码，生成解决方案和分析报告
        """
        context = {}

        # Step 1: 收集题目代码上下文（题目描述等）
        self.memory.add_thought("正在分析 LeetCode 代码")
    
        # 使用题目描述和代码片段来构建上下文
        problem_description, question_id, question_title = self.run_tool("LeetCode", question_id)

        context = self.run_tool("CollectRepoContext", text=problem_description)
        
        # Step 2: 根据题目代码和描述构建分析报告的提示词
        prompt = self.run_tool("BuildPrompt", context, text=problem_description)
        self.memory.add_thought("根据题目描述生成分析报告的提示词")

        # Step 3: 使用 LLM 生成 Python 解答
        try:
            solution = self.run_tool("GenerateReport", prompt, self.api_key)
            self.memory.add_execution("生成解决方案", f"成功生成解答")
        except Exception as e:
            self.memory.add_execution("生成解决方案", f"失败: {str(e)}")
            return f"解决方案生成失败: {str(e)}"
    
        # Step 4: 保存报告和解决方案
        try:
            self.run_tool("SaveReport", solution, question_id, question_title)
            self.memory.add_thought("解决方案和报告已保存")
        except Exception as e:
            self.memory.add_execution("保存报告", f"失败: {str(e)}")
            return f"报告保存失败: {str(e)}"

        return solution



    def run_tool(self, tool_name, *args, **kwargs):
        """
        根据工具名称来执行工具
        """
        tool = next(tool for tool in tools if tool.name == tool_name)
        return tool.func(*args, **kwargs)
