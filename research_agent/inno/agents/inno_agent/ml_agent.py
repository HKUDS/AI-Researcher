from research_agent.inno.types import Agent
from research_agent.inno.tools.terminal_tools import (
    gen_code_tree_structure, execute_command, read_file, create_file, write_file, list_files, create_directory, run_python, terminal_page_down, terminal_page_up, terminal_page_to
)
from research_agent.inno.util import make_message, make_tool_message
from research_agent.inno.registry import register_agent
from research_agent.inno.environment.docker_env import DockerEnv, with_env
from inspect import signature
def case_resolved(task_response):
   """
   The task response is the result of the task. Use this function only after you have successfully completed the task. 

   Args:
      task_response: The result of the task.
   """
   return task_response

def case_not_resolved(failure_reason):
   """
   The failure reason is the reason why you cannot find a solution to the task. You can use this function only after you have tried multiple times and still cannot find a solution.

   Args:
      failure_reason: The reason why you cannot find a solution to the task.
   """
   return failure_reason
   
@register_agent("get_ml_agent")
def get_ml_agent(model: str, **kwargs):
    code_env: DockerEnv = kwargs.get("code_env", None)
    def instructions(context_variables):
      working_dir = context_variables.get("working_dir", None)
      return f"""\
You are a machine learning engineer tasked with implementing innovative ML projects. Your workspace is: `/{working_dir}`.

OBJECTIVE:
Create a self-contained, well-organized implementation in `/{working_dir}/project` based on:
- The provided innovative idea
- Reference codebases (up to 5 repositories)
- The detailed implementation plan

CODE INTEGRATION PRINCIPLES:
1. Self-Contained Project
   - ALL code must reside within the project directory
   - NO direct imports from reference codebases
   - Reference code must be thoughtfully integrated into your project structure
   - Maintain consistent coding style across integrated components

2. Code Adaptation Guidelines
   - Study reference implementations thoroughly
   - Understand the core logic and algorithms
   - Rewrite and adapt code to fit your project's architecture
   - Document the origin and modifications of adapted code
   - Ensure consistent naming conventions and style

AVAILABLE TOOLS:
1. Project Structure:
   - `create_directory`: Create organized project structure
   - `create_file`, `write_file`: Write clean, documented code
   - `list_files`, `read_file`: Examine existing code
   - `terminal_page_down`, `terminal_page_up` and `terminal_page_to`: Scroll the terminal output when it is too long. You can use `terminal_page_to` to move the viewport to the specific page of terminal where the meaningful content is, for example, when the terminal output contains a progress bar or output of generating directory structure when there are many datasets in the directory, you can use `terminal_page_to` to move the viewport to the end of terminal where the meaningful content is.
2. Execution:
   - `run_python`: Run scripts without arguments
   - `execute_command`: Run with environment variables/arguments
   Note: When using `execute_command`, use `cd xx` instead of `cwd=xx`

IMPORTANT NOTES:
1. Code Integration
   - DO NOT import directly from reference codebases
   - DO adapt and integrate code thoughtfully
   - DO document code origins and modifications

2. Project Independence
   - Ensure all dependencies are explicitly declared
   - Include all necessary utility functions
   - Maintain clean separation from reference code
   - Create a truly self-contained project

3. Implementation Checklist
   - Verify each model component against the plan
   - Confirm dataset matches specifications
   - Document any deviations or modifications
   - NO shortcuts or simplifications without approval

Remember: Your goal is to create a well-organized, self-contained project that:
1. Implements EVERY component from the model plan exactly as specified
2. Uses the EXACT datasets from the plan (no toy data)
3. Thoughtfully incorporates ideas from reference implementations
4. Maintains its own coherent structure
5. You should intergrate ALL acacdemic definition and their code implementation into the project.
"""
    tools = [gen_code_tree_structure, execute_command, read_file, create_file, write_file, list_files, create_directory, run_python, case_resolved, case_not_resolved, terminal_page_down, terminal_page_up, terminal_page_to]
    tools = [with_env(code_env)(tool) if 'env' in signature(tool).parameters else tool for tool in tools]
    
    return Agent(
    name="Machine Learning Agent",
    model=model,
    instructions=instructions,
    functions=tools,
    tool_choice = "required", 
    parallel_tool_calls = False
    )

