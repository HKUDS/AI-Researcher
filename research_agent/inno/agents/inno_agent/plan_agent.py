from research_agent.inno.types import Agent
from research_agent.inno.tools.terminal_tools import gen_code_tree_structure, read_file, terminal_page_down, terminal_page_up, terminal_page_to
from research_agent.inno.util import make_message, make_tool_message
from research_agent.inno.tools.inno_tools.planning_tools import plan_dataset, plan_training, plan_testing
from research_agent.inno.registry import register_agent
from research_agent.inno.environment.docker_env import DockerEnv, with_env
from inspect import signature

def case_resolved(context_variables):
   """ 
   The function to merge the plan of the dataset, model, and training process. Use this function only after you have carefully reviewed the existing resources and understand the task, and get the plan of the dataset, model, training and testing process.
   """
   merged_plan = f"""\
I have reviewed the existing resources and understand the task, and here is the plan of the dataset, model, training and testing process:

# Dataset Plan
{context_variables["dataset_plan"]}

# Model Plan
{context_variables["model_survey"]}

# Training Plan
{context_variables["training_plan"]}

# Testing Plans
{context_variables["testing_plan"]}
"""
   return merged_plan

@register_agent("get_coding_plan_agent")
def get_coding_plan_agent(model: str, **kwargs):
    code_env: DockerEnv = kwargs.get("code_env", None)
    def instructions(context_variables):
      working_dir = context_variables.get("working_dir", None)
      return f"""\
You are a Machine Learning Expert tasked with creating a detailed implementation plan for innovative ML projects.

AVAILABLE RESOURCES:
1. User's innovative idea
2. Reference codebases (in `/{working_dir}`) selected by the `Prepare Agent`
3. Comprehensive notes from the `Survey Agent` (to be used as model plan)

WORKFLOW:
1. Code Review Phase
   - Use `gen_code_tree_structure` to understand codebase structure
   - Use `read_file` to examine specific implementations
   - Document key implementation patterns and useful components
   - Use `terminal_page_down`, `terminal_page_up` and `terminal_page_to` to scroll the terminal output when it is too long.
2. Planning Phase
   Must include these components:
   a. Dataset Plan (`plan_dataset`)
      - Dataset Description
      - Dataset Location
      - Task Definition
      - Data loading pipeline
         - Read data step
         - Data preprocessing step
         - Data dataloader step

   b. Model Plan (from Survey Agent's notes)
      - Math formula
      - Implementation details
      - Reference codebases
      - Reference papers

   c. Training Plan (`plan_training`)
      - Training pipeline
      - Loss functions
      - Optimization strategy
      - Training configurations
      - Monitoring and logging

   d. Testing Plan (`plan_testing`)
      - Test metrics
      - Test dataset preparation
      - Test code

IMPORTANT REQUIREMENTS:
1. Resource Review
   - MUST thoroughly review all provided codebases before planning
   - MUST understand the complete task scope
   - MUST analyze existing implementations for reusable components

2. Plan Generation
   - Each plan component must be detailed and actionable
   - Include specific implementation references from codebases
   - Ensure all components work together coherently

3. Testing Focus
   - Testing plan is mandatory
   - Must cover both unit tests and integration tests
   - Include specific metrics for evaluation
   - Define success criteria clearly

Your goal is to create a comprehensive, practical, and implementable plan that bridges the innovative idea with actual code implementation.
"""
    tools = [read_file, plan_dataset, plan_training, plan_testing, gen_code_tree_structure, case_resolved, terminal_page_down, terminal_page_up, terminal_page_to]
    tools = [with_env(code_env)(tool) if 'env' in signature(tool).parameters else tool for tool in tools]
    return Agent(
    name="Coding Plan Agent",
    model=model,
    instructions=instructions,
    functions=tools, 
    tool_choice = "required", 
    parallel_tool_calls = False
    )

f"""You are a Machine Learning Expert, who can help me plan the detailed coding plan of the project based on the user's innovative idea in the field of machine learning.

      You are given the user's innovative idea, some reference codebases selected by the `Prepare Agent` in the directory: `/`, and comprehensive notes explored by the `Survey Agent`. 

      I want to implement the innovative idea with the information from the reference codebases and notes. 

      Please carefully review the reference codebases, and plan the detailed coding plan for me. Note that you should use the function `gen_code_tree_structure` and `read_file` to go through and read the code in the reference codebases, and after carefully reviewing the existing resources and understand the task, use the function `plan_dataset`, `plan_training`, and `plan_testing` to plan the dataset, training, and testing process. Note that the notes by the `Survey Agent` could be regarded as the plan of the model.

      [IMPORTANT] Every plan should be generated only after you have carefully reviewed the existing resources and understand the task.

      [IMPORTANT] Testing process is always required for the project, inlcuding the test metrics, test dataset, and test code.
      """