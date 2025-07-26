import os
import shutil
import git

def clone_repo(repo_url: str, clone_dir: str):
    """
    克隆 Git 仓库到指定的目录
    """
    if os.path.exists(clone_dir):
        remove_cloned_repo(clone_dir)  # 如果目录已经存在，先删除
    print(f"正在克隆仓库: {repo_url} 到 {clone_dir}")
    try:
        git.Repo.clone_from(repo_url, clone_dir)
        print(f"成功克隆仓库到: {clone_dir}")
    except Exception as e:
        print(f"克隆失败: {e}")
        raise

def remove_cloned_repo(clone_dir: str):
    """
    删除临时克隆的仓库
    """
    try:
        if os.path.exists(clone_dir):
            shutil.rmtree(clone_dir)
            print(f"已删除临时仓库目录: {clone_dir}")

    except PermissionError:
            print(f"拒绝访问: {clone_dir}。尝试强制删除。")
            # 强制设置文件权限
            for root, dirs, files in os.walk(clone_dir, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    try:
                        os.chmod(file_path, 0o777)  # 更改文件权限
                        os.remove(file_path)  # 删除文件
                    except Exception as e:
                        print(f"无法删除文件 {file_path}: {str(e)}")

                for name in dirs:
                    dir_path = os.path.join(root, name)
                    try:
                        os.chmod(dir_path, 0o777)  # 更改目录权限
                        os.rmdir(dir_path)  # 删除目录
                    except Exception as e:
                        print(f"无法删除目录 {dir_path}: {str(e)}")
            # 尝试删除顶层目录
            shutil.rmtree(clone_dir)
            print(f"已强制删除临时仓库目录: {clone_dir}")
    except Exception as e:
        print(f"删除失败: {str(e)}")

def read_file_content(file_path: str):
    """
    读取文件内容
    """
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    else: 
        return ""

def collect_repo_context(repo_root: str = None, file_path: str = None, code_snippet: str = None, text: str = None):
    """
    根据仓库路径或指定文件分析
    如果指定了 specific_file，则只分析该文件；
    如果提供了 code_snippet，则只分析这段代码。
    """
    print(f"读取项目信息...")
    context = {}

    if text:
        # 构建上下文（将题目描述和代码片段按照模板组织）
        context["Description"] = text

    # 如果提供了文件路径，读取该文件
    elif file_path:
        context["FileContent"] = read_file_content(file_path)

    # 如果提供了代码段，直接使用代码段
    elif code_snippet:
        context["CodeSnippet"] = code_snippet

    # 如果没有指定文件或代码段，则分析整个仓库
    else:
        # 自动收集 README 文件
        readme_path = os.path.join(repo_root, "README.md")
        context["README"] = read_file_content(readme_path)

        # 自动收集 pyproject.toml 文件
        pyproject_path = os.path.join(repo_root, "pyproject.toml")
        context["Pyproject"] = read_file_content(pyproject_path)

        # 自动收集 Dockerfile 文件
        dockerfile_path = os.path.join(repo_root, "Dockerfile")
        context["Dockerfile"] = read_file_content(dockerfile_path)

        # 自动收集 Makefile 文件
        makefile_path = os.path.join(repo_root, "Makefile")
        context["Makefile"] = read_file_content(makefile_path)

        # 自动收集 CLI 文件
        cli_path = os.path.join(repo_root, "CLI")
        context["CLI"] = read_file_content(cli_path)

        # 收集所有 Python 文件或其他关键代码文件
        context["CodeFiles"] = []
        for root, dirs, files in os.walk(repo_root):
            for file in files:
                if file.endswith(".py") or file.endswith(".js") or file.endswith(".go"):  # 根据需要扩展其他语言
                    file_path = os.path.join(root, file)
                    file_content = read_file_content(file_path)
                    relative_path = os.path.relpath(file_path, repo_root)
                    context["CodeFiles"].append({"file_path": relative_path, "content": file_content})

        # 自动收集整个项目的文件树
        context["Tree"] = "\n".join([str(root) for root, dirs, files in os.walk(repo_root)])

    return context





