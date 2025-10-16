
from research_agent.inno.tools.file_surfer_tool import with_env as with_env_file
from research_agent.inno.tools.file_surfer_tool import (
    open_local_file,
    page_up_markdown,
    page_down_markdown,
    find_on_page_ctrl_f,
    find_next,
    visualizer,
    question_answer_on_whole_page
)
from research_agent.inno.environment.markdown_browser import RequestsMarkdownBrowser
from research_agent.inno.environment.docker_env import with_env as with_env_docker
from research_agent.inno.environment.docker_env import DockerConfig, DockerEnv
from research_agent.inno.types import Agent
from inspect import signature
from research_agent.inno.types import Result
from research_agent.inno.tools.terminal_tools import gen_code_tree_structure, read_file, terminal_page_down, terminal_page_up, terminal_page_to
from typing import List

def get_paper_survey_agent(model: str, **kwargs):
    file_env: RequestsMarkdownBrowser = kwargs.get("file_env", None)
    assert file_env is not None, "file_env is required"
    def instructions(context_variables):
        return f"""\
You are a `Paper Survey Agent` specialized in analyzing academic papers. Your task is to extract and analyze specific academic concepts from research papers located in `{file_env.docker_workplace}/papers/`.

OBJECTIVE:
- Analyze the provided academic definition
- Extract relevant mathematical formulas and theoretical foundations
- Prepare comprehensive notes for the `Code Survey Agent`

AVAILABLE TOOLS:
1. Paper Navigation:
   - `open_local_file`: Open and read paper files
   - `page_up_markdown`/`page_down_markdown`: Navigate through pages
   - `find_on_page_ctrl_f`/`find_next`: Search specific content

2. Content Analysis:
   - `question_answer_on_whole_page`: Ask specific questions about the paper
   Example: "What is the math formula for Transformer?"

WORKFLOW:
1. Open and read the relevant papers
2. Search for the specified academic definition
3. Extract:
   - Formal definitions
   - Mathematical formulas
   - Key theoretical components
4. Document your findings and transfer your findings to the `Code Survey Agent` using the `transfer_to_code_survey_agent` function. Make sure you have read these papers thoroughly. YOU MUST USE THE `transfer_to_code_survey_agent` function. DO NOT use any other `transfer_...` function.

REQUIREMENTS:
- Be thorough in your analysis
- Focus on mathematical precision
- Ensure all extracted information is directly relevant to the given academic definition
- Provide clear and structured notes that can be effectively used by the Code Survey Agent

Remember: Your analysis forms the theoretical foundation for the subsequent code implementation phase.
"""
    tool_list = [
        open_local_file,
        page_up_markdown,
        page_down_markdown,
        find_on_page_ctrl_f,
        find_next,
        question_answer_on_whole_page,
    ]
    tool_list = [
        with_env_file(file_env)(tool) if "env" in signature(tool).parameters else tool
        for tool in tool_list
    ]
    return Agent(
        name="Paper Survey Agent",
        model=model,
        instructions=instructions,
        functions=tool_list,
        tool_choice="required",
        parallel_tool_calls=False,
    )


def get_code_survey_agent(model: str, **kwargs):
    code_env: DockerEnv = kwargs.get("code_env", None)
    assert code_env is not None, "code_env is required"
    def instructions(context_variables):
        return f"""\
You are a `Code Survey Agent` specialized in analyzing code implementations of academic concepts. Your task is to examine codebases and match theoretical concepts with their practical implementations.

OBJECTIVE:
- Analyze codebases from reference papers in `/{code_env.workplace_name}/`
- Map academic definitions and mathematical formulas to their code implementations
- Create comprehensive implementation notes

AVAILABLE TOOLS:
1. Code Navigation:
   - `gen_code_tree_structure`: Generate repository structure overview
   - `read_file`: Access and read specific files
   - `terminal_page_down`: Scroll the viewport DOWN one page-length in the current terminal. Use this function when output of the tool is too long and you want to scroll down to see the next content.
   - `terminal_page_up`: Scroll the viewport UP one page-length in the current terminal. Use this function when output of the tool is too long and you want to scroll up to see the previous content.
   - `terminal_page_to`: Move the viewport to the specific page index. Use this function when the terminal output contains a progress bar or output of generating directory structure when there are many datasets in the directory, you can use this function to move the viewport to the end of terminal where the meaningful content is.

2. Documentation:
   - `transfer_back_to_survey_agent`: Document findings and merge with `Paper Survey Agent`'s notes

WORKFLOW:
1. Review provided academic definitions and formulas from `Paper Survey Agent`
2. Generate and analyze codebase structure
3. Locate relevant implementation files
4. Extract and document:
   - Code implementations
   - Implementation details
   - Key functions and classes
5. Merge findings with `Paper Survey Agent`'s notes and transfer complete documentation back to `Survey Agent`using the `transfer_back_to_survey_agent` function

REQUIREMENTS:
- Ensure code examples directly correspond to theoretical concepts
- Focus on critical implementation details
- Document any important variations or optimizations
- Provide clear connections between theory and implementation

Remember: Your analysis bridges the gap between theoretical concepts and practical implementation.
"""
    tool_list = [
        gen_code_tree_structure,
        read_file,
        terminal_page_down,
        terminal_page_up,
        terminal_page_to
    ]
    tool_list = [
        with_env_docker(code_env)(tool) if "env" in signature(tool).parameters else tool
        for tool in tool_list
    ]
    return Agent(
        name="Code Survey Agent",
        model=model,
        instructions=instructions,
        functions=tool_list,
        tool_choice="required",
        parallel_tool_calls=False,
    )


def case_resolved(context_variables: dict):
    """
    After you have taken enough notes for the innovation, you should use this function to merge the notes for the further innovation.
    """
    merge_notes = "\n".join([f"## {note['definition']}\n* The math formula is:\n{note['math_formula']}\n* * The code implementation is:\n{note['code_implementation']}\n* Reference papers are:\n{note['reference_papers']}\n* Reference codebases are:\n{note['reference_codebases']}" for note in context_variables["notes"]])
    ret_val = f"""\
I have merged the notes for the innovation.
The notes are as follows:
{merge_notes}
"""
    return Result(
        value=ret_val,
        context_variables=context_variables,
    )

def get_survey_agent(model: str = "gpt-4o", **kwargs):
    file_env: RequestsMarkdownBrowser = kwargs.get("file_env", None)
    assert file_env is not None, "file_env is required"
    code_env: DockerEnv = kwargs.get("code_env", None)
    assert code_env is not None, "code_env is required"

    def instructions(context_variables):
        return f"""\
1. INPUT ANALYSIS
- You will receive a list of research papers and their corresponding codebases
- You will also receive specific innovative ideas that need to be implemented

2. ATOMIC DEFINITION BREAKDOWN
- Break down the innovative ideas into atomic academic definitions
- Each atomic definition should:
  * Be a single, self-contained concept
  * Have clear mathematical foundations
  * Be implementable in code
  * Be traceable to specific papers

3. KEY CONCEPT IDENTIFICATION
- For each atomic definition identified above, proceed with the following steps:
  a. Pass the definition to the `Paper Survey Agent` using `transfer_to_paper_survey_agent` function
  b. `Paper Survey Agent` will extract relevant academic definitions and mathematical formulas
  c. After the `Paper Survey Agent` has extracted the relevant academic definitions and mathematical formulas, `Paper Survey Agent` will use `transfer_to_code_survey_agent` function to forward the findings to the `Code Survey Agent`
  d. `Code Survey Agent` will extract corresponding code implementations
  e. After the `Code Survey Agent` has extracted the corresponding code implementations, `Code Survey Agent` will use `transfer_back_to_survey_agent` function to forward all findings to the `Survey Agent`
  f. `Survey Agent` will collect and organize the notes for each definition

4. ITERATIVE PROCESS
- Continue this process until ALL atomic definitions have been covered
- Do not conclude until you have thoroughly examined all concepts necessary for the innovation

5. FINAL COMPILATION
- Use the `case_resolved` function to merge all collected notes
- Ensure the final output is well-structured and comprehensive

IMPORTANT NOTES:
- Before proceeding with any analysis, you MUST first break down the innovative idea into atomic definitions
- Each atomic definition should be specific enough to be traced to concrete mathematical formulas and code implementations
- Do not skip or combine definitions - each atomic concept must be analyzed separately
- If you're unsure about a definition's atomicity, err on the side of breaking it down further
- Document your breakdown reasoning before proceeding with the analysis

Your goal is to create a complete knowledge base that bridges theoretical concepts with practical implementations for the proposed innovation.
"""
    paper_survey_agent = get_paper_survey_agent(model, file_env=file_env)
    code_survey_agent = get_code_survey_agent(model, code_env=code_env)
    survey_agent = Agent(
        name="Survey Agent",
        model=model,
        instructions=instructions,
        tool_choice="required",
        parallel_tool_calls=False,
    )

    def transfer_back_to_survey_agent(academic_definition: str, code_implementation: str, reference_codebases: List[str], context_variables: dict):
        """
        After you have carefully read the related paper, understood the academic definition, especially the math formula, and reviewed the corresponding code implementation, you should take notes about the specific academic definition, math formula, and code implementation for the further innovation.
        Args:
            academic_definition: the academic definition to be explored. It should be a single, atomic academic concept with a few words.
            code_implementation: the code implementation of the academic definition. [IMPORTANT] It should be as complete as possible and it should be the real code. 
            reference_codebases: the list of reference codebases. If you don't have reference codebases, you can set it to `None`.
        """
        # context_variables["notes"] = {
        #     academic_definition: {
        #         "definition": academic_definition,
        #         "math_formula": math_formula,
        #         "code_implementation": code_implementation,
        #         "references": references,
        #     }
        # }
        context_variables["notes"][-1]["code_implementation"] = code_implementation
        context_variables["notes"][-1]["reference_codebases"] = reference_codebases
        ret_val = f"""\
    I have taken notes for the innovation.
    The notes are as follows:
    ## Academic Definition
    {academic_definition}
    ## Math Formula
    {context_variables["notes"][-1]["math_formula"]}
    ## Reference papers
    {context_variables["notes"][-1]["reference_papers"]}
    ## Code Implementation
    {context_variables["notes"][-1]["code_implementation"]}
    ## Reference codebases
    {context_variables["notes"][-1]["reference_codebases"]}
    """
        return Result(
            value=ret_val,
            context_variables=context_variables,
            agent=survey_agent,
        )
    def transfer_to_paper_survey_agent(academic_definition: str, context_variables: dict):
        """
        You should pass a specific academic definition to the `Paper Survey Agent` and `Code Survey Agent` to let them find the corresponding math formula and code implementation. 
        [IMPORTANT] You can use this function only after you have use the provided tools to actually and carefully read and analyze the codebases. DONNOT use this function before you have read the codebases.
        Args:
            academic_definition: the academic definition to be explored. It should be a single, atomic academic concept with a few words.
        """
        ret_val = f"""\
You should explore the papers and extract the math formula for the academic definition: {academic_definition}.
"""
        context_variables["notes"].append({"definition": academic_definition})
        return Result(
            value=ret_val,
            agent=paper_survey_agent,
            context_variables=context_variables,
        )
    def transfer_to_code_survey_agent(academic_definition: str, math_formula: str, reference_papers: List[str], context_variables: dict):
        """
        You should pass a specific academic definition and math formula to the `Code Survey Agent` to let it find the corresponding code implementation. 
        [IMPORTANT] You can use this function only after you have use the provided tools to actually and carefully read and analyze the papers. DONNOT use this function before you have read the papers.
        Args:
            academic_definition: the academic definition to be implemented. It should be a single, atomic academic concept with a few words.
            math_formula: the full math formula to be implemented. [IMPORTANT] It should be as complete as possible and it should be the real math formula. 
            reference_papers: the list of reference papers. If you don't have reference papers, you can set it to `None`.
        """
        ret_val = f"""\
You should explore the codebases and extract the code implementation for the academic definition: {academic_definition} and math formula: {math_formula}.
"""
        context_variables["notes"][-1]["math_formula"] = math_formula
        context_variables["notes"][-1]["reference_papers"] = reference_papers
        return Result(
            value=ret_val,
            agent=code_survey_agent,
            context_variables=context_variables,
        )
    survey_agent.functions = [transfer_to_paper_survey_agent, case_resolved]
    paper_survey_agent.functions.append(transfer_to_code_survey_agent)
    code_survey_agent.functions.append(transfer_back_to_survey_agent)
    return survey_agent