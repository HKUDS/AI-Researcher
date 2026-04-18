import json
import os
from research_agent.inno.util import single_select_menu
from research_agent.inno.core import MetaChain, MetaChainLogger
from typing import Union, Dict, List, Callable, Any
from research_agent.inno import Agent
from abc import ABC, abstractmethod
# 사용안하는 import제거

class AgentModule:
    def __init__(self, agent: Agent, client: MetaChain, cache_path: str):
        self.agent = agent
        self.client = client
        self.cache_path = cache_path
    async def __call__(self, messages: List[Dict], context_variables: Dict, iter_times: int = None, *args, **kwargs):
        # messages = [{"role": "user", "content": query}]
        agent_cache, escape_running = self.check_cache(self.agent.name, iter_times)
        if agent_cache and escape_running:
            messages.extend(agent_cache["messages"])
            context_variables.update(agent_cache["context_variables"])
        elif agent_cache and not escape_running:
            messages.extend(agent_cache["messages"])
            context_variables.update(agent_cache["context_variables"])
            response = await self.client.run_async(self.agent, messages, context_variables=context_variables, debug=True)
            ret_messages = response.messages
            ret_context_variables = response.context_variables
            if ret_messages[-1]["role"] != "error":
                ret_messages.append({"role": "success", "content": "The agent successfully generated a response."})
            self.save_cache(self.agent.name, agent_cache["messages"] + ret_messages[:-1], iter_times, ret_context_variables)
            messages.extend(ret_messages[:-1])
            context_variables.update(ret_context_variables)
            if ret_messages[-1]["role"] == "error":
                raise Exception(ret_messages[-1]["content"])
        else:
            response = await self.client.run_async(self.agent, messages, context_variables=context_variables, debug=True)
            ret_messages = response.messages
            ret_context_variables = response.context_variables
            if ret_messages[-1]["role"] != "error":
                ret_messages.append({"role": "success", "content": "The agent successfully generated a response."})
            self.save_cache(self.agent.name, ret_messages[:-1], iter_times, ret_context_variables)
            messages.extend(ret_messages[:-1])
            context_variables.update(ret_context_variables)
            if ret_messages[-1]["role"] == "error":
                raise Exception(ret_messages[-1]["content"])
        return messages, context_variables
    def save_cache(self, agent_name, messages, iter_times: int = None, context_variables: Dict = None):
        agent_name = agent_name.replace(" ", "_").lower()
        if iter_times is not None:
            agent_name = agent_name + f"_iter_{iter_times}"
        agent_cache_file = f"{self.cache_path}/agents/{agent_name}.json"
        os.makedirs(os.path.dirname(agent_cache_file), exist_ok=True)
        with open(agent_cache_file, "w", encoding="utf-8") as f:
            json.dump({"messages": messages, "context_variables": context_variables}, f, ensure_ascii=False, indent=4)
    def check_cache(self, agent_name, iter_times: int = None):
        agent_name_norm = agent_name.replace(" ", "_").lower()
        if iter_times is not None:
            agent_name_norm = agent_name_norm + f"_iter_{iter_times}"
        cache_file = f"{self.cache_path}/agents/{agent_name_norm}.json"
        if os.path.exists(cache_file):
            choice = single_select_menu(["Yes", "Resume", "No"], f"The agent '{agent_name}' cache file exists, do you want to use it?")
            if choice == "Yes":
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f), True
            elif choice == "Resume":
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f), False
            else:
                return None, False
        return None, False
    
class ToolModule:
    def __init__(self, tool: Callable[[Any], Union[str, Dict]], cache_path: str):
        self.tool = tool
        self.cache_path = cache_path
    def __call__(self, tool_args: Dict, *args, **kwargs):
        tool_cache = self.check_cache(self.tool.__name__)
        if tool_cache:
            return tool_cache
        else:
            tool_result = self.tool(**tool_args)
            self.save_cache(self.tool, tool_args, tool_result)
            return tool_result
    def save_cache(self, tool: Callable, tool_args: Dict, tool_result: Union[str, Dict]):
        tool_name = tool.__name__

        tool_cache_file = f"{self.cache_path}/tools/{tool_name}.json"
        os.makedirs(os.path.dirname(tool_cache_file), exist_ok=True)
        tool_cache_dict = {
            "name": tool_name,
            "args": tool_args,
            "result": tool_result
        }
        with open(tool_cache_file, "w", encoding="utf-8") as f:
            json.dump(tool_cache_dict, f, ensure_ascii=False, indent=4)
    def check_cache(self, tool_name: str):
        tool_name = tool_name
        cache_file = f"{self.cache_path}/tools/{tool_name}.json"
        if os.path.exists(cache_file):
            choice = single_select_menu(["Yes", "No"], f"The tool '{tool_name}' cache file exists, do you want to use it?")
            if choice == "Yes":
                with open(cache_file, "r", encoding="utf-8") as f:
                    tool_cache_dict = json.load(f)
                    return tool_cache_dict["result"]
            else:
                return None
        return None

class FlowModule(ABC):
    def __init__(self, cache_path: str, log_path: Union[str, None, MetaChainLogger] = None, model: str = "gpt-4o-2024-08-06"):
        self.cache_path = cache_path
        self.client = MetaChain(log_path=log_path)
        self.model = model
    @abstractmethod
    async def forward(self, *args, **kwargs):
        raise NotImplementedError("subclass should implement this method")
    
    async def __call__(self, *args, **kwargs):
        return await self.forward(*args, **kwargs)

    