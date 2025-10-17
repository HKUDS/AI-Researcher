from research_agent.inno.types import Agent
from research_agent.inno.tools.terminal_tools import gen_code_tree_structure, read_file, terminal_page_down, terminal_page_up, terminal_page_to
from research_agent.inno.tools.inno_tools.code_search import search_github_repos
from research_agent.inno.tools.inno_tools.web_tools import with_env as with_env_web
from research_agent.inno.util import make_message, make_tool_message
from research_agent.inno.registry import register_agent
from research_agent.inno.environment.docker_env import DockerEnv
from research_agent.inno.environment.docker_env import with_env as with_env_docker
from research_agent.inno.environment.browser_env import BrowserEnv
from research_agent.inno.tools.terminal_tools import execute_command
from research_agent.inno.tools.file_surfer_tool import with_env as with_env_file
from research_agent.inno.tools.file_surfer_tool import (
    open_local_file,
    page_up_markdown,
    find_on_page_ctrl_f,
    find_next,
    visualizer,
)
from research_agent.inno.environment.markdown_browser import RequestsMarkdownBrowser
from inspect import signature
from typing import Dict, Any
import json


def case_resolved(
    context_variables, fully_correct: bool, suggestion: Dict[str, str] = None
):
    """
    Use this function when you have finished the task and want to give a suggestion about the implementation. You can only use this function after you have checked the implementation and the reference codebases.

    Args:
       fully_correct: whether the implementation is fully correct. If not, you should give a suggestion about the implementation.
       suggestion: the suggestion about the implementation. It should be a dictionary with the keys as the key points in the innovative idea and the values as the suggestions about the implementation. If the implementation is fully correct, you can set this argument to None.
    """
    suggestion_dict = {"fully_correct": fully_correct, "suggestion": suggestion}
    context_variables["suggestion_dict"] = suggestion_dict
    ret_val = f"""\
Here is the suggestion about the implementation:
Whether the implementation is fully correct: {fully_correct}
The suggestion about the implementation:
{json.dumps(suggestion_dict, indent=4)}
"""
    return ret_val



def get_code_review_agent(model: str, **kwargs):
    code_env: DockerEnv = kwargs.get("code_env", None)

    def instructions(context_variables):
        working_dir = context_variables.get("working_dir", None)
        return f"""You are a code reviewer, who can help me review the code in the directory: `/{working_dir}`.

      A `Machine Learning Agent` has implemented the code in the directory `/{working_dir}/project` with the innovative ideas, and you should review the code to ensure it meets the requirements of the innovative ideas, rather than a toy implementation.

      You can also review the reference codebases in the directory `/{working_dir}` to get more information about the task.

      Use `terminal_page_down` `terminal_page_up` and `terminal_page_to` to scroll the terminal output when it is too long.
      [Note] You can use `terminal_page_to` to move the viewport to the end of terminal when the middle of terminal output are meaningless, like the output of progress bar or output of generating directory structure when there are many datasets in the directory, you can use this function to move the viewport to the end of terminal where the meaningful content is.

      After reviewing the code, you should use the function `transfer_to_judge_agent` to transfer the conversation to the `Judge Agent`, and give a code review report.
      """

    tools = [read_file, gen_code_tree_structure, terminal_page_down, terminal_page_up, terminal_page_to]
    tools = [
        with_env_docker(code_env)(tool) if "env" in signature(tool).parameters else tool
        for tool in tools
    ]
    return Agent(
        name="Code Review Agent",
        model=model,
        instructions=instructions,
        functions=tools,
        tool_choice="required",
    )


@register_agent("get_judge_agent")
def get_judge_agent(model: str, **kwargs):
    file_env: RequestsMarkdownBrowser = kwargs.get("file_env", None)
    web_env: BrowserEnv = kwargs.get("web_env", None)
    code_env: DockerEnv = kwargs.get("code_env", None)
    # academic_search_agent = get_academic_search_agent(
    #     model, web_env=web_env, code_env=code_env
    # )
    # filesurfer_agent = get_filesurfer_agent(model, file_env=file_env)
    code_review_agent = get_code_review_agent(model, code_env=code_env)

    def instructions(context_variables):
        working_dir = context_variables.get("working_dir", None)
        return f"""You are a advisor that can help the `Machine Learning Agent` to implement the task.

      A `Machine Learning Agent` has implemented the code in the directory `/{working_dir}/project` with the innovative ideas, but I am not sure if the implementation is correct and meets the requirements of the innovative ideas, especially some specific academic definitions.

      Your job is to go through the implementation, go through the reference codebases in the directory `/{working_dir}`, and make sure the implementation is correct and meets the requirements of the innovative ideas, especially some specific academic definitions. 

      [IMPORTANT] You should carefully check whether the `Machine Learning Agent` has implemented the specific atomic idea correctly one by one based on the survey notes and the innovative idea.

      After carefully checking the implementation and the reference codebases, you should use the function `case_resolved` to propose a final suggestion about the implementation.
      """

    def transfer_to_code_review_agent(atomic_idea):
        """
        Transfer the conversation to the `Code Review Agent`. Use this function when you want to review the code in the working directory.

        Args:
           atomic_idea: the atomic idea you separate from the innovative idea and the survey notes. It should be as specific and accurate as possible.
        """
        return code_review_agent

    judge_agent = Agent(
        name="Judge Agent",
        model=model,
        instructions=instructions,
        functions=[
            case_resolved,
            transfer_to_code_review_agent,
        ],
        tool_choice="required",
    )

    def transfer_to_judge_agent(task_report):
        """
        Transfer the conversation to the `Judge Agent`. Use this function when you want to give a report about the search, file reading, and code reviewing.

        Args:
           task_report: the report about the search, file reading, and code reviewing.
        """
        return judge_agent

    code_review_agent.functions.append(transfer_to_judge_agent)
    return judge_agent
