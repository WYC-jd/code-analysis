import os, json

def build_prompt(context: dict, file_path=None, code_snippet=None, text=None):
    # 读取模板 JSON 文件
    # 获取当前脚本的路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 拼接文件路径
    code_path = os.path.join(current_dir, '..', 'prompt_template', "code.json")
    file_content_path = os.path.join(current_dir, '..', 'prompt_template', "file_content.json")
    repo_path = os.path.join(current_dir, '..', 'prompt_template', "repo.json")
    leetcode_path = os.path.join(current_dir, '..', 'prompt_template', "leetcode.json")

    with open(code_path, 'r', encoding='utf-8') as f:
        code_template = json.load(f)
    with open(file_content_path, 'r', encoding='utf-8') as f:
        file_template = json.load(f)
    with open(repo_path, 'r', encoding='utf-8') as f:
        repo_template = json.load(f)
    with open(leetcode_path, 'r', encoding='utf-8') as f:
        leetcode_template = json.load(f)

    prompt = ""
    # 如果是纯文本描述，生成解答prompt
    if text:
        # 生成基础的 prompt
        prompt = leetcode_template["header"]
        # 添加题目描述
        prompt += leetcode_template["description"].format(
            description = context["Description"]
        )

        # 添加分析要求
        prompt += f"\nleetcode_template['analysis']"


    # 如果是代码段，生成针对代码的分析prompt
    elif code_snippet:
        # 生成基础的 prompt
        prompt = code_template["header"]
    
        # 添加 sections 内容
        for section in code_template["sections"]:
            prompt += f"\n{section}"
    
        # 添加文件内容（动态部分）
        prompt += f"\n{code_template['code_header']}"
        prompt += f"{context['CodeSnippet'][:1500]}"  # 动态填充文件内容
        prompt += code_template['code_footer']
    
    # 如果是文件内容，生成针对文件的分析prompt
    elif file_path:
        # 生成基础的 prompt
        prompt = file_template["header"]
    
        # 添加 sections 内容
        for section in file_template["sections"]:
            prompt += f"\n{section}"
    
        # 添加文件内容（动态部分）
        prompt += f"\n{file_template['file_header']}"
        prompt += f"{context['FileContent'][:1500]}"  # 动态填充文件内容
        prompt += file_template['file_footer']
    
    else:
        prompt = repo_template["header"]

        # 添加每个 section
        for section in repo_template["sections"]:
            prompt += f"\n{section}"

        # 添加文件内容部分
        prompt += "\n" + repo_template["sections"][-1]  # 添加代码文件分析的标题

        # 添加文件内容，分批处理
        max_file_length = 1500  # 每个文件传递的最大长度
        files_processed = 0
        for code_file in context.get("CodeFiles", []):
            file_content = code_file['content']
        
            # 如果内容过长，截取前1500字符
            truncated_content = file_content[:max_file_length]
            prompt += f"代码文件: {code_file['file_path']}\n{truncated_content}\n\n"
        
            files_processed += 1
            # 如果超过处理的最大文件数量，可以选择停止
            if files_processed > 10:  # 例如只处理前10个文件
                break
        prompt += f"codefiles为代码文件（请分析核心部分，可以根据readme判断）\n\n"
        # 填充 footer 中的动态部分
        prompt += repo_template["footer"].format(
            tree=context["Tree"],
            readme=context["README"][:2000],
            pyproject=context["Pyproject"][:1500],
            dockerfile=context["Dockerfile"][:1500],
            makefile=context["Makefile"][:1500],
            cli=context["CLI"][:1500]
        )
    return prompt.strip()





