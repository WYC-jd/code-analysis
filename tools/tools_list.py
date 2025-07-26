from .repo_tools import clone_repo, remove_cloned_repo, read_file_content, collect_repo_context
from .prompt_tools import build_prompt
from .report_tools import generate_report, save_report
from .leetcode_tools import get_problem_by_id

class Tool:
    def __init__(self, name: str, func, description: str):
        self.name = name
        self.func = func
        self.description = description

tools = [
    Tool(
        name="CloneRepo",
        func=clone_repo,
        description="克隆 Git 仓库到指定目录"
    ),
    Tool(
        name="RemoveClonedRepo",
        func=remove_cloned_repo,
        description="删除临时克隆的 Git 仓库"
    ),
    Tool(
        name="ReadFileContent",
        func=read_file_content,
        description="读取指定文件的内容"
    ),
    Tool(
        name="CollectRepoContext",
        func=collect_repo_context,
        description="收集项目的相关上下文信息（如 README, pyproject, 代码文件等）"
    ),
    Tool(
        name="BuildPrompt",
        func=build_prompt,
        description="根据收集到的上下文构建分析提示词"
    ),
    Tool(
        name="GenerateReport",
        func=generate_report,
        description="生成项目分析报告"
    ),
    Tool(
        name="SaveReport",
        func=save_report,
        description="保存生成的报告为 Markdown 文件"
    ),
    Tool(
        name="LeetCode",
        func=get_problem_by_id,
        description="根据题目编号获取题目详细信息"
    ),
]
