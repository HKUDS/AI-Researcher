# Standard library imports
import copy
import json
from collections import defaultdict
from typing import List, Callable, Union
from datetime import datetime
# Local imports
import litellm
from litellm import ContextWindowExceededError, BadRequestError
from litellm.types.utils import Message as litellmMessage
from .util import function_to_json, debug_print, merge_chunk, pretty_print_messages
from .types import (
    Agent,
    AgentFunction,
    Message,
    ChatCompletionMessageToolCall,
    Function,
    Response,
    Result,
)
from litellm import completion, acompletion
from pathlib import Path
from .logger import MetaChainLogger, LoggerManager
from httpx import RemoteProtocolError, ConnectError
from litellm.exceptions import APIError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type, 
    RetryCallState
)
from tenacity.wait import wait_base
from openai import AsyncOpenAI
from research_agent.constant import  API_BASE_URL, NOT_SUPPORT_SENDER, MUST_ADD_USER, NOT_SUPPORT_FN_CALL, NOT_USE_FN_CALL
from research_agent.inno.fn_call_converter import convert_tools_to_description, convert_non_fncall_messages_to_fncall_messages, SYSTEM_PROMPT_SUFFIX_TEMPLATE, convert_fn_messages_to_non_fn_messages, interleave_user_into_messages
from research_agent.inno.memory.utils import encode_string_by_tiktoken, decode_tokens_by_tiktoken
import re

# litellm.set_verbose=True
# litellm.num_retries = 3

def should_retry_error(retry_state: RetryCallState):
    """检查是否应该重试错误
    
    Args:
        retry_state: RetryCallState对象，包含重试状态信息
        
    Returns:
        bool: 是否应该重试
    """
    if retry_state.outcome is None:
        return False
        
    exception = retry_state.outcome.exception()
    if exception is None:
        return False
        
    print(f"Caught exception: {type(exception).__name__} - {str(exception)}")
    
    # 匹配更多错误类型
    if isinstance(exception, (APIError, RemoteProtocolError, ConnectError)):
        return True
    
    # 通过错误消息匹配
    error_msg = str(exception).lower()
    return any([
        "connection error" in error_msg,
        "server disconnected" in error_msg,
        "eof occurred" in error_msg,
        "timeout" in error_msg,
        "rate limit" in error_msg,  # 添加 rate limit 错误检查
        "rate_limit_error" in error_msg,  # Anthropic 的错误类型
        "too many requests" in error_msg,  # HTTP 429 错误
        "overloaded" in error_msg,  # 添加 Anthropic overloaded 错误
        "overloaded_error" in error_msg,  # 添加 Anthropic overloaded 错误的另一种形式
        "负载已饱和" in error_msg,  # 添加中文错误消息匹配
        "error code: 429" in error_msg,  # 添加 HTTP 429 状态码匹配
        "context_length_exceeded" in error_msg  # 添加上下文长度超限错误匹配
    ])
__CTX_VARS_NAME__ = "context_variables"
logger = LoggerManager.get_logger()
def truncate_message(message: str) -> str:
    """按比例截断消息"""
    if not message:
        return message
    tokens = encode_string_by_tiktoken(message)
    # 假设每个字符平均对应1个token（这是个粗略估计）
    current_length = len(tokens)
    # 多截断一些以确保在token限制内
    max_length = 10000
    if current_length > max_length:
        return decode_tokens_by_tiktoken(tokens[:max_length])
    else:
        return message

class my_wait_strategy(wait_base):
    def __init__(self):
        self.short_wait = wait_exponential(multiplier=2, min=1, max=60)
        self.long_wait = wait_exponential(multiplier=2, min=30, max=1200)

    def __call__(self, retry_state):
        exception = retry_state.outcome.exception()
        if isinstance(exception, litellm.RateLimitError):
            return self.long_wait(retry_state)
        else:
            return self.short_wait(retry_state)

def before_sleep_fn(retry_state):
    """A custom function to be called before sleeping in a retry loop."""
    exception = retry_state.outcome.exception()
    wait_time = retry_state.next_action.sleep
    if isinstance(exception, litellm.RateLimitError):
        print(f"Rate limit exceeded. Retrying in {wait_time:.2f} seconds...")
    else:
        print(f"An error occurred: {exception}. Retrying in {wait_time:.2f} seconds... (attempt {retry_state.attempt_number})")

class MetaChain:
    def __init__(self, log_path: Union[str, None, MetaChainLogger] = None):
        """
        log_path: path of log file, None
        """
        if logger:
            self.logger = logger
        elif isinstance(log_path, MetaChainLogger):
            self.logger = log_path
        else:
            self.logger = MetaChainLogger(log_path=log_path)
        if self.logger.log_path is None: self.logger.info("[Warning] Not specific log path, so log will not be saved", "...", title="Log Path", color="light_cyan3")
        else: self.logger.info("Log file is saved to", self.logger.log_path, "...", title="Log Path", color="light_cyan3")

    def get_chat_completion(
        self,
        agent: Agent,
        history: List,
        context_variables: dict,
        model_override: str,
        stream: bool,
        debug: bool,
    ) -> Message:
        context_variables = defaultdict(str, context_variables)
        instructions = (
            agent.instructions(context_variables)
            if callable(agent.instructions)
            else agent.instructions
        )
        if agent.examples:
            examples = agent.examples(context_variables) if callable(agent.examples) else agent.examples
            history = examples + history
        
        messages = [{"role": "system", "content": instructions}] + history
        # debug_print(debug, "Getting chat completion for...:", messages)
        
        tools = [function_to_json(f) for f in agent.functions]
        # hide context_variables from model
        for tool in tools:
            params = tool["function"]["parameters"]
            params["properties"].pop(__CTX_VARS_NAME__, None)
            if __CTX_VARS_NAME__ in params["required"]:
                params["required"].remove(__CTX_VARS_NAME__)

        create_params = {
            "model": model_override or agent.model,
            "messages": messages,
            "tools": tools or None,
            "tool_choice": agent.tool_choice,
            "stream": stream,
            "base_url": API_BASE_URL,
        }

        if create_params['model'].startswith("mistral"):
            messages = create_params["messages"]
            for message in messages:
                if 'sender' in message:
                    del message['sender']
            create_params["messages"] = messages

        if tools and create_params['model'].startswith("gpt"):
            create_params["parallel_tool_calls"] = agent.parallel_tool_calls

        return completion(**create_params)

    def handle_function_result(self, result, debug) -> Result:
        match result:
            case Result() as result:
                return result

            case Agent() as agent:
                return Result(
                    value=json.dumps({"assistant": agent.name}),
                    agent=agent,
                )
            case _:
                try:
                    return Result(value=str(result))
                except Exception as e:
                    error_message = f"Failed to cast response to string: {result}. Make sure agent functions return a string or Result object. Error: {str(e)}"
                    self.logger.info(error_message, title="Handle Function Result Error", color="red")
                    raise TypeError(error_message)

    def handle_tool_calls(
        self,
        tool_calls: List[ChatCompletionMessageToolCall],
        functions: List[AgentFunction],
        context_variables: dict,
        debug: bool,
        handle_mm_func: Callable[[], str] = None,
    ) -> Response:
        function_map = {f.__name__: f for f in functions}
        partial_response = Response(
            messages=[], agent=None, context_variables={})
        
        for tool_call in tool_calls:
            name = tool_call.function.name
            # handle missing tool case, skip to next tool
            if name not in function_map:
                self.logger.info(f"Tool {name} not found in function map.", title="Tool Call Error", color="red")
                partial_response.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": f"[Tool Call Error] Error: Tool {name} not found.",
                    }
                )
                continue
            args = json.loads(tool_call.function.arguments)
            
            # debug_print(
            #     debug, f"Processing tool call: {name} with arguments {args}")
            func = function_map[name]
            # pass context_variables to agent functions
            if __CTX_VARS_NAME__ in func.__code__.co_varnames:
                args[__CTX_VARS_NAME__] = context_variables
            try:
                raw_result = function_map[name](**args)
            except Exception as e:
                # if "case_resolved" in name:
                #     raw_result = function_map[name](tool_call.function.arguments)
                # else:
                self.logger.info(f"[Tool Call Error] The execution of tool {name} failed. Error: {e}", title="Tool Call Error", color="red")
                partial_response.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": f"[Tool Call Error] The execution of tool {name} failed. Error: {e}",
                    }
                )
                continue


            result: Result = self.handle_function_result(raw_result, debug)
    
            partial_response.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": name,
                    "content": result.value,
                }
            )
            self.logger.pretty_print_messages(partial_response.messages[-1])
            if result.image: 
                assert handle_mm_func, f"handle_mm_func is not provided, but an image is returned by tool call {name}({tool_call.function.arguments})"
                partial_response.messages.append(
                {
                    "role": "user",
                    "content": [
                    # {"type":"text", "text":f"After take last action `{name}({tool_call.function.arguments})`, the image of current page is shown below. Please take next action based on the image, the current state of the page as well as previous actions and observations."},
                    {"type":"text", "text":handle_mm_func(name, tool_call.function.arguments)},
                    {
                    "type":"image_url",
                        "image_url":{
                            "url":f"data:image/png;base64,{result.image}"
                        }
                    }
                ]
                }
                )
            # debug_print(debug, "Tool calling: ", json.dumps(partial_response.messages[-1], indent=4), log_path=log_path, title="Tool Calling", color="green")
            
            partial_response.context_variables.update(result.context_variables)
            if result.agent:
                partial_response.agent = result.agent

        return partial_response

    def run(
        self,
        agent: Agent,
        messages: List,
        context_variables: dict = {},
        model_override: str = None,
        stream: bool = False,
        debug: bool = True,
        max_turns: int = float("inf"),
        execute_tools: bool = True,
    ) -> Response:
        if stream:
            return self.run_and_stream(
                agent=agent,
                messages=messages,
                context_variables=context_variables,
                model_override=model_override,
                debug=debug,
                max_turns=max_turns,
                execute_tools=execute_tools,
            )
        active_agent = agent
        context_variables = copy.deepcopy(context_variables)
        history = copy.deepcopy(messages)
        init_len = len(messages)

        self.logger.info("Receiveing the task:", history[-1]['content'], title="Receive Task", color="green")

        while len(history) - init_len < max_turns and active_agent:

            # get completion with current history, agent
            completion = self.get_chat_completion(
                agent=active_agent,
                history=history,
                context_variables=context_variables,
                model_override=model_override,
                stream=stream,
                debug=debug,
            )
            message: Message = completion.choices[0].message
            message.sender = active_agent.name
            # debug_print(debug, "Received completion:", message.model_dump_json(indent=4), log_path=log_path, title="Received Completion", color="blue")
            self.logger.pretty_print_messages(message)
            history.append(
                json.loads(message.model_dump_json())
            )  # to avoid OpenAI types (?)

            if not message.tool_calls or not execute_tools:
                self.logger.info("Ending turn.", title="End Turn", color="red")
                break
            # if (message.tool_calls and message.tool_calls[0].function.name == "case_resolved") or not execute_tools:
            #     debug_print(debug, "Ending turn.", log_path=log_path, title="End Turn", color="red")
            #     break

            # handle function calls, updating context_variables, and switching agents
            if message.tool_calls:
                partial_response = self.handle_tool_calls(
                    message.tool_calls, active_agent.functions, context_variables, debug, handle_mm_func=active_agent.handle_mm_func
                )
            else:
                partial_response = Response(messages=[message])
            history.extend(partial_response.messages)
            context_variables.update(partial_response.context_variables)
            if partial_response.agent:
                active_agent = partial_response.agent

        return Response(
            messages=history[init_len:],
            agent=active_agent,
            context_variables=context_variables,
        )
    @retry(
        stop=stop_after_attempt(6),
        wait=my_wait_strategy(),
        retry=should_retry_error,
        before_sleep=before_sleep_fn
    )
    async def get_chat_completion_async(
        self,
        agent: Agent,
        history: List,
        context_variables: dict,
        model_override: str,
        stream: bool,
        debug: bool,
    ) -> Message:
        context_variables = defaultdict(str, context_variables)
        instructions = (
            agent.instructions(context_variables)
            if callable(agent.instructions)
            else agent.instructions
        )
        if agent.examples:
            examples = agent.examples(context_variables) if callable(agent.examples) else agent.examples
            history = examples + history
        
        messages = [{"role": "system", "content": instructions}] + history
        # debug_print(debug, "Getting chat completion for...:", messages)
        
        tools = [function_to_json(f) for f in agent.functions]
        # hide context_variables from model
        for tool in tools:
            params = tool["function"]["parameters"]
            params["properties"].pop(__CTX_VARS_NAME__, None)
            if __CTX_VARS_NAME__ in params["required"]:
                params["required"].remove(__CTX_VARS_NAME__)
        create_model = model_override or agent.model
        if create_model not in NOT_USE_FN_CALL:
            
            # assert litellm.supports_function_calling(model = create_model) == True, f"Model {create_model} does not support function calling, please set `FN_CALL=False` to use non-function calling mode"
            create_params = {
                "model": create_model,
                "messages": messages,
                "tools": tools or None,
                "tool_choice": agent.tool_choice,
                "stream": stream,
                "base_url": API_BASE_URL,
                "timeout": 600,
            }
            NO_SENDER_MODE = False
            for not_sender_model in NOT_SUPPORT_SENDER:
                if not_sender_model in create_model:
                    NO_SENDER_MODE = True
                    break

            if NO_SENDER_MODE:
                messages = create_params["messages"]
                for message in messages:
                    if 'sender' in message:
                        del message['sender']
                create_params["messages"] = messages

            if tools and create_params['model'].startswith("gpt"):
                create_params["parallel_tool_calls"] = agent.parallel_tool_calls
            completion_response = await acompletion(**create_params)
        elif create_model in NOT_USE_FN_CALL:
            assert agent.tool_choice == "required", f"Non-function calling mode MUST use tool_choice = 'required' rather than {agent.tool_choice}"
            last_content = messages[-1]["content"]
            tools_description = convert_tools_to_description(tools)
            messages[-1]["content"] = last_content + "\n[IMPORTANT] You MUST use the tools provided to complete the task.\n" + SYSTEM_PROMPT_SUFFIX_TEMPLATE.format(description=tools_description)
            NO_SENDER_MODE = False
            for not_sender_model in NOT_SUPPORT_SENDER:
                if not_sender_model in create_model:
                    NO_SENDER_MODE = True
                    break

            if NO_SENDER_MODE:
                for message in messages:
                    if 'sender' in message:
                        del message['sender']
            if create_model in NOT_SUPPORT_FN_CALL:
                messages = convert_fn_messages_to_non_fn_messages(messages)
            if create_model in MUST_ADD_USER and messages[-1]["role"] != "user":
                # messages.append({"role": "user", "content": "Please think twice and take the next action according to your previous actions and observations."})
                messages = interleave_user_into_messages(messages)
            create_model = "deepseek-chat"

            create_params = {
                "model": create_model,
                "messages": messages,
                "stream": stream,
                "base_url": API_BASE_URL,
                "timeout": 600,
            }
            completion_response = await acompletion(**create_params)
            last_message = [{"role": "assistant", "content": completion_response.choices[0].message.content}]
            converted_message = convert_non_fncall_messages_to_fncall_messages(last_message, tools)
            converted_tool_calls = [ChatCompletionMessageToolCall(**tool_call) for tool_call in converted_message[0]["tool_calls"]]
            completion_response.choices[0].message = litellmMessage(content = converted_message[0]["content"], role = "assistant", tool_calls = converted_tool_calls)
        # response = await client.chat.completions.create(**create_params)
        return completion_response

    async def try_completion_with_truncation(self, agent, history, context_variables, model_override, stream, debug):
        try:
            return await self.get_chat_completion_async(
                agent=agent,
                history=history,
                context_variables=context_variables,
                model_override=model_override,
                stream=stream,
                debug=debug,
            )
        except (ContextWindowExceededError, BadRequestError) as e:
            error_msg = str(e)
            # 检查是否是上下文长度超限错误
            if "context length" in error_msg.lower() or "context_length_exceeded" in error_msg:
                # 提取超出的token数量
                # match = re.search(r'resulted in (\d+) tokens.*maximum context length is (\d+)', error_msg)
                # if match:
                # current_tokens = int(match.group(1))
                # max_tokens = int(match.group(2))
                
                # 修改最后一条消息
                if history and len(history) > 0:
                    last_message = history[-1]
                    if isinstance(last_message.get('content'), str):
                        last_message['content'] = truncate_message(
                            last_message['content'],
                        )
                        self.logger.info(
                            f"消息已截断以适应上下文长度限制", 
                            title="Message Truncated", 
                            color="yellow"
                        )
                        # 重试一次
                        return await self.get_chat_completion_async(
                            agent=agent,
                            history=history,
                            context_variables=context_variables,
                            model_override=model_override,
                            stream=stream,
                            debug=debug,
                        )
            # 如果不是上下文长度问题或无法处理，则重新抛出异常
            raise e
    
    async def run_async(
        self,
        agent: Agent,
        messages: List,
        context_variables: dict = {},
        model_override: str = None,
        stream: bool = False,
        debug: bool = True,
        max_turns: int = float("inf"),
        execute_tools: bool = True,
    ) -> Response:
        assert stream == False, "Async run does not support stream"
        active_agent = agent
        enter_agent = agent
        context_variables = copy.deepcopy(context_variables)
        history = copy.deepcopy(messages)
        init_len = len(messages)

        self.logger.info("Receiveing the task:", history[-1]['content'], title="Receive Task", color="green")

        while len(history) - init_len < max_turns and active_agent:

            # get completion with current history, agent
            try:
                completion_response = await self.try_completion_with_truncation(
                    agent=active_agent,
                    history=history,
                    context_variables=context_variables,
                    model_override=model_override,
                    stream=stream,
                    debug=debug,
                )
            except Exception as e:
                self.logger.info(f"Error: {e}", title="Error", color="red")
                history.append({"role": "error", "content": f"Error: {e}"})
                break
            message: Message = completion_response.choices[0].message
            message.sender = active_agent.name
            # debug_print(debug, "Received completion:", message.model_dump_json(indent=4), log_path=log_path, title="Received Completion", color="blue")
            self.logger.pretty_print_messages(message)
            history.append(
                json.loads(message.model_dump_json())
            )  # to avoid OpenAI types (?)

            if enter_agent.tool_choice != "required":
                if (not message.tool_calls and active_agent.name == enter_agent.name) or not execute_tools:
                    self.logger.info("Ending turn.", title="End Turn", color="red")
                    break
            else: 
                if (message.tool_calls and message.tool_calls[0].function.name == "case_resolved") or not execute_tools:
                    self.logger.info("Ending turn with case resolved.", title="End Turn", color="red")
                    try:
                        partial_response = self.handle_tool_calls(
                            message.tool_calls, active_agent.functions, context_variables, debug, handle_mm_func=active_agent.handle_mm_func
                        )
                        history.extend(partial_response.messages)
                        context_variables.update(partial_response.context_variables)
                        if partial_response.messages[-1]["content"].startswith("[Tool Call Error]") is False:
                            break
                        else: 
                            print("continue")
                            continue
                    except Exception as e:
                        self.logger.info(f"Error: {e}", title="Error", color="red")
                        history.append({"role": "error", "content": f"Error: {e}"})
                        break
                elif (message.tool_calls and message.tool_calls[0].function.name == "case_not_resolved") or not execute_tools:
                    self.logger.info("Ending turn with case not resolved.", title="End Turn", color="red")
                    try:
                        partial_response = self.handle_tool_calls(
                            message.tool_calls, active_agent.functions, context_variables, debug, handle_mm_func=active_agent.handle_mm_func
                        )
                        history.extend(partial_response.messages)
                        context_variables.update(partial_response.context_variables)
                        if partial_response.messages[-1]["content"].startswith("[Tool Call Error]") is False:
                            break
                        else: 
                            print("continue")
                            continue
                    except Exception as e:
                        self.logger.info(f"Error: {e}", title="Error", color="red")
                        history.append({"role": "error", "content": f"Error: {e}"})
                        break
            # if (message.tool_calls and message.tool_calls[0].function.name == "case_resolved") or not execute_tools:
            #     debug_print(debug, "Ending turn.", log_path=log_path, title="End Turn", color="red")
            #     break

            # handle function calls, updating context_variables, and switching agents
            if message.tool_calls:
                try:
                    partial_response = self.handle_tool_calls(
                    message.tool_calls, active_agent.functions, context_variables, debug, handle_mm_func=active_agent.handle_mm_func
                )
                except Exception as e:
                    self.logger.info(f"Error: {e}", title="Error", color="red")
                    history.append({"role": "error", "content": f"Error: {e}"})
                    break
            else:
                partial_response = Response(messages=[{"role": "user", "content": "Please use the tools provided to complete the task."}])
            history.extend(partial_response.messages)
            context_variables.update(partial_response.context_variables)
            if partial_response.agent:
                active_agent = partial_response.agent

        return Response(
            messages=history[init_len:],
            agent=active_agent,
            context_variables=context_variables,
        )
