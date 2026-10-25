import asyncio
import json
from types import SimpleNamespace

from research_agent.inno.core import MetaChain
from research_agent.inno.types import Agent, Response


class QuietLogger:
    def info(self, *args, **kwargs):
        pass

    def pretty_print_messages(self, *args, **kwargs):
        pass


class AssistantMessage:
    def __init__(self, tool_calls=None):
        self.content = "final answer"
        self.tool_calls = tool_calls
        self.sender = None

    def model_dump_json(self):
        calls = None
        if self.tool_calls:
            calls = [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments,
                    },
                }
                for call in self.tool_calls
            ]
        return json.dumps(
            {
                "role": "assistant",
                "content": self.content,
                "sender": self.sender,
                "tool_calls": calls,
            }
        )


def run_without_tools(tool_calls):
    message = AssistantMessage(tool_calls)
    chain = MetaChain.__new__(MetaChain)
    chain.logger = QuietLogger()
    handled_calls = []

    async def completion(**kwargs):
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])

    def handle_tool_calls(*args, **kwargs):
        handled_calls.append(args[0])
        return Response(messages=[{"role": "tool", "content": "executed"}])

    chain.try_completion_with_truncation = completion
    chain.handle_tool_calls = handle_tool_calls
    agent = Agent(name="root", tool_choice="required", functions=[])

    result = asyncio.run(
        chain.run_async(
            agent,
            [{"role": "user", "content": "hello"}],
            execute_tools=False,
        )
    )
    return result, handled_calls


def test_execute_tools_false_returns_final_message_without_tool_calls():
    result, handled_calls = run_without_tools(None)

    assert handled_calls == []
    assert len(result.messages) == 1
    assert result.messages[0]["content"] == "final answer"


def test_execute_tools_false_does_not_handle_requested_tool():
    tool_call = SimpleNamespace(
        id="call-1",
        function=SimpleNamespace(name="side_effect", arguments="{}"),
    )
    result, handled_calls = run_without_tools([tool_call])

    assert handled_calls == []
    assert len(result.messages) == 1
    assert result.messages[0]["content"] == "final answer"
