import requests
import re
import os 

def generate_report(prompt: str, api_key: str):
    """
    使用 LLM 生成报告
    """
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek-chat", 
        "messages": [
            {"role": "system", "content": "你是一位擅长软件结构和架构设计分析的专家。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 4096,
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"请求失败: {response.status_code}\n{response.text}")

    data = response.json()
    content = data['choices'][0]['message']['content']
    return content

def save_report(content, question_id=None, question_title=None):
    """
    保存分析报告
    """
    # 清理 Markdown 内容
    cleaned_content = clean_markdown_content(content)
    if question_id and question_title:
        filename = f"{question_id}.{question_title}-solution.md"
    else:
        filename = generate_filename_from_content(cleaned_content)
    filepath = f"reports/" + filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(cleaned_content)
    print(f"✅ 分析报告已保存至: {filepath}")

def generate_filename_from_content(content: str, directory: str = '.'):
    """
    根据 Markdown 内容的第一个标题生成文件名
    """
    # 查找第一个以 "#" 开头的标题（包括 #, ##, ###, 等）
    match = re.search(r'^\s*#{1,}\s*(.+?)\s*$', content, re.MULTILINE)
    
    if match:
        title = match.group(1)
        # 将标题中的空格和特殊字符替换为下划线，转换为小写
        filename = f"{title.replace(' ', '_').replace('/', '_').lower()}.md"
    else:
        # 如果没有找到标题，使用默认名称
        filename = "untitled_report.md"

    # 检查文件是否已经存在，如果存在，添加数字后缀
    file_path = os.path.join(directory, filename)
    
    # 如果文件已存在，递增数字后缀直到找到一个可用的文件名
    if os.path.exists(file_path):
        base_filename, extension = os.path.splitext(filename)
        count = 1
        while os.path.exists(file_path):
            filename = f"{base_filename}_{count}{extension}"
            file_path = os.path.join(directory, filename)
            count += 1

    return filename

def clean_markdown_content(content: str):
    """
    清理 Markdown 内容，去掉开头和结尾的代码块标记
    """
    # 去掉开头的 ```markdown 和结尾的 ```
    cleaned_content = content.strip()
    
    # 如果内容以 ```markdown 开头，并以 ``` 结尾，去除这些部分
    if cleaned_content.startswith("```markdown"):
        cleaned_content = cleaned_content[len("```markdown"):].strip()  # 去掉开头的 ```markdown
    if cleaned_content.endswith("```"):
        cleaned_content = cleaned_content[:-3].strip()  # 去掉结尾的 ```
    
    return cleaned_content





