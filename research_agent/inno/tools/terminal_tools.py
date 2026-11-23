import os
import socket
import json
import base64
import math
# from metachain.util import run_command_in_container
from research_agent.inno.environment.docker_env import DockerEnv, DockerConfig
from research_agent.inno.registry import register_tool
from research_agent.inno.environment.markdown_browser.requests_markdown_browser import RequestsMarkdownBrowser
from typing import Tuple, Optional, Dict
import time
import tiktoken
from functools import wraps
from rich.console import Console
from pathlib import Path

terminal_env = RequestsMarkdownBrowser(local_root=os.getcwd(), workplace_name="terminal_env", viewport_size=1024 * 6)

def _get_browser_state(env: RequestsMarkdownBrowser) -> Tuple[str, str]:
    """
    Get the current state of the browser, including the header and content.
    """
    # print(env.address)
    address = env.address
    tool_name = address.split('/')[-1].split('.')[0].split('___')[-1]
    header = f"[The output of the tool `{tool_name}` showing in the interactive terminal]\n"

    current_page = env.viewport_current_page
    total_pages = len(env.viewport_pages)

    
    for i in range(len(env.history) - 2, -1, -1):  # Start from the second last
        if env.history[i][0] == address:
            header += f"You previously visited this page of terminal {round(time.time() - env.history[i][1])} seconds ago.\n"
            break
    prefix = f"[Your terminal is currently open to the page '{env.page_title}']\n" if env.page_title is not None else ""
    
    header = prefix + header
    header += f"Terminal viewport position: Showing page {current_page+1} of {total_pages}.\n"
    if total_pages > 1:
        header += f"[NOTE] The output of the tool `{tool_name}`, you can use `terminal_page_up` to scroll up and `terminal_page_down` to scroll down. If there are many pages with meaningless content like progress bar or output of generating directory structure when there are many datasets in the directory, you can use `terminal_page_to` to move the viewport to the end of terminal where the meaningful content is.\n"
    return (header, env.viewport)

@register_tool("terminal_page_up")
def terminal_page_up():
    """
    Scroll the viewport UP one page-length in the current terminal. Use this function when the terminal is too long and you want to scroll up to see the previous content.
    """
    try: 
        terminal_env.page_up()
        header, content = _get_browser_state(terminal_env)
        final_response = header.strip() + "\n==============================================\n" + content + "\n==============================================\n"
        return final_response
    except Exception as e:
        return f"Error in `page_up`: {e}"
    
@register_tool("terminal_page_down")
def terminal_page_down():
    """
    Scroll the viewport DOWN one page-length in the current terminal. Use this function when the terminal is too long and you want to scroll down to see the next content.
    """
    try: 
        terminal_env.page_down()
        header, content = _get_browser_state(terminal_env)
        final_response = header.strip() + "\n==============================================\n" + content + "\n==============================================\n"
        return final_response
    except Exception as e:
        return f"Error in `page_down`: {e}"
@register_tool("terminal_page_to")
def terminal_page_to(page_idx: int):
    """
    Move the viewport to the specified page index. The index starts from 1.
    Use this function when you want to move the viewport to a specific page, especially when the middle of terminal output are meaningless, like the output of progress bar or output of generating directory structure when there are many datasets in the directory, you can use this function to move the viewport to the end of terminal where the meaningful content is.
    """
    try:
        terminal_env.page_to(page_idx - 1)
        header, content = _get_browser_state(terminal_env)
        final_response = header.strip() + "\n==============================================\n" + content + "\n==============================================\n"
        return final_response
    except Exception as e:
        return f"Error in `page_to`: {e}"

def process_terminal_response(func):
    """
    装饰器函数，用于处理命令执行的响应结果
    - 如果结果是包含 status 和 result 的字典，返回格式化后的结果
    - 如果结果是错误字符串，直接返回
    """
    @wraps(func)  # 保持原函数的签名和文档
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        
        # 如果返回值是字典且包含 status 和 result
        if isinstance(result, dict) and 'status' in result and 'result' in result:
            try:
                address = f"terminal://{time.time_ns()}/{func.__name__}"
                terminal_env.open_text(address, result["result"] or " ")
                header, content = _get_browser_state(terminal_env)
                return f"{header.strip()}\n==============================================\n{content}\n==============================================\n"
            except Exception as e:
                return f"Error in the post-processing of `{func.__name__}`: {e}"
            
        elif isinstance(result, str):
            return result
        else:
            return f"Error in `{func.__name__}`: {result}"
    
    return wrapper
@register_tool("read_file")
@process_terminal_response
def read_file(file_path: str, env: DockerEnv) -> str:
    """
    Read the contents of a file and return it as a string. Use this function when there is a need to check an existing file.
    Args:
        file_path: The path of the file to read.
    Returns:
        A string representation of the contents of the file.
    """
    try:
        command = f"cat {file_path}"
        response = env.run_command(command) # status, result
        # res_output = truncate_by_tokens(env, response['result'], 10000)
        # return f"Exit code: {response['status']} \nOutput: \n{res_output}"
        return response
    except FileNotFoundError:
        return f"Error in reading file: {file_path}"

def write_file_in_chunks(file_content, output_path, env: DockerEnv, chunk_size=100000):
    encoded_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
    total_chunks = math.ceil(len(encoded_content) / chunk_size)
    
    for i in range(total_chunks):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        chunk = encoded_content[start:end]
        
        # use cat command
        if i == 0:
            command = f"echo \"{chunk}\" | base64 -d > {output_path}"
        else:
            command = f"echo \"{chunk}\" | base64 -d >> {output_path}"
        
        response = env.run_command(command)
        
        if response["status"] != 0:
            return f"Error creating file {output_path}: " + response["result"]
        
        # print(f"Successfully written block {i+1}/{total_chunks}")
    
    return f"File created at: {output_path}"

@register_tool("create_file")
def create_file(path: str, content: str, env: DockerEnv) -> str:
    """
    Create a file with the given path and content. Use this function when there is a need to create a new file with initial content.
    Args:
        path: The path to the file to create.
        content: The initial content to write to the file.
    Returns:
        A string representation of the result of the file creation.
    """
    try:
        msg = write_file_in_chunks(content, path, env)
        return msg
    except Exception as e:
        return f"Error creating file: {str(e)}"

@register_tool("write_file")
def write_file(path: str, content: str, env: DockerEnv) -> str:
    """
    Write content to a file. Use this function when there is a need to write content to an existing file.
    Args:
        path: The path to the file to write to.
        content: The content to write to the file.
    Returns:
        A string representation of the result of the file writing.
    """
    try:
        msg = write_file_in_chunks(content, path, env)
        return msg
    except Exception as e:
        return f"Error writing to file: {str(e)}"

@register_tool("list_files")
@process_terminal_response
def list_files(path: str, env: DockerEnv) -> str:
    """
    List all files and directories under the given path if it is a directory. Use this function when there is a need to list the contents of a directory.
    Args:
        path: The file system path to check and list contents from.
    Returns:
        A string representation of the contents of the directory.
    """
    if os.path.isfile(path):
        return "The given path is a file. Please provide a path of a directory."
    command = f"ls -1 {path}"
    response = env.run_command(command)
    if response["status"] != 0:
        return f"Error listing files: {response['result']}"
    return response

@register_tool("create_directory")
def create_directory(path: str, env: DockerEnv) -> str:
    """
    Create a directory if it does not exist. Use this function when there is a need to create a new directory.
    Args:
        path: The path of the directory to create.
    Returns:
        A string representation of the result of the directory creation.
    """
    try:
        command = f"mkdir -p {path}"
        response = env.run_command(command)
        if response["status"] != 0:
            return f"Error creating directory: {response['result']}"
        return f"Directory '{path}' created successfully."
    except OSError as error:
        return f"Creation of the directory '{path}' failed due to: {error}"

@register_tool("gen_code_tree_structure")
@process_terminal_response
def gen_code_tree_structure(directory: str, env: DockerEnv) -> str:
    """Generate a tree structure of the code in the specified directory. Use this function when you need to know the overview of the codebase and want to generate a tree structure of the codebase.
    Args:
        directory: The directory to generate the tree structure for.
    Returns:
        A string representation of the tree structure of the code in the specified directory.
    """
    try:
        command = f"tree {directory}"
        response = env.run_command(command)
        return response
    except Exception as e:
        return f"Error running tree {directory}: {str(e)}"
    
def print_stream(text):
    console = Console()
    console.print(f"[grey42]{text}[/grey42]")
@register_tool("execute_command")
@process_terminal_response
def execute_command(command: str, env: DockerEnv) -> str:
    """
    Execute a command in the system shell. Use this function when there is a need to run a system command, and execute programs.
    Args:
        command: The command to execute in the system shell.
    Returns:
        A string representation of the exit code and output of the command.
    """
    try:
        response = env.run_command(command, print_stream)
        return response
    except Exception as e:
        return f"Error running command: {str(e)}"

def print_stream(text):
    console = Console()
    console.print(f"[grey42]{text}[/grey42]")
def set_doc(doc_template):
    def decorator(func):
        func.__doc__ = doc_template
        return func
    return decorator

@register_tool("run_python")
@process_terminal_response
def run_python(
    env: DockerEnv,
    code_path: str,
    cwd: str = None,
    env_vars: Optional[Dict[str, str]] = None,
) -> str:
    """
    Run a python script. 
    Args:
        code_path: The absolute or relative path (the relative path is from the root of the workplace `/workplace`) to the python script file.
        cwd: The working directory of the python script. If not provided, will regard the directory of the script as the working directory. If there is a command `cd ...` in the instruction for running the script, you should provide the cwd and not use the default value. (Optional)
        env_vars: The environment variables to be set before running the python script. (Optional)
    Returns:
        A string representation of the exit code and output of the python script.
    """
    try:
        # 转换为绝对路径
        # abs_path = str(Path(code_path).resolve())
        if Path(code_path).is_absolute():
            if env.run_command(f"ls {code_path}")['status'] != 0: return f"File {code_path} does not exist"
            code_abs_path = code_path
        else: 
            code_abs_path = f"{env.docker_workplace}/{code_path}"
            if env.run_command(f"ls {code_abs_path}")['status'] != 0: return f'You use a relative path, so we regard the `{env.docker_workplace}` as the root of the workplace, but `{code_abs_path}` does not exist'
        
        
        if cwd:
            # 使用指定的项目根目录
            if Path(cwd).is_absolute():
                if env.run_command(f"ls {cwd}")['status'] != 0: return f"Working directory {cwd} does not exist"
            else: 
                cwd = f"{env.docker_workplace}/{cwd}"
                if env.run_command(f"ls {cwd}")['status'] != 0: return f"You use a relative path for `cwd`, so we regard the `{env.docker_workplace}` as the working directory, but `{cwd}` does not exist"
        else:
            cwd = str(Path(code_abs_path).parent)
            
        
        # 设置PYTHONPATH
        pythonpath = str(cwd)
        
        # 获取Python解释器路径
        env_str = f"PYTHONPATH={pythonpath}"
        
        if env_vars:
            env_str += " " + " ".join([f"{k}={v}" for k, v in env_vars.items()])
        # print(env_str)
        
        # 构建相对模块路径
        try:
            rel_path = Path(code_abs_path).relative_to(cwd)
            module_path = str(rel_path.with_suffix('')).replace(os.sep, '.')
            
            command = f"cd {cwd} && {env_str} python -m {module_path}"
        except ValueError:
            # 如果无法构建相对路径，使用完整路径
            command = f"cd {cwd} && {env_str} python {code_path}"
            
        # print(f"Executing: {command}")
        
        result = env.run_command(command, print_stream)
        return result
        
    except Exception as e:
        return f"Error when running the python script: {e}"


if __name__ == "__main__":
    env_config = DockerConfig(
        container_name = "paper_eval_dit", 
        workplace_name = "workplace", 
        communication_port = 7040, 
        local_root = "/root/tjb/AI-Researcher/research_agent/workplace_test"
    )
    env = DockerEnv(env_config)
    env.init_container()

    print("=" * 60)
    print("开始测试 Terminal Tools")
    print("=" * 60)
    
    # 1. 测试创建目录
    print("\n1. 测试 create_directory:")
    result = create_directory("/workplace/test_dir", env)
    print(result)
    
    # 2. 测试创建文件
    print("\n2. 测试 create_file:")
    test_content = """# 测试文件
print("Hello from test file!")
import os
print(f"当前工作目录: {os.getcwd()}")
for i in range(5):
    print(f"循环 {i}")
"""
    result = create_file("/workplace/test_dir/test_script.py", test_content, env)
    print(result)
    
    # 3. 测试写入文件
    print("\n3. 测试 write_file:")
    result = write_file("/workplace/test_dir/config.txt", "配置文件内容\nkey=value\ndebug=true", env)
    print(result)
    
    # 4. 测试读取文件
    print("\n4. 测试 read_file:")
    result = read_file("/workplace/test_dir/config.txt", env)
    print("读取文件结果:")
    print(result)
    
    # 5. 测试列出文件
    print("\n5. 测试 list_files:")
    result = list_files("/workplace/test_dir", env)
    print("列出文件结果:")
    print(result)
    
    # 6. 测试执行命令
    print("\n6. 测试 execute_command:")
    result = execute_command("cd /workplace/test_dir && ls -la ./", env)
    print("执行命令结果:")
    print(result)
    
    # 7. 测试生成代码树结构
    print("\n7. 测试 gen_code_tree_structure:")
    result = gen_code_tree_structure("/workplace/test_dir", env)
    print("代码树结构:")
    print(result)
    
    # 8. 测试运行Python脚本
    print("\n8. 测试 run_python:")
    result = run_python(env, "/workplace/test_dir/test_script.py")
    print("运行Python脚本结果:")
    print(result)
    
    # 9. 测试带环境变量的Python脚本
    print("\n9. 测试带环境变量的 run_python:")
    env_vars = {"TEST_VAR": "hello_world", "DEBUG": "1"}
    result = run_python(env, "/workplace/test_dir/test_script.py", env_vars=env_vars)
    print("带环境变量运行结果:")
    print(result)
    
    # 10. 测试terminal分页功能
    print("\n10. 测试 terminal 分页功能:")
    # 创建一个长输出的命令
    long_command = "for i in {1..50}; do echo \"Line $i: This is a long output for testing pagination\"; done"
    result = execute_command(long_command, env)
    print("长输出命令执行完成，测试分页:")
    
    # 测试向上翻页
    print("\n测试 terminal_page_up:")
    result = terminal_page_up()
    print(result[:200] + "..." if len(result) > 200 else result)
    
    # 测试向下翻页
    print("\n测试 terminal_page_down:")
    result = terminal_page_down()
    print(result[:200] + "..." if len(result) > 200 else result)
    
    # 测试跳转到指定页
    print("\n测试 terminal_page_to(1):")
    result = terminal_page_to(1)
    print(result[:200] + "..." if len(result) > 200 else result)
    
    print("\n" + "=" * 60)
    print("所有 Terminal Tools 测试完成!")
    print("=" * 60)
    
