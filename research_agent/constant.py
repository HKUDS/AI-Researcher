import os
from dotenv import load_dotenv
import global_state

load_dotenv()  # 加载.env文件
# utils: 
def str_to_bool(value):
    """convert string to bool"""
    true_values = {'true', 'yes', '1', 'on', 't', 'y'}
    false_values = {'false', 'no', '0', 'off', 'f', 'n'}
    
    if isinstance(value, bool):
        return value
        
    if not value:
        return False
        
    value = str(value).lower().strip()
    if value in true_values:
        return True
    if value in false_values:
        return False
    return True  # default return True

# platform of the research agent
PLATFORM = os.getenv('PLATFORM', "linux/amd64")

DOCKER_WORKPLACE_NAME = os.getenv('DOCKER_WORKPLACE_NAME', 'workplace_meta')
GITHUB_AI_TOKEN = os.getenv('GITHUB_AI_TOKEN', None)
AI_USER = os.getenv('AI_USER', "ai-sin")
LOCAL_ROOT = os.getenv('LOCAL_ROOT', os.getcwd())

DEBUG = str_to_bool(os.getenv('DEBUG', True))

DEFAULT_LOG = str_to_bool(os.getenv('DEFAULT_LOG', True))
LOG_PATH = os.getenv('LOG_PATH', None)
LOG_PATH = global_state.LOG_PATH
EVAL_MODE = str_to_bool(os.getenv('EVAL_MODE', False))
BASE_IMAGES = os.getenv('BASE_IMAGES', "tjbtech1/paperapp:latest")

COMPLETION_MODEL = os.getenv('COMPLETION_MODEL', "gpt-4o-2024-08-06") # gpt-4o-2024-08-06
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', "text-embedding-3-small")
CHEEP_MODEL = os.getenv('CHEEP_MODEL', "gpt-4o-mini-2024-07-18")
# BASE_URL = os.getenv('BASE_URL', None)

# GPUS = os.getenv('GPUS', "all")
GPUS = os.getenv('GPUS', None)

FN_CALL = str_to_bool(os.getenv('FN_CALL', True))
API_BASE_URL = os.getenv('API_BASE_URL', None)
ADD_USER = str_to_bool(os.getenv('ADD_USER', False))

NON_FN_CALL = str_to_bool(os.getenv('NON_FN_CALL', False))

NOT_SUPPORT_SENDER = ["mistral", "groq"]


MUST_ADD_USER = ["deepseek/deepseek-reasoner", "o1-mini"]
NOT_SUPPORT_FN_CALL = ["o1-mini", "deepseek/deepseek-reasoner"]
NOT_USE_FN_CALL = [ "deepseek/deepseek-chat"] + NOT_SUPPORT_FN_CALL

if EVAL_MODE:
    DEFAULT_LOG = False

# if "deepseek" in COMPLETION_MODEL:
#     os.environ["http_proxy"] = "http://127.0.0.1:7890"
#     os.environ["https_proxy"] = "http://127.0.0.1:7890"


