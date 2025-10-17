from main_ai_researcher import main_ai_researcher
import os
import gradio as gr
import time
import json
import logging
import datetime
from typing import Tuple
import importlib
from dotenv import load_dotenv, set_key, find_dotenv, unset_key
import threading
import queue
import re  # For regular expression operations
import random
import global_state
import base64

os.environ["PYTHONIOENCODING"] = "utf-8"

# If you want to use proxy, please uncomment the following lines
# os.environ['https_proxy'] = 'http://100.68.161.73:3128'
# os.environ['http_proxy'] = 'http://100.68.161.73:3128'
# os.environ['no_proxy'] = 'localhost,127.0.0.1,0.0.0.0'

def setup_path():
    # logs_dir = os.path.join("casestudy_results", f'agent_{container_name}', 'logs')
    logs_dir = os.path.join("casestudy_results", f'agent', 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    # 生成日志文件名（使用当前日期）
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(logs_dir, f"gradio_log_{current_date}.log")
    return log_file


# 配置日志系统
def setup_logging():
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    log_file = os.path.join(logs_dir, f"log_{current_date}.log")
    global_state.LOG_PATH = log_file

    root_logger = logging.getLogger()

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    root_logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file, encoding="utf-8", mode="a")
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.info("Logging system initialized, log file: %s", log_file)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("LiteLLM").setLevel(logging.WARNING)
    return log_file


def return_log_file():
    return LOG_FILE

def return_paper_file():
    category = os.getenv("CATEGORY")
    instance_id = os.getenv("INSTANCE_ID")
    global PAPER_FILE
    PAPER_FILE = f'{category}/target_sections/{instance_id}/iclr2025_conference.pdf'
    return PAPER_FILE

def return_paper_log_file():
    return PAPER_LOG

def return_paper_log():
    logs_dir = os.path.join(os.path.dirname(__file__), "paper_agent", "paper_logs")
    os.makedirs(logs_dir, exist_ok=True)

    # logs_dir = os.path.join("casestudy_results", f'agent_{container_name}', 'logs')
    # os.makedirs(logs_dir, exist_ok=True)

    # 生成日志文件名（使用当前日期）
    # current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    log_file = os.path.join(logs_dir, f"rotated_vq_{current_date}.log")

    global_state.LOG_PATH = log_file

    # 配置根日志记录器（捕获所有日志）
    root_logger = logging.getLogger()

    # 清除现有的处理器，避免重复日志
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    root_logger.setLevel(logging.INFO)

    # 创建文件处理器
    file_handler = logging.FileHandler(log_file, encoding="utf-8", mode="a")
    file_handler.setLevel(logging.INFO)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 创建格式化器
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加处理器到根日志记录器
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.info("Logging system initialized, log file: %s", log_file)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("LiteLLM").setLevel(logging.WARNING)
    return log_file


def get_latest_log():
    path2save = os.path.splitext(os.path.basename(LOG_FILE))[0]
    # Read the current content of the log file
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        # Create a temporary file with timestamp to ensure uniqueness
        temp_file = f"{path2save}_copy.log"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(content)
        return temp_file
    except Exception as e:
        print(f"Error reading log file: {e}")
        return None


def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


# 全局变量
LOG_FILE = None
LOG_READ_FILE = None
PAPER_LOG = None
category = os.getenv("CATEGORY")
instance_id = os.getenv("INSTANCE_ID")

PAPER_FILE = f'{category}/target_sections/{instance_id}/iclr2025_conference.pdf'
# PAPER_FILE = './vq/target_sections/rotated_vq/iclr2025_conference.pdf'
# PAPER_LOG = './paper_agent/paper_logs/rotated_vq.log'
LOG_QUEUE: queue.Queue = queue.Queue()
STOP_LOG_THREAD = threading.Event()
CURRENT_PROCESS = None
STOP_REQUESTED = threading.Event()




# 日志读取和更新函数
def log_reader_thread(log_file):
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            # 移动到文件末尾
            f.seek(0, 2)

            while not STOP_LOG_THREAD.is_set():
                line = f.readline()
                if line:
                    LOG_QUEUE.put(line)
                else:
                    time.sleep(0.1)
    except Exception as e:
        logging.error(f"Exception occurred in background log reader thread: {str(e)}")

def parse_logs_incrementally(logs, state_list, last_index):
    existing_inputs = set()
    existing_pairs = set()
    for input_text, output_text in state_list:
        existing_pairs.add((input_text.strip(), output_text.strip()))
        existing_inputs.add(input_text.strip())

    conversations = []
    current_convo = None
    state = "idle"

    new_logs = logs[last_index:]  # 只处理新日志
    new_last_index = last_index + len(new_logs)  # 更新后的索引

    # 定义需要显示的工具列表
    allowed_tools = {
        "execute_command", "run_python", "create_file", 
        "write_file", "list_files", "gen_code_tree_structure"
    }

    def adjust_markdown_headers(content):
        """调整markdown标题级别，确保不与主标题冲突"""
        lines = content.split('\n')
        adjusted_lines = []
        
        for line in lines:
            # 检查是否是markdown标题
            if line.strip().startswith('#'):
                # 计算当前标题级别
                header_level = 0
                for char in line:
                    if char == '#':
                        header_level += 1
                    else:
                        break
                
                # 如果是1-3级标题，调整为4-6级
                if header_level <= 3:
                    # 添加额外的#使其成为更低级别的标题
                    adjusted_line = '#' * (header_level + 3) + line[header_level:]
                    adjusted_lines.append(adjusted_line)
                else:
                    # 保持原样（4级及以上标题不变）
                    adjusted_lines.append(line)
            else:
                adjusted_lines.append(line)
        
        return '\n'.join(adjusted_lines)

    for line in new_logs:
        line = line.strip()

        if "Receive Task" in line or "Assistant Message" in line:
            if current_convo:
                conversations.append(current_convo)
            current_convo = {
                "user_time": None,
                "user_content": "",
                "assistant_time": None,
                "assistant_role": None,
                "assistant_content": "",
                "tool_calls_time": None,
                "tool_calls_content": "",
                "tool_execution_time": None,
                "tool_execution_content": "",
                "current_tool_name": None  # 添加当前工具名称跟踪
            }
            if "Receive Task" in line:
                state = "await_user_time"
            else:
                state = "await_assistant_time"

        elif current_convo is not None:
            if state == "await_user_time" and line.startswith("["):
                current_convo["user_time"] = line.strip("[]")
                state = "await_user_input"

            elif state == "await_user_input" and line.lower().startswith("receiveing the task:"):
                state = "user_content"

            elif state == "user_content" and not line.startswith("*"):
                current_convo["user_content"] += line + "\n"

            elif state == "await_assistant_time" and line.startswith("["):
                current_convo["assistant_time"] = line.strip("[]")
                state = "await_assistant_role"

            elif state == "await_assistant_role":
                if ":" in line:
                    parts = line.split(":", 1)
                    role = parts[0].strip()
                    content_line = parts[1].strip() + "\n"
                else:
                    role = "assistant"
                    content_line = line + "\n"

                current_convo["assistant_role"] = role
                current_convo["assistant_content"] += content_line
                state = "assistant_content"

            elif state == "assistant_content":
                if "Tool Calls" in line:
                    state = "await_tool_calls_time"
                elif "Tool Execution" in line:
                    state = "await_tool_execution_time"
                elif "End Turn" in line:
                    conversations.append(current_convo)
                    current_convo = None
                    state = "idle"
                else:
                    current_convo["assistant_content"] += line + "\n"

            elif state == "await_tool_calls_time" and line.startswith("["):
                current_convo["tool_calls_time"] = line.strip("[]")
                state = "tool_calls_content"

            elif state == "tool_calls_content":
                if "Tool Execution" in line:
                    state = "await_tool_execution_time"
                elif "End Turn" in line:
                    conversations.append(current_convo)
                    current_convo = None
                    state = "idle"
                else:
                    current_convo["tool_calls_content"] += line + "\n"
                    # 提取工具名称
                    if "tool execution:" in line.lower():
                        tool_name = line.split(":")[-1].strip()
                        current_convo["current_tool_name"] = tool_name

            elif state == "await_tool_execution_time" and line.startswith("["):
                current_convo["tool_execution_time"] = line.strip("[]")
                state = "tool_execution_content"

            elif state == "tool_execution_content":
                if "End Turn" in line:
                    conversations.append(current_convo)
                    current_convo = None
                    state = "idle"
                else:
                    current_convo["tool_execution_content"] += line + "\n"

    # 🧹 收尾：捕获未被 End Turn 收尾的对话
    if current_convo:
        conversations.append(current_convo)

    for convo in conversations:
        section_input = ""
        section_output = ""

        # ✅ 每轮独立处理 user_content
        if convo["user_content"].strip():
            section_input = f"### 🙋 User ({convo['user_time']})\n```markdown\n{convo['user_content'].strip()}\n```"
        else:
            section_input = ""

        input_clean = section_input.strip()

        if (input_clean, "") not in existing_pairs:
            state_list.append((input_clean, ""))
            existing_inputs.add(input_clean)
            existing_pairs.add((input_clean, ""))

        output_parts = []

        if convo["assistant_content"].strip():
            # 检查Assistant内容是否为"None"，如果是则设置为空字符串
            assistant_content = convo["assistant_content"].strip()
            if assistant_content.lower() == "none":
                assistant_content = ""
            
            # 始终显示Assistant块，即使内容为空
            output_parts.append(
                f"### 🤖 {convo['assistant_role']} ({convo['assistant_time']})\n{adjust_markdown_headers(assistant_content)}"
            )
        if convo["tool_calls_content"].strip():
            output_parts.append(
                f"### 🛠️ Tool Calls\n```python\n{convo['tool_calls_content'].strip()}\n```"
            )
        
        # 处理 Tool Execution 内容（只显示允许的工具，并放在markdown代码块中）
        if convo["tool_execution_content"].strip():
            # 检查是否是允许显示的工具
            tool_name = convo.get("current_tool_name", "")
            
            # 如果没有从tool_calls_content中提取到工具名，尝试从tool_execution_content中提取
            if not tool_name:
                for line in convo["tool_execution_content"].split('\n'):
                    if "tool execution:" in line.lower():
                        tool_name = line.split(":")[-1].strip()
                        break
            
            # 只显示允许的工具执行结果
            if tool_name in allowed_tools:
                tool_execution_content = convo["tool_execution_content"].strip()
                output_parts.append(
                    f"### ⚙️ Tool Execution\n```markdown\n{tool_execution_content}\n```"
                )

        if output_parts:
            section_output = "\n\n".join(output_parts)
            for i in reversed(range(len(state_list))):
                user, bot = state_list[i]
                if user.strip() == input_clean and not bot.strip():
                    new_pair = (user, section_output.strip())
                    if new_pair not in existing_pairs:
                        state_list[i] = new_pair
                        existing_pairs.add(new_pair)
                    break

    return state_list, new_last_index



def get_latest_logs(max_lines=500, state=None, queue_source=None, last_index=0):

    logs = []
    log_queue = queue_source if queue_source else LOG_QUEUE
    temp_queue = queue.Queue()
    temp_logs = []


    try:
        while not log_queue.empty():
            log = log_queue.get_nowait()
            temp_logs.append(log)
            temp_queue.put(log)  # 将日志放回临时队列
    except queue.Empty:
        pass

    logs = temp_logs

    if LOG_FILE and os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                all_lines = f.readlines()
                logs = all_lines
        except Exception as e:
            error_msg = f"Error reading log file: {str(e)}"
            logging.error(error_msg)
            if not logs:
                logs = [error_msg]

    if not logs:
        return state, 0


    filtered_logs = []
    for log in logs:
        if "- INFO -" not in log:
            filtered_logs.append(log)

    if not filtered_logs:
        return state, 0

    final_contents, updated_index = parse_logs_incrementally(filtered_logs, state, last_index)

    return final_contents, updated_index



# Dictionary containing module descriptions
MODULE_DESCRIPTIONS = {
    "Detailed Idea Description": "At this level, users provide comprehensive descriptions of their specific research ideas. The system processes these detailed inputs to develop implementation strategies based on the user's explicit requirements. Examples 1-2 are the templates of this mode.",
    "Reference-Based Ideation": "This simpler level involves users submitting reference papers without a specific idea in mind. The user query typically follows the format: "'"I have some reference papers, please come up with an innovative idea and implement it with these papers."'" The system then analyzes the provided references to generate and develop novel research concepts. Examples 3-4 are the templates of this mode.",
    "Paper Generation Agent": "Once all research and experimental work is finished, employ this agent for paper generation",
    # "exit": "exit mode"
}

# 默认环境变量模板
DEFAULT_ENV_TEMPLATE = """#===========================================
# MODEL & API 
# (See https://docs.camel-ai.org/key_modules/models.html#)
#===========================================

# OPENAI API (https://platform.openai.com/api-keys)
OPENAI_API_KEY='Your_Key'
# OPENAI_API_BASE_URL=""

# Azure OpenAI API
# AZURE_OPENAI_BASE_URL=""
# AZURE_API_VERSION=""
# AZURE_OPENAI_API_KEY=""
# AZURE_DEPLOYMENT_NAME=""


# Qwen API (https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key)
QWEN_API_KEY='Your_Key'

# DeepSeek API (https://platform.deepseek.com/api_keys)
DEEPSEEK_API_KEY='Your_Key'

#===========================================
# Tools & Services API
#===========================================

# Google Search API (https://coda.io/@jon-dallas/google-image-search-pack-example/search-engine-id-and-google-api-key-3)
GOOGLE_API_KEY='Your_Key'
SEARCH_ENGINE_ID='Your_ID'

# Chunkr API (https://chunkr.ai/)
CHUNKR_API_KEY='Your_Key'

# Firecrawl API (https://www.firecrawl.dev/)
FIRECRAWL_API_KEY='Your_Key'
#FIRECRAWL_API_URL="https://api.firecrawl.dev"
"""


def validate_input(question: str) -> bool:
    """验证用户输入是否有效

    Args:
        question: 用户问题

    Returns:
        bool: 输入是否有效
    """
    # 检查输入是否为空或只包含空格
    if not question or question.strip() == "":
        return False
    return True


def run_ai_researcher(question: str, reference: str, example_module: str) -> Tuple[str, str, str]:
    global CURRENT_PROCESS

    # 验证输入
    if not validate_input(question):
        logging.warning("User submitted invalid input")
        return ("Please enter a valid question", "0", "❌ Error: Invalid input question")

    try:
        # 确保环境变量已加载
        load_dotenv(find_dotenv(), override=True)
        logging.info(f"Processing question: '{question}', using module: {example_module}")

        # 检查模块是否在MODULE_DESCRIPTIONS中
        if example_module not in MODULE_DESCRIPTIONS:
            logging.error(f"User selected an unsupported module: {example_module}")
            return (
                f"Selected module '{example_module}' is not supported",
                "0",
                "❌ Error: Unsupported module",
            )

 
        # 运行
        try:
            # logging.info("Runing AI Researcher...")
            # answer, chat_history, token_info = run_society(society)
            answer = main_ai_researcher(question, reference, example_module)
            logging.info("Sucessully Runing AI Researcher")
        except Exception as e:
            logging.error(f"Error occurred while running Researcher: {str(e)}")
            return (
                f"Error occurred while running Researcher: {str(e)}",
                "0",
                f"❌ Error: Run failed - {str(e)}",
            )

        token_info = None
        if not isinstance(token_info, dict):
            token_info = {}

        completion_tokens = token_info.get("completion_token_count", 0)
        prompt_tokens = token_info.get("prompt_token_count", 0)
        total_tokens = completion_tokens + prompt_tokens

        logging.info(
            f"Processing completed, token usage: completion={completion_tokens}, prompt={prompt_tokens}, total={total_tokens}"
        )

        return (
            answer,
            f"Completion tokens: {completion_tokens:,} | Prompt tokens: {prompt_tokens:,} | Total: {total_tokens:,}",
            "✅ Successfully completed",
        )

    except Exception as e:
        logging.error(
            f"Uncaught error occurred while processing the question: {str(e)}"
        )
        return (f"Error occurred: {str(e)}", "0", f"❌ Error: {str(e)}")


def update_module_description(module_name: str) -> str:
    return MODULE_DESCRIPTIONS.get(module_name, "No description available")


# 存储前端配置的环境变量
WEB_FRONTEND_ENV_VARS: dict[str, str] = {}


def init_env_file():
    """初始化.env文件如果不存在"""
    dotenv_path = find_dotenv()
    if not dotenv_path:
        with open(".env", "w") as f:
            f.write(DEFAULT_ENV_TEMPLATE)
        dotenv_path = find_dotenv()
    return dotenv_path


def load_env_vars():
    """加载环境变量并返回字典格式

    Returns:
        dict: 环境变量字典，每个值为一个包含值和来源的元组 (value, source)
    """
    dotenv_path = init_env_file()
    load_dotenv(dotenv_path, override=True)

    # 从.env文件读取环境变量
    env_file_vars = {}
    with open(dotenv_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                if "=" in line:
                    key, value = line.split("=", 1)
                    env_file_vars[key.strip()] = value.strip().strip("\"'")

    # 从系统环境变量中获取
    system_env_vars = {
        k: v
        for k, v in os.environ.items()
        if k not in env_file_vars and k not in WEB_FRONTEND_ENV_VARS
    }

    # 合并环境变量，并标记来源
    env_vars = {}

    # 添加系统环境变量（最低优先级）
    for key, value in system_env_vars.items():
        env_vars[key] = (value, "System")

    # 添加.env文件环境变量（中等优先级）
    for key, value in env_file_vars.items():
        env_vars[key] = (value, ".env file")

    # 添加前端配置的环境变量（最高优先级）
    for key, value in WEB_FRONTEND_ENV_VARS.items():
        env_vars[key] = (value, "Frontend configuration")
        # 确保操作系统环境变量也被更新
        os.environ[key] = value

    return env_vars


def save_env_vars(env_vars):
    """保存环境变量到.env文件

    Args:
        env_vars: 字典，键为环境变量名，值可以是字符串或(值,来源)元组
    """
    try:
        dotenv_path = init_env_file()

        # 保存每个环境变量
        for key, value_data in env_vars.items():
            if key and key.strip():  # 确保键不为空
                # 处理值可能是元组的情况
                if isinstance(value_data, tuple):
                    value = value_data[0]
                else:
                    value = value_data

                set_key(dotenv_path, key.strip(), value.strip())

        # 重新加载环境变量以确保生效
        load_dotenv(dotenv_path, override=True)
        global_state.START_FLAG = False
        global_state.FIRST_MAIN = False
        # autoagent_init(container_name, port, test_pull_name, git_clone, local_env, LOG_FILE)

        return True, "Environment variables have been successfully saved!"
    except Exception as e:
        return False, f"Error saving environment variables: {str(e)}"


def add_env_var(key, value, from_frontend=True):
    """添加或更新单个环境变量

    Args:
        key: 环境变量名
        value: 环境变量值
        from_frontend: 是否来自前端配置，默认为True
    """
    try:
        if not key or not key.strip():
            return False, "Variable name cannot be empty"

        key = key.strip()
        value = value.strip()

        # 如果来自前端，则添加到前端环境变量字典
        if from_frontend:
            WEB_FRONTEND_ENV_VARS[key] = value
            # 直接更新系统环境变量
            os.environ[key] = value

        # 同时更新.env文件
        dotenv_path = init_env_file()
        set_key(dotenv_path, key, value)
        load_dotenv(dotenv_path, override=True)

        return True, f"Environment variable {key} has been successfully added/updated!"
    except Exception as e:
        return False, f"Error adding environment variable: {str(e)}"


def delete_env_var(key):
    """删除环境变量"""
    try:
        if not key or not key.strip():
            return False, "Variable name cannot be empty"

        key = key.strip()

        # 从.env文件中删除
        dotenv_path = init_env_file()
        unset_key(dotenv_path, key)

        # 从前端环境变量字典中删除
        if key in WEB_FRONTEND_ENV_VARS:
            del WEB_FRONTEND_ENV_VARS[key]

        # 从当前进程环境中也删除
        if key in os.environ:
            del os.environ[key]

        return True, f"Environment variable {key} has been successfully deleted!"
    except Exception as e:
        return False, f"Error deleting environment variable: {str(e)}"


def is_api_related(key: str) -> bool:
    """判断环境变量是否与API相关

    Args:
        key: 环境变量名

    Returns:
        bool: 是否与API相关
    """
    # API相关的关键词
    api_keywords = [
        "api",
        "key",
        "token",
        "secret",
        "password",
        "openai",
        "qwen",
        "deepseek",
        "google",
        "search",
        "hf",
        "hugging",
        "chunkr",
        "firecrawl",
        "category",
        "instance_id",
        "task_level",
        "container_name",
        "workplace_name",
        "cache_path",
        "port",
        "max_iter_times"
    ]

    # 检查是否包含API相关关键词（不区分大小写）
    return any(keyword in key.lower() for keyword in api_keywords)


def get_api_guide(key: str) -> str:
    """根据环境变量名返回对应的API获取指南

    Args:
        key: 环境变量名

    Returns:
        str: API获取指南链接或说明
    """
    key_lower = key.lower()
    if "openai" in key_lower:
        return "https://platform.openai.com/api-keys"
    elif "qwen" in key_lower or "dashscope" in key_lower:
        return "https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key"
    elif "deepseek" in key_lower:
        return "https://platform.deepseek.com/api_keys"
    elif "google" in key_lower:
        return "https://coda.io/@jon-dallas/google-image-search-pack-example/search-engine-id-and-google-api-key-3"
    elif "search_engine_id" in key_lower:
        return "https://coda.io/@jon-dallas/google-image-search-pack-example/search-engine-id-and-google-api-key-3"
    elif "chunkr" in key_lower:
        return "https://chunkr.ai/"
    elif "firecrawl" in key_lower:
        return "https://www.firecrawl.dev/"
    else:
        return ""


def update_env_table():
    """更新环境变量表格显示，只显示API相关的环境变量"""
    env_vars = load_env_vars()
    # 过滤出API相关的环境变量
    api_env_vars = {k: v for k, v in env_vars.items() if is_api_related(k)}
    # 转换为列表格式，以符合Gradio Dataframe的要求
    # 格式: [变量名, 变量值, 获取指南链接]
    result = []
    for k, v in api_env_vars.items():
        guide = get_api_guide(k)
        # 如果有指南链接，创建一个可点击的链接
        guide_link = (
            f"<a href='{guide}' target='_blank' class='guide-link'>🔗 获取</a>"
            if guide
            else ""
        )
        result.append([k, v[0], guide_link])
    return result


def save_env_table_changes(data):
    """保存环境变量表格的更改

    Args:
        data: Dataframe数据，可能是pandas DataFrame对象

    Returns:
        str: 操作状态信息，包含HTML格式的状态消息
    """
    try:
        logging.info(
            f"Starting to process environment variable table data, type: {type(data)}"
        )

        # 获取当前所有环境变量
        current_env_vars = load_env_vars()
        processed_keys = set()  # 记录已处理的键，用于检测删除的变量

        # 处理pandas DataFrame对象
        import pandas as pd

        if isinstance(data, pd.DataFrame):
            # 获取列名信息
            columns = data.columns.tolist()
            logging.info(f"DataFrame column names: {columns}")

            # 遍历DataFrame的每一行
            for index, row in data.iterrows():
                # 使用列名访问数据
                if len(columns) >= 3:
                    # 获取变量名和值 (第0列是变量名，第1列是值)
                    key = row[0] if isinstance(row, pd.Series) else row.iloc[0]
                    value = row[1] if isinstance(row, pd.Series) else row.iloc[1]

                    # 检查是否为空行或已删除的变量
                    if key and str(key).strip():  # 如果键名不为空，则添加或更新
                        logging.info(f"Processing environment variable: {key} = {value}")
                        add_env_var(key, str(value))
                        processed_keys.add(key)
        # 处理其他格式
        elif isinstance(data, dict):
            logging.info(f"Dictionary format data keys: {list(data.keys())}")
            # 如果是字典格式，尝试不同的键
            if "data" in data:
                rows = data["data"]
            elif "values" in data:
                rows = data["values"]
            elif "value" in data:
                rows = data["value"]
            else:
                # 尝试直接使用字典作为行数据
                rows = []
                for key, value in data.items():
                    if key not in ["headers", "types", "columns"]:
                        rows.append([key, value])

            if isinstance(rows, list):
                for row in rows:
                    if isinstance(row, list) and len(row) >= 2:
                        key, value = row[0], row[1]
                        if key and str(key).strip():
                            add_env_var(key, str(value))
                            processed_keys.add(key)
        elif isinstance(data, list):
            # 列表格式
            for row in data:
                if isinstance(row, list) and len(row) >= 2:
                    key, value = row[0], row[1]
                    if key and str(key).strip():
                        add_env_var(key, str(value))
                        processed_keys.add(key)
        else:
            logging.error(f"Unknown data format: {type(data)}")
            return f"❌ Save failed: Unknown data format {type(data)}"

        # 处理删除的变量 - 检查当前环境变量中是否有未在表格中出现的变量
        api_related_keys = {k for k in current_env_vars.keys() if is_api_related(k)}
        keys_to_delete = api_related_keys - processed_keys

        # 删除不在表格中的变量
        for key in keys_to_delete:
            logging.info(f"Deleting environment variable: {key}")
            delete_env_var(key)

        return "✅ Environment variables have been successfully saved"
    except Exception as e:
        import traceback

        error_details = traceback.format_exc()
        logging.error(f"Error saving environment variables: {str(e)}\n{error_details}")
        return f"❌ Save failed: {str(e)}"


def get_env_var_value(key):
    """获取环境变量的实际值

    优先级：前端配置 > .env文件 > 系统环境变量
    """
    # 检查前端配置的环境变量
    if key in WEB_FRONTEND_ENV_VARS:
        return WEB_FRONTEND_ENV_VARS[key]

    # 检查系统环境变量（包括从.env加载的）
    return os.environ.get(key, "")


def create_ui():

    def clear_log_file():
        """清空日志文件内容"""
        try:
            if LOG_FILE and os.path.exists(LOG_FILE):
                # 清空日志文件内容而不是删除文件
                open(LOG_FILE, "w").close()
                logging.info("Log file has been cleared")
                # 清空日志队列
                while not LOG_QUEUE.empty():
                    try:
                        LOG_QUEUE.get_nowait()
                    except queue.Empty:
                        break
                return ""
            else:
                return ""
        except Exception as e:
            logging.error(f"Error clearing log file: {str(e)}")
            return ""

    # 创建一个实时日志更新函数
    def process_with_live_logs(question, reference, module_name, state, last_index):
        """处理问题并实时更新日志"""
        global CURRENT_PROCESS

        result_queue = queue.Queue()

        def process_in_background():
            try:
                result = run_ai_researcher(question, reference, module_name)
                result_queue.put(result)
            except Exception as e:
                result_queue.put(
                    (f"Error occurred: {str(e)}", "0", f"❌ Error: {str(e)}")
                )

        # 过滤空内容的对话记录
        def filter_empty_conversations(conversations):
            """过滤掉完全空的对话记录，并处理部分空内容"""
            filtered = []
            for user_msg, bot_msg in conversations:
                # 检查是否两者都为空
                user_empty = not user_msg.strip()
                bot_empty = not bot_msg.strip()
                
                # 如果两者都为空，则跳过这个对话记录
                if user_empty and bot_empty:
                    continue
                
                # 如果只有一个为空，保留非空的那个，空的用None替代
                processed_user = user_msg if not user_empty else None
                processed_bot = bot_msg if not bot_empty else None
                
                filtered.append((processed_user, processed_bot))
            return filtered

        # 启动后台处理线程
        bg_thread = threading.Thread(target=process_in_background)
        CURRENT_PROCESS = bg_thread  # 记录当前进程
        bg_thread.start()
        # scroll_script = "<script>scrollToBottom();</script>"
        # scroll_script = "<script>document.getElementById('top')?.scrollIntoView();</script>"
        # scroll_script = "<script>document.getElementById('down').scrollTop = document.getElementById('chat-log').scrollHeight;</script>"
        scroll_script = None



        # 在等待处理完成的同时，每秒更新一次日志
        while bg_thread.is_alive():
            # 更新对话记录显示
            logs2, updated_index = get_latest_logs(500, state, LOG_QUEUE, last_index)
            # 过滤空内容的对话记录
            filtered_logs = filter_empty_conversations(logs2)
            # scroll_script = "<script>scrollToBottom();</script>"
            # 始终更新状态
            yield (
                state,
                "<span class='status-indicator status-running'></span> Processing...",
                filtered_logs,
                scroll_script, 
                updated_index
            )

            time.sleep(1)

        # 处理完成，获取结果
        if not result_queue.empty():
            result = result_queue.get()
            answer, token_count, status = result

            # 最后一次更新对话记录
            logs2, updated_index = get_latest_logs(500, state, LOG_QUEUE, last_index)
            # 过滤空内容的对话记录
            filtered_logs = filter_empty_conversations(logs2)

            # 根据状态设置不同的指示器
            if "错误" in status:
                status_with_indicator = (
                    f"<span class='status-indicator status-error'></span> {status}"
                )
            else:
                status_with_indicator = (
                    f"<span class='status-indicator status-success'></span> {status}"
                )

            yield token_count, status_with_indicator, filtered_logs, scroll_script, updated_index
            # yield token_count, status_with_indicator, logs2
        else:
            logs2, updated_index = get_latest_logs(500, state, LOG_QUEUE, last_index)
            # 过滤空内容的对话记录
            filtered_logs = filter_empty_conversations(logs2)
            yield (
                state,
                "<span class='status-indicator status-error'></span> Terminated",
                filtered_logs,
                None, 
                updated_index
            )

    with gr.Blocks(theme=gr.themes.Soft(primary_hue="amber")) as app:
    #     gr.HTML("""
    #             <script>
    #             function scrollToBottom() {
    #                 const chatLog = document.getElementById('chat-log');
    #                 if (chatLog) {
    #                     chatLog.scrollTop = chatLog.scrollHeight;
    #                 }
    #             }
    #             </script>
    #             """)


        image_base64 = get_base64_image("assets/logo.png")

        gr.HTML(
            f"""
            <div style="display: flex; align-items: center; gap: 16px;">
                <img src="{image_base64}" alt="模型图片" style="width: 100px; height: auto;">
                <div style="display: flex; flex-direction: column;">
                    <h2 style="margin: 0;">AI-Researcher: Autonomous Scientific Innovation</h2>
                    <br>
                    <p style="margin: 0;">Welcome to AI-Researcher🤗 AI-Researcher introduces a revolutionary breakthrough in Automated</p>
                    <p style="margin: 0;">Scientific Discovery🔬, presenting a new system that fundamentally Reshapes the Traditional Research Paradigm.</p>
                </div>
            </div>
            """
        )



        # 添加自定义CSS
        gr.HTML("""
            <style>
            /* 聊天容器样式 */

            body, html, * {
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            }
                
            .chat-container .chatbot {
                height: 500px;
                overflow-y: auto;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }

            /* 减少聊天消息间距 */
            .chatbot .message {
                margin-bottom: 8px !important;
                padding: 8px 12px !important;
            }

            .chatbot .message-row {
                margin-bottom: 8px !important;
                gap: 8px !important;
            }

            .chatbot .message-bubble-border {
                margin-bottom: 6px !important;
            }

            .chatbot .message-bubble {
                margin-bottom: 6px !important;
                padding: 10px 14px !important;
            }

            /* 减少markdown标题间距 */
            .chatbot h3 {
                margin-top: 8px !important;
                margin-bottom: 6px !important;
                line-height: 1.3 !important;
            }

            .chatbot h4, .chatbot h5, .chatbot h6 {
                margin-top: 6px !important;
                margin-bottom: 4px !important;
                line-height: 1.2 !important;
            }

            /* 减少段落间距 */
            .chatbot p {
                margin-bottom: 8px !important;
                line-height: 1.4 !important;
            }

            /* 为用户内容代码块添加特殊样式 */
            .chatbot .message-bubble:has(h3:contains("🙋 User")) pre {
                max-height: 200px !important;
                overflow-y: auto !important;
                border: 1px solid #e0e0e0 !important;
                border-radius: 6px !important;
                padding: 12px !important;
                background-color: #f8f9fa !important;
            }

            /* 通用代码块样式 - 限制高度并支持滚动 */
            .chatbot pre {
                max-height: 250px !important;
                overflow-y: auto !important;
                border: 1px solid #e0e0e0 !important;
                border-radius: 6px !important;
                padding: 12px !important;
                background-color: #f8f9fa !important;
                font-family: 'Courier New', Consolas, monospace !important;
                font-size: 0.9em !important;
                line-height: 1.4 !important;
            }

            /* 为markdown代码块添加滚动条样式 */
            .chatbot pre::-webkit-scrollbar {
                width: 8px !important;
            }

            .chatbot pre::-webkit-scrollbar-track {
                background: #f1f1f1 !important;
                border-radius: 4px !important;
            }

            .chatbot pre::-webkit-scrollbar-thumb {
                background: #c1c1c1 !important;
                border-radius: 4px !important;
            }

            .chatbot pre::-webkit-scrollbar-thumb:hover {
                background: #a8a8a8 !important;
            }

            /* 减少列表间距 */
            .chatbot ul, .chatbot ol {
                margin-bottom: 8px !important;
                padding-left: 20px !important;
            }

            .chatbot li {
                margin-bottom: 2px !important;
            }

            /* 改进标签页样式 */
            .tabs .tab-nav {
                background-color: #f5f5f5;
                border-radius: 8px 8px 0 0;
                padding: 5px;
            }

            .tabs .tab-nav button {
                border-radius: 5px;
                margin: 0 3px;
                padding: 8px 15px;
                font-weight: 500;
            }

            .tabs .tab-nav button.selected {
                background-color: #FFA500;
                color: white;
            }
            
            /* input 范围限定 */
            .scrolling-textbox textarea {
                max-height: 300px !important;  /* 设置最大高度 */
                overflow-y: auto !important;  /* 垂直滚动 */
            }
            
            /* example 范围限定 */
            .scrolling-example {
                max-width: 100%;
                overflow-x: auto;
                white-space: nowrap;
            }
            .scrolling-example button {
                display: inline-block;
                max-width: 100%;
                text-overflow: ellipsis;
                overflow: hidden;
                white-space: nowrap;
            }

            /* 状态指示器样式 */
            .status-indicator {
                display: inline-block;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                margin-right: 5px;
            }

            .status-running {
                background-color: #ffc107;
                animation: pulse 1.5s infinite;
            }

            .status-success {
                background-color: #28a745;
            }

            .status-error {
                background-color: #dc3545;
            }

            /* 日志显示区域样式 */
            .log-display textarea {
                height: 400px !important;
                max-height: 400px !important;
                overflow-y: auto !important;
                font-family: monospace;
                font-size: 0.9em;
                white-space: pre-wrap;
                line-height: 1.4;
            }

            .log-display {
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
                min-height: 100vh;
                max-height: 120vh;
            }

            /* 环境变量管理样式 */
            .env-manager-container {
                border-radius: 10px;
                padding: 15px;
                background-color: #FFD580;
                margin-bottom: 20px;
            }

            .env-controls, .api-help-container {
                border-radius: 8px;
                padding: 15px;
                background-color: white;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
                height: 100%;
            }

            .env-add-group, .env-delete-group {
                margin-top: 20px;
                padding: 15px;
                border-radius: 8px;
                background-color: #f5f8ff;
                border: 1px solid #e0e8ff;
            }

            .env-delete-group {
                background-color: #fff5f5;
                border: 1px solid #ffe0e0;
            }

            .env-buttons {
                justify-content: flex-start;
                gap: 10px;
                margin-top: 10px;
            }

            .env-button {
                min-width: 100px;
            }

            .delete-button {
                background-color: #dc3545;
                color: white;
            }

            .env-table {
                margin-bottom: 15px;
            }

            /* 改进环境变量表格样式 */
            .env-table table {
                border-collapse: separate;
                border-spacing: 0;
                width: 100%;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }

            .env-table th {
                background-color: #FFD580;
                padding: 12px 15px;
                text-align: left;
                font-weight: 600;
                color: #FFA500;
                border-bottom: 2px solid #FFD580;
            }

            .env-table td {
                padding: 10px 15px;
                border-bottom: 1px solid #f0f0f0;
            }

            .env-table tr:hover td {
                background-color: #FFA500;
            }

            .env-table tr:last-child td {
                border-bottom: none;
            }

            /* 状态图标样式 */
            .status-icon-cell {
                text-align: center;
                font-size: 1.2em;
            }

            /* 链接样式 */
            .guide-link {
                color: #FF8C00;
                text-decoration: none;
                cursor: pointer;
                font-weight: 500;
            }

            .guide-link:hover {
                text-decoration: underline;
            }

            .env-status {
                margin-top: 15px;
                font-weight: 500;
                padding: 10px;
                border-radius: 6px;
                transition: all 0.3s ease;
            }

            .env-status-success {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }

            .env-status-error {
                background-color: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }

            .api-help-accordion {
                margin-bottom: 8px;
                border-radius: 6px;
                overflow: hidden;
            }
         
            .custom-file .gr-file-box {
                height: 4px !important;
                max-height: 4px !important;
                padding: 4px !important;
            }



            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
            body, html {
                background-color: #FFF7ED !important;  /* ✅ 页面整体背景 */
            }
            </style>
            """)

        with gr.Row():
            with gr.Column(scale=0.5):
                question_input = gr.Textbox(
                    lines=5,
                    max_lines=10,
                    placeholder="Please enter your questions...",
                    label="Prompt",
                    elem_id="question_input",
                    show_copy_button=True,
                    # elem_classes="scrolling-textbox",
                    value="Write a hello world python file and save it in local file",
                )

                reference_input = gr.Textbox(
                    lines=5,
                    max_lines=10,
                    placeholder="Please enter your reference papers...",
                    label="Reference",
                    elem_id="reference_input",
                    show_copy_button=True,
                    # elem_classes="scrolling-textbox",
                    value="1. Attention is all you need. ",
                )

                # 增强版模块选择下拉菜单
                # 只包含MODULE_DESCRIPTIONS中定义的模块
                module_dropdown = gr.Dropdown(
                    choices=list(MODULE_DESCRIPTIONS.keys()),
                    value="Detailed Idea Description",
                    label="Select Mode",
                    interactive=True,
                )

                # 模块描述文本框
                module_description = gr.Textbox(
                    lines=3,
                    max_lines=5,
                    value=MODULE_DESCRIPTIONS["Detailed Idea Description"],
                    label="Mode Description",
                    interactive=False,
                    elem_classes="module-info",
                )

                with gr.Row():
                    run_button = gr.Button(
                        "Run", variant="primary", elem_classes="primary"
                    )

                status_output = gr.HTML(
                    value="<span class='status-indicator status-success'></span> Ready",
                    label="状态",
                )
                # token_count_output = gr.Textbox(
                #     label="令牌计数", interactive=False, elem_classes="token-count"
                # )

                # 示例问题
                examples = [
                    # [
                    #     "1. **Task**: The proposed model is designed to address representation collapse in Vector Quantized (VQ) models, specifically in unsupervised representation learning and latent generative models applicable to modalities like image and audio data.\n\n2. **Core Techniques/Algorithms**: The methodology introduces a linear transformation layer applied to the code vectors in a reparameterization strategy that leverages a learnable latent basis, enhancing the optimization of the entire codebook rather than individual code vectors.\n\n3. **Purpose and Function of Major Technical Components**:\n   - **Encoder (f_θ)**: Maps input data (images or audio) into a continuous latent representation (z_e).\n   - **Codebook (C)**: A collection of discrete code vectors used for quantizing the latent representations.\n   - **Linear Transformation Layer (W)**: A learnable matrix that transforms the codebook vectors, optimizing the entire latent space jointly to improve codebook utilization during training.\n   - **Decoder (g_ϕ)**: Reconstructs the input data from the quantized representations.\n\n4. **Implementation Details**:\n   - **Key Parameters**:\n     - Learning rate (η): Commonly set to 1e-4.\n     - Commitment weight (β): Adjust according to data modality, e.g., set to 1.0 for images and 1000.0 for audio.\n   - **Input/Output Specifications**:\n     - **Input**: Raw data instances, such as images of size 128x128 or audio frames. \n     - **Output**: Reconstructed data (images or audio).\n   - **Important Constraints**: The codebook size should be large enough to capture the data complexity; experiments indicate sizes like 65,536 or larger are beneficial.\n\n5. **Step-by-Step Description of Component Interaction**:\n   - **Step 1**: Initialize the codebook (C) using a distribution (e.g., Gaussian) and freeze its parameters for initial training iterations.\n   - **Step 2**: For each data instance (x), compute the latent representation (z_e) using the encoder (f_θ).\n   - **Step 3**: Perform nearest code search to find the closest codebook vector to z_e using the distance metric. Use the selected code vector for reconstruction.\n   - **Step 4**: Reparameterize the selected code vector using the performed linear transformation (C * W), effectively treating both C and W in the optimization process.\n   - **Step 5**: Calculate the loss, which combines reconstruction loss (MSE between original and decoded output) and commitment loss to ensure effective use of the codebook.\n   - **Step 6**: Update only the linear layer (W) through gradient backpropagation, keeping C static throughout this phase to facilitate the joint training procedure.\n\n6. **Critical Implementation Details**:\n   - To prevent representation collapse, it is crucial to carefully set the learning rate so that the transformation matrix W can adapt without compromising the usefulness of the latent space.\n   - Keeping the codebook static during the initial phase speeds up the convergence while ensuring that the linear transformation can stretch and rotate the latent space effectively.\n   - Regularly evaluate the utilization percentage of the codebook during training iterations, aiming for near-complete usage (ideally 100%) to combat representation collapse actively.",

                    #     "Title: Neural discrete representation learning; You can use this paper in the following way: The core VQ method proposed in this study is directly utilized in the proposed model, providing the essential framework for vector quantization.\nTitle: Vector-quantized image modeling with improved VQGAN; You can use this paper in the following way: The improved VQGAN methodology is built upon to develop the proposed model, particularly in optimizing codebook utilization without sacrificing model capacity.\nTitle: Taming transformers for high-resolution image synthesis; You can use this paper in the following way: VQGAN serves as a foundational model that the proposed model builds upon, especially in terms of integrating adversarial techniques to improve latent space optimization.\nTitle: Estimating or propagating gradients through stochastic neurons for conditional computation; You can use this paper in the following way: STE is employed in this study to facilitate gradient descent updates for the codebook vectors, ensuring effective training of the proposed model despite the discrete quantization step.\nTitle: Learning transferable visual models from natural language supervision.; You can use this paper in the following way: VQGAN-LC, as proposed in this study, is used as a comparative baseline to highlight the limitations of relying on pre-trained models for codebook initialization.\nTitle: Finite scalar quantization: VQ-VAE made simple.; You can use this paper in the following way: FSQ is evaluated as an existing method for mitigating representation collapse. The proposed model is proposed as a superior alternative that avoids the dimensionality reduction inherent in FSQ.\nTitle: Auto-encoding variational bayes.; You can use this paper in the following way: Conceptual insights from VAEs are used to theoretically analyze the representation collapse problem in VQ models, highlighting the differences in optimization strategies between VAEs and the proposed approach.\nTitle: Categorical reparameterization with gumbel-softmax.; You can use this paper in the following way: The Gumbel-Softmax technique is discussed as part of alternative quantization strategies, informing the development of the proposed model's approach to optimizing the latent space."
                    # ],

                    [
                        "1. The proposed model designed in this paper is designed to improve the performance of Vector Quantized Variational AutoEncoders (VQ-VAEs) by addressing issues with gradient propagation through the non-differentiable vector quantization layer.\n\n2. The core methodologies utilized include:\n   - **Rotation and Rescaling Transformation**: A linear transformation that alters the encoder output to align it with the nearest codebook vector without changing the forward pass output.\n   - **Gradient Propagation Method**: The proposed model ensures that gradients flow from the decoder to the encoder while preserving the angle between the gradient and codebook vector.\n   - **Codebook Management**: Utilizes the connection between the encoder output and the corresponding codebook vectors to mitigate codebook collapse and improve utilization.\n\n3. The primary functions of these components are:\n   - The rotation and rescaling transformation modifies how the encoder output is quantized and how information is retained during backpropagation, enabling gradients to reflect the true positioning of the encoder output relative to the codebook vectors.\n   - The gradient propagation method redefines how gradients are transported back to the encoder, allowing for an enhanced and nuanced movement through the quantization layer, which leads to a better performance during training.\n   - Codebook management practices help in maintaining a diverse set of codebook vectors throughout training, avoiding scenarios where multiple vectors become redundant or unused.\n\n4. Implementation details for each component:\n   - **Key Parameters**: \n     - Codebook size should be configured based on the complexity of the dataset (e.g., 1024 or 8192).\n     - Commitment loss coefficient (\u03b2) is typically set within [0.25, 2].\n   - **Input/Output Specifications**: \n     - Input to the encoder is a continuous high-dimensional vector, while the output is a corresponding quantized vector from the codebook.\n     - The output for reconstruction is generated using the decoder applied to the transformed codebook vectors.\n   - **Important Constraints**: \n     - Ensure that the codebook is updated correctly with an exponential moving average procedure, and treat both rotation and rescaling during the forward pass as constants with respect to the gradient.\n\n5. Step-by-Step Integration of Components:\n   - **Step 1**: Input the data vector into the encoder to obtain the continuous representation.\n   - **Step 2**: Identify the nearest codebook vector to the encoder output.\n   - **Step 3**: Compute the rotation matrix that aligns the encoder output to the codebook vector.\n   - **Step 4**: Apply the rotation and rescaling transformation to obtain the modified output for the decoder (i.e., `\u02dc q`).\n   - **Step 5**: Feed `\u02dc q` into the decoder to produce the reconstructed output.\n   - **Step 6**: Compute the loss using the reconstruction and apply backpropagation.\n   - **Step 7**: During backpropagation, modify the gradient transfer process to maintain the angle using the proposed model, replacing traditional shortcuts in gradient computation.\n\n6. Critical implementation details affecting performance:\n   - The choice of rotation matrix calculation should ensure computational efficiency\u2014using Householder transformations to minimize resource demands.\n   - The deployment of the stop-gradient technique effectively turns off the back-propagation through the quantization layer, which is essential to reflect the intended change without inducing undesired noise in the gradient updates.\n   - Monitor the codebook usage regularly during training to detect any potential collapse early and adjust the training dynamics (e.g., learning rate) accordingly to maintain effective utilization throughout the training period.",

                        "1. Title: Neural discrete representation learning; The proposed model proposed in this paper restructures the gradient propagation through the vector quantization layer of VQ-VAEs, directly building upon the foundational methods established in this study.\n\n2. Title: Straightening out the straight-through estimator: Overcoming optimization challenges in vector quantized networks; The proposed model is proposed as an improvement over the STE, aiming to preserve more gradient information and enhance codebook utilization, thereby overcoming the optimization challenges highlighted in this paper.\n\n3. Title: Estimating or propagating gradients through stochastic neurons for conditional computation; The STE method introduced in this paper serves as the baseline approach that the proposed model aims to improve upon, offering a more nuanced gradient propagation mechanism.\n\n4. Title: High-resolution image synthesis with latent diffusion models; The proposed model is evaluated on VQGANs as utilized in latent diffusion models presented in this study, showcasing significant improvements in reconstruction metrics and codebook utilization.\n\n5. Title: Finite scalar quantization: Vq-vae made simple; By introducing the proposed approach, this study provides an alternative to the methods discussed in this paper, further enhancing training stability and performance in VQ-VAEs.\n\n6. Title: Elements of information theory; The current paper references information theory concepts from this study to explain the importance of low quantization error and high codebook utilization in vector quantization.\n\n7. Title: Vector-quantized image modeling with improved vqgan; The proposed approach is applied to VQGANs as discussed in this study, resulting in improved reconstruction metrics and more efficient codebook usage.\n\n8. Title: Uvim: A unified modeling approach for vision with learned guiding codes; The proposed approach builds upon the vector quantization methodologies discussed in this study, aiming to enhance codebook utilization and gradient efficiency.\n\n9. Title: Auto-encoding variational bayes; The loss function for VQ-VAEs used in the proposed approach follows the ELBO conventions set forth in this study.\n\n10. Title: Categorical reparameterization with gumbel-softmax; The Gumbel-Softmax trick is discussed as one of the methods to sidestep the STE in vector quantization, providing context for the advantages offered by the proposed model."
                    ],

                    [
                        "gnn",

                        "Title: Graph Neural Networks: A Review of Methods and Applications; You can use this paper in the following way: Core methodologies of GNNs were integrated into the proposed model framework to enhance understanding of graph data.\nTitle: Deep Graph Infomax; You can use this paper in the following way: The DGI approach was used to enhance self-supervision in the instruction tuning of the proposed model.\nTitle: Semi-Supervised Classification with Graph Convolutional Networks; You can use this paper in the following way: The concepts from GCNs were adapted for improving generalization in zero-shot learning scenarios.\nTitle: Attention is All You Need; You can use this paper in the following way: Self-attention principles were utilized in the proposed model to effectively manage graph structural information.\nTitle: Graph Attention Networks; You can use this paper in the following way: Attention mechanisms from GATs were integrated to enhance the proposed model's performance on graph tasks.\nTitle: BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding; You can use this paper in the following way: BERT's architecture was adapted for encoding text in relation to graph data.\nTitle: Learning Transferable Visual Models From Natural Language Supervision; You can use this paper in the following way: The design of self-supervised instruction tuning in the proposed model was influenced by the methodologies proposed in this paper.\nTitle: Gpt-gnn: Generative pre-training of graph neural networks; You can use this paper in the following way: The generative pre-training concepts informed the development of the proposed model's learning strategies."
                    ],

                    [
                        "diffu_flow",

                        "Title: Denoising diffusion probabilistic models; You can use this paper in the following way: Used as a foundational reference for the denoising processes and model architecture.\nTitle: Generative adversarial nets; You can use this paper in the following way: Referenced for underlying generative capabilities which influenced our proposed model design.\nTitle: Image-noise Optimal Transport in Generative Models; You can use this paper in the following way: Served as a framework for understanding and applying transport concepts to the proposed model.\nTitle: Improving consistency models with generator-induced coupling; You can use this paper in the following way: Detailed analysis of generator behaviors informed our component enhancements.\nTitle: Conditional wasser- stein distances with applications in bayesian ot flow matching; You can use this paper in the following way: Informed the adjustments made in our distance evaluation framework.\nTitle: Imagenet: A large-scale hierarchical image database; You can use this paper in the following way: Utilized CIFAR-10 as a benchmark derived from this foundational work."
                    ]
                ]

                with gr.Row(elem_classes="scrolling-example"):
                    gr.Examples(examples=examples, inputs=[question_input, reference_input])

                gr.Markdown("""
                ### Example Description：
                1️⃣ Examples 1-2: For **Detailed Idea Description** Mode <br>
                2️⃣ Examples 3-4: For **Reference-Based Ideation** Mode <br>
                3️⃣ In Reference-Based Ideation mode, the Question can be a category <br>
                (existing categories: gnn, diffu_flow, reasoning, recommendation, vq). <br>
                Also you can design other category like metaprompt.py
                """)

                gr.HTML("""
                        <div class="footer" id="about">
                            <h3>AI-Researcher: Autonomous Scientific Innovation</h3>
                            <p>© 2025 HKUDS. MIT license <a href="https://github.com/HKUDS/AI-Researcher" target="_blank">GitHub</a></p>
                        </div>
                    """)

            with gr.Tabs():  # 设置对话记录为默认选中的标签页
                with gr.TabItem("Conversation Record"):
                    # 添加对话记录显示区域
                    with gr.Group():
                        log_display2 = gr.Chatbot(
                            # value="No conversation records yet.",
                            elem_id="chat-log",  # 添加 ID，供 JS 使用
                            elem_classes="log-display"
                        )

                        state = gr.State([])
                        last_index = gr.State(0)
                        scroll_trigger = gr.HTML("", visible=False)

                    with gr.Row():
                        # clear_logs_button2 = gr.Button("Clear Record", variant="secondary")
                        download_research_logs = gr.Button("Extract research log files")
                        download_paper_logs = gr.Button("Extract paper log files")
                        download_paper = gr.Button("Extract paper")
                        file_output = gr.File(label="click to download", elem_classes="custom-file")

                with gr.TabItem("Environment Variable Management", id="env-settings"):
                    with gr.Group(elem_classes="env-manager-container"):
                        gr.Markdown("""
                            ## Environment Variable Management

                            Set model API keys and other service credentials here. This information will be saved in a local `.env` file, ensuring your API keys are securely stored and not uploaded to the network. Correctly setting API keys is crucial for the functionality of our system. Environment variables can be flexibly configured according to tool requirements.
                            """)

                        # 主要内容分为两列布局
                        with gr.Row():
                            # 左侧列：环境变量管理控件
                            with gr.Column(scale=3):
                                with gr.Group(elem_classes="env-controls"):
                                    # 环境变量表格 - 设置为可交互以直接编辑
                                    gr.Markdown("""
                                    <div style="background-color: #e7f3fe; border-left: 6px solid #2196F3; padding: 10px; margin: 15px 0; border-radius: 4px;">
                                      <strong>Tip:</strong> Please make sure to run cp .env_template .env to create a local .env file, and flexibly configure the required environment variables according to the running module
                                    </div>
                                    """)

                                    # Enhanced environment variable table, supporting adding and deleting rows
                                    env_table = gr.Dataframe(
                                        headers=[
                                            "Variable Name",
                                            "Value",
                                            "Retrieval Guide",
                                        ],
                                        datatype=[
                                            "str",
                                            "str",
                                            "html",
                                        ],  # Set the last column as HTML type to support links
                                        row_count=10,  # Increase row count to allow adding new variables
                                        col_count=(3, "fixed"),
                                        value=update_env_table,
                                        label="API Keys and Environment Variables",
                                        interactive=True,  # Set as interactive, allowing direct editing
                                        elem_classes="env-table",
                                    )

                                    # Operation instructions
                                    gr.Markdown(
                                        """
                                    <div style="background-color: #fff3cd; border-left: 6px solid #ffc107; padding: 10px; margin: 15px 0; border-radius: 4px;">
                                    <strong>Operation Guide</strong>:
                                    <ul style="margin-top: 8px; margin-bottom: 8px;">
                                      <li><strong>Edit Variable</strong>: Click directly on the "Value" cell in the table to edit</li>
                                      <li><strong>Add Variable</strong>: Enter a new variable name and value in a blank row</li>
                                      <li><strong>Delete Variable</strong>: Clear the variable name to delete that row</li>
                                      <li><strong>Get API Key</strong>: Click on the link in the "Retrieval Guide" column to get the corresponding API key</li>
                                    </ul>
                                    </div>
                                    """,
                                        elem_classes="env-instructions",
                                    )

                                    # Environment variable operation buttons
                                    with gr.Row(elem_classes="env-buttons"):
                                        save_env_button = gr.Button(
                                            "💾 Save Changes",
                                            variant="primary",
                                            elem_classes="env-button",
                                        )
                                        refresh_button = gr.Button(
                                            "🔄 Refresh List", elem_classes="env-button"
                                        )

                                    # Status display
                                    env_status = gr.HTML(
                                        label="Operation Status",
                                        value="",
                                        elem_classes="env-status",
                                    )

                    save_env_button.click(
                        fn=save_env_table_changes,
                        inputs=[env_table],
                        outputs=[env_status],
                    ).then(fn=update_env_table, outputs=[env_table])

                    refresh_button.click(fn=update_env_table, outputs=[env_table])


        run_button.click(
            fn=process_with_live_logs,
            inputs=[question_input, reference_input, module_dropdown, state, last_index],
            # outputs=[token_count_output, status_output, log_display2, scroll_trigger],
            outputs=[state, status_output, log_display2, scroll_trigger, last_index],
        )

        module_dropdown.change(
            fn=update_module_description,
            inputs=module_dropdown,
            outputs=module_description,
        )
        download_research_logs.click(fn=return_log_file, outputs=file_output)
        download_paper_logs.click(fn=return_log_file, outputs=file_output)
        download_paper.click(fn=return_paper_file, outputs=file_output)

        # clear_logs_button2.click(fn=clear_log_file, outputs=[log_display2])

        def toggle_auto_refresh(enabled):
            if enabled:
                return gr.update(every=3)
            else:
                return gr.update(every=0)

    return app


def main():
    try:
        global LOG_FILE
        global LOG_READ_FILE
        # global PAPER_LOG
        LOG_FILE = setup_logging()
        # PAPER_LOG = return_paper_log()
        LOG_READ_FILE = setup_path()
        # logging.info("AutoAgent Web application is running")

        log_thread = threading.Thread(
            target=log_reader_thread, args=(LOG_FILE,), daemon=True
        )
        log_thread.start()
        logging.info("Log reading thread started")

        init_env_file()
        app = create_ui()

        app.queue()
        allowed_paths = [os.path.dirname(LOG_FILE)]
        app.launch(
            share=False, 
            server_port=7039,
            server_name="127.0.0.1",
            allowed_paths=allowed_paths,
            show_error=True,
            quiet=False,
            favicon_path="assets/logo.png"
        )

    except Exception as e:
        logging.error(f"Error occurred while starting the application: {str(e)}")
        print(f"Error occurred while starting the application: {str(e)}")
        import traceback

        traceback.print_exc()

    finally:
        STOP_LOG_THREAD.set()
        STOP_REQUESTED.set()
        logging.info("Application closed")


if __name__ == "__main__":
    main()
