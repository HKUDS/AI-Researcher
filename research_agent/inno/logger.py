from datetime import datetime
from rich.console import Console
from rich.markup import escape
import json
from typing import List
from research_agent.constant import DEBUG, DEFAULT_LOG, LOG_PATH
from pathlib import Path
BAR_LENGTH = 60
class MetaChainLogger:
    def __init__(self, log_path: str):
        self.log_path = log_path
        self.console = Console()
        self.debug = DEBUG
        
    def _write_log(self, message: str):
        with open(self.log_path, 'a') as f:
            f.write(message + '\n')
    def _warp_args(self, args_dict: str):
        args_dict = json.loads(args_dict)
        args_str = ''
        for k, v in args_dict.items():
            args_str += f"{repr(k)}={repr(v)}, "
        return args_str[:-2]
    def _wrap_title(self, title: str, color: str = None):
        single_len = (BAR_LENGTH - len(title)) // 2
        color_bos = f"[{color}]" if color else ""
        color_eos = f"[/{color}]" if color else ""
        return f"{color_bos}{'*'*single_len} {title} {'*'*single_len}{color_eos}"
    def info(self, *args: str, **kwargs: dict):
        # console = Console()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = "\n".join(map(str, args))
        color = kwargs.get("color", "white")
        title = kwargs.get("title", "INFO")
        log_str = f"[{timestamp}]\n{message}"
        if self.debug: 
            # print_in_box(log_str, color=color, title=title)
            self.console.print(self._wrap_title(title, f"bold {color}"))
            self.console.print(escape(log_str), highlight=True, emoji=True)
        log_str = self._wrap_title(title) + "\n" + log_str
        if self.log_path: self._write_log(log_str) 
    def lprint(self, *args: str, **kwargs: dict):
        if not self.debug: return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = "\n".join(map(str, args))
        color = kwargs.get("color", "white")
        title = kwargs.get("title", "")
        log_str = f"[{timestamp}]\n{message}"
            # print_in_box(log_str, color=color, title=title)
        self.console.print(self._wrap_title(title, f"bold {color}"))
        self.console.print(escape(log_str), highlight=True, emoji=True)
        
    def _wrap_timestamp(self, timestamp: str, color: bool = True):
        color_bos = "[grey58]" if color else ""
        color_eos = "[/grey58]" if color else ""
        return f"{color_bos}[{timestamp}]{color_eos}"
    def _print_tool_execution(self, message, timestamp: str):
        self.console.print(self._wrap_title("Tool Execution", "bold pink3"))
        self.console.print(self._wrap_timestamp(timestamp, color=True))
        self.console.print("[bold blue]Tool Execution:[/bold blue]", end=" ")
        self.console.print(f"[bold purple]{message['name']}[/bold purple]\n[bold blue]Result:[/bold blue]")
        self.console.print(f"---\n{escape(message['content'])}\n---")
    def _save_tool_execution(self, message, timestamp: str):
        self._write_log(self._wrap_title("Tool Execution"))
        self._write_log(f"{self._wrap_timestamp(timestamp, color=False)}\ntool execution: {message['name']}\nResult:\n---\n{message['content']}\n---")
    def _print_assistant_message(self, message, timestamp: str):
        self.console.print(self._wrap_title("Assistant Message", "bold light_salmon3"))
        self.console.print(f"{self._wrap_timestamp(timestamp, color=True)}\n[bold blue]{message['sender']}[/bold blue]:", end=" ")
        if message["content"]: self.console.print(escape(message["content"]), highlight=True, emoji=True) 
        else: self.console.print()
    def _save_assistant_message(self, message, timestamp: str):
        self._write_log(self._wrap_title("Assistant Message"))
        content = message["content"] if message["content"] else ""
        self._write_log(f"{self._wrap_timestamp(timestamp, color=False)}\n{message['sender']}: {content}")
    def _print_tool_call(self, tool_calls: List, timestamp: str):
        if len(tool_calls) >= 1: self.console.print(self._wrap_title("Tool Calls", "bold light_pink1"))

        for tool_call in tool_calls:
            f = tool_call["function"]
            name, args = f["name"], f["arguments"]
            arg_str = self._warp_args(args)
            self.console.print(f"{self._wrap_timestamp(timestamp, color=True)}\n[bold purple]{name}[/bold purple]({escape(arg_str)})")
    def _save_tool_call(self, tool_calls: List, timestamp: str):
        if len(tool_calls) >= 1: self._write_log(self._wrap_title("Tool Calls"))

        for tool_call in tool_calls:
            f = tool_call["function"]
            name, args = f["name"], f["arguments"]
            arg_str = self._warp_args(args)
            self._write_log(f"{self._wrap_timestamp(timestamp, color=False)}\n{name}({arg_str})")

    def pretty_print_messages(self, message, **kwargs) -> None:
        # for message in messages:
        if message["role"] != "assistant" and message["role"] != "tool":
            return
        # console = Console()
        
        # handle tool call
        if message["role"] == "tool":
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.log_path: self._save_tool_execution(message, timestamp)
            if self.debug: self._print_tool_execution(message, timestamp)
            return
        
        # handle assistant message
        # print agent name in blue
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.log_path: self._save_assistant_message(message, timestamp)
        if self.debug: self._print_assistant_message(message, timestamp)

        # print tool calls in purple, if any
        tool_calls = message.get("tool_calls") or []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.log_path: self._save_tool_call(tool_calls, timestamp)
        if self.debug: self._print_tool_call(tool_calls, timestamp)
class LoggerManager:
    _instance = None
    _logger: MetaChainLogger = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = LoggerManager()
        return cls._instance

    @classmethod
    def get_logger(cls):
        return cls.get_instance()._logger

    @classmethod
    def set_logger(cls, new_logger):
        cls.get_instance()._logger = new_logger
if DEFAULT_LOG:
    if LOG_PATH is None:
        log_dir = Path(f'logs/res_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        log_dir.mkdir(parents=True, exist_ok=True)  # recursively create all necessary parent directories
        log_path = str(log_dir / "agent.log")
        # logger = MetaChainLogger(log_path=log_path)
        LoggerManager.set_logger(MetaChainLogger(log_path=log_path))
    else:
        # logger = MetaChainLogger(log_path=LOG_PATH)
        LoggerManager.set_logger(MetaChainLogger(log_path=LOG_PATH))
    # logger.info("Log file is saved to", logger.log_path, "...", title="Log Path", color="light_cyan3")
    LoggerManager.get_logger().info("Log file is saved to", 
                                  LoggerManager.get_logger().log_path, "...", 
                                  title="Log Path", color="light_cyan3")
else:
    # logger = None
    LoggerManager.set_logger(None)
logger = LoggerManager.get_logger()

def set_logger(new_logger):
    LoggerManager.set_logger(new_logger)
# if __name__ == "__main__":
#     logger = MetaChainLogger(log_path="test.log")
#     logger.pretty_print_messages({"role": "assistant", "content": "Hello, world!", "tool_calls": [{"function": {"name": "test", "arguments": {"url": "https://www.google.com", "query": "test"}}}], "sender": "test_agent"})

#     logger.pretty_print_messages({"role": "tool", "name": "test", "content": "import requests\n\nurl = 'https://www.google.com'\nquery = 'test'\n\nresponse = requests.get(url)\nprint(response.text)", "sender": "test_agent"})
#     logger.info("test content", color="red", title="test")
