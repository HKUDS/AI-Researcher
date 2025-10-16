from research_agent.inno.types import Agent
from research_agent.inno.tools.terminal_tools import gen_code_tree_structure, read_file, execute_command, terminal_page_down, terminal_page_up, terminal_page_to
from research_agent.inno.util import make_message, make_tool_message
from research_agent.inno.registry import register_agent
from research_agent.inno.types import Result
import json
from inspect import signature
from research_agent.inno.environment.docker_env import DockerEnv, with_env
import re 
from pathlib import Path
import subprocess

GITHUB_RE = re.compile(r'^https?://github\.com/[^/]+/[^/]+/?$')


def case_resolved(reference_codebases: list[str], reference_paths: list[str], reference_papers: list[str]):
    """
    The function to output the determined reference codebases. Use this function only after you have carefully reviewed the existing resources and understand the task.
    Args:
        reference_codebases: list of the name of the determined reference codebases.
        reference_paths: list of the determined reference paths.
        reference_papers: list of titles of the determined reference papers.
    """
    prepare_result = {
        "reference_codebases": reference_codebases,
        "reference_paths": reference_paths,
        "reference_papers": reference_papers
    }

    return Result(
        value=f"""\
I have determined the reference codebases and paths according to the existing resources and the innovative ideas.
{json.dumps(prepare_result, ensure_ascii=False, indent=4)}
""", 
        context_variables={"prepare_result": prepare_result}
    )
@register_agent("get_prepare_agent")
def get_prepare_agent(model: str, **kwargs):
    code_env: DockerEnv = kwargs.get("code_env", None)

    raw_urls: list[str] = kwargs.get("reference_codebases", [])
    validated_urls: list[str] = [
        u for u in raw_urls if _is_valid_github_repo(u)
    ]

    def instructions(context_variables):
      working_dir = context_variables.get("working_dir", None)
      validated_urls = context_variables.get("validated_urls", [])
      
      url_list = "\n".join(f"- {url}" for url in validated_urls) if validated_urls else "(No valid GitHub repositories provided)"
      
      return f"""
You are given a list of papers, searching results of the papers on GitHub, and innovative ideas according to the papers. Your working directory is `/{working_dir}`, you can only access files in this directory.

The user may provide a list called reference codebases. If provided, these repositories are treated as MUST-USE. 
Reference codebases provided by the user:
{url_list}

You should first review the user-provided reference codebases (if any) and use them as MUST-USE repositories. If the provided repositories are insufficient (less than 5 repositories), then review the searching results to find additional repositories that are most relevant and useful to the innovative ideas. You can determine the relevance and usefulness by the following criteria:
1. Repositories with more stars are more recommended.
2. Repositories created more recently are more recommended, [IMPORTANT!] Too old repositories are not recommended.
3. More detaild `README.md` file means more readable codebase and more reproducible, so more recommended.
4. More clear code structure, code comments, and inline code explanations mean more readable codebase and more maintainable, so more recommended.
5. I prefer repositories with `python` language, and running coding in the local machine rather than in docker. As for deep learning projects, I prefer `pytorch` framework.

You should choose at least 5 repositories as the reference codebases.

I should use the determined repositories as reference codebases to implement the innovative ideas, so your decision should be as accurate as possible, and the number of repositories should be as less as possible. 

During the decision process, you can use the following tools:
1. You can use `execute_command` to git clone the repository to the working directory `/{working_dir}`. Choose 5-8 repositories you really need. And you should reserve the names of the repositories.

2. You can use `gen_code_tree_structure` to generate the tree structure of the code in the repository.

3. You can use `read_file` to read the content of the file in the repository. Note that read `README.md` file can help you know the purpose and function of the code in the repository, and read other files can help you know the details of the implementation.

4. You can use `terminal_page_down`, `terminal_page_up` and `terminal_page_to` to scroll the terminal output when it is too long. You can use `terminal_page_to` to move the viewport to the specific page of terminal where the meaningful content is, for example, when the terminal output contains a progress bar or output of generating directory structure when there are many datasets in the directory, you can use `terminal_page_to` to move the viewport to the end of terminal where the meaningful content is.

5. Finally, you should use the function `case_resolved` to output the determined reference codebases.
      """
    tools = [gen_code_tree_structure, read_file, execute_command, case_resolved, terminal_page_down, terminal_page_up, terminal_page_to]
    tools = [with_env(code_env)(tool) if 'env' in signature(tool).parameters else tool for tool in tools]
    return Agent(
        name="Prepare Agent",
        model=model,
        instructions=instructions,
        functions=tools,
        tool_choice="required",
        parallel_tool_calls=False,
        context_variables={"validated_urls": validated_urls}
    )

def _is_valid_github_repo(url: str) -> bool:
    return bool(GITHUB_RE.match(url.strip()))
