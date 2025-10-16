
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
4. Document your findings and transfer your findings to the `Code Survey Agent` using the `transfer_to_code_survey_agent` function. Make sure you have read these papers thoroughly.

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

WORKFLOW:
1. Generate code structure overview
2. Identify relevant implementation files
3. Extract:
   - Code implementations matching the academic definition
   - Key algorithms and data structures
   - Implementation patterns and best practices
4. Document findings and transfer back to the `Survey Agent` using `transfer_back_to_survey_agent`

REQUIREMENTS:
- Focus on practical implementation details
- Ensure code examples are complete and runnable
- Document any modifications or adaptations needed
- Provide clear explanations of how code implements the theoretical concepts

Remember: Your analysis bridges the gap between theory and practical implementation.
"""
    tool_list = [
        gen_code_tree_structure,
        read_file,
        terminal_page_down,
        terminal_page_up,
        terminal_page_to,
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
    try:
        notes = context_variables.get("notes", [])
        if not notes:
            ret_val = "No notes found in context variables. Please ensure notes have been collected before calling case_resolved."
            return Result(
                value=ret_val,
                context_variables=context_variables,
            )
        
        merged_notes = []
        for note in notes:
            # Get values with defaults to handle missing keys
            definition = note.get('definition', 'No definition provided')
            math_formula = note.get('math_formula', 'No math formula provided')
            code_implementation = note.get('code_implementation', 'No code implementation provided')
            reference_papers = note.get('reference_papers', 'No reference papers provided')
            reference_codebases = note.get('reference_codebases', 'No reference codebases provided')
            
            note_text = f"""## {definition}
* The math formula is:
{math_formula}
* The code implementation is:
{code_implementation}
* Reference papers are:
{reference_papers}
* Reference codebases are:
{reference_codebases}"""
            merged_notes.append(note_text)
        
        merge_notes = "\n\n".join(merged_notes)
        ret_val = f"""\
I have merged the notes for the innovation.
The notes are as follows:
{merge_notes}
"""
        return Result(
            value=ret_val,
            context_variables=context_variables,
        )
    except Exception as e:
        # Fallback in case of any error
        ret_val = f"""\
Error occurred while merging notes: {str(e)}
Available context variables keys: {list(context_variables.keys())}
Notes structure: {context_variables.get('notes', 'No notes found')}
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

4. COMPREHENSIVE NOTE COLLECTION
- Ensure all notes are properly structured and complete
- Verify that each definition has:
  * Clear academic definition
  * Mathematical formulas
  * Code implementations
  * Reference papers and codebases

5. FINAL INTEGRATION
- Use `case_resolved` function to merge all collected notes
- Ensure the final output is comprehensive and ready for implementation

IMPORTANT GUIDELINES:
- Be systematic and thorough in your analysis
- Ensure each atomic definition is properly explored
- Maintain clear documentation throughout the process
- Focus on practical implementation feasibility
"""
    survey_agent = Agent(
        name="Survey Agent",
        model=model,
        instructions=instructions,
        functions=[],
        tool_choice="required",
        parallel_tool_calls=False,
    )
    paper_survey_agent = get_paper_survey_agent(model, file_env=file_env)
    code_survey_agent = get_code_survey_agent(model, code_env=code_env)

    def transfer_back_to_survey_agent(academic_definition: str, code_implementation: str, reference_codebases: List[str], context_variables: dict):
        """
        You should pass the code implementation back to the `Survey Agent` to let it collect the notes for the innovation.
        [IMPORTANT] You can use this function only after you have use the provided tools to actually and carefully read and analyze the codebases. DONNOT use this function before you have read the codebases.
        Args:
            academic_definition: the academic definition to be explored. It should be a single, atomic academic concept with a few words.
            code_implementation: the code implementation of the academic definition. [IMPORTANT] It should be as complete as possible and it should be the real code. 
            reference_codebases: the list of reference codebases. If you don't have reference codebases, you can set it to `None`.
        """
        try:
            # Ensure notes list exists
            if "notes" not in context_variables:
                context_variables["notes"] = []
            
            # Ensure the last note exists
            if not context_variables["notes"]:
                context_variables["notes"].append({"definition": academic_definition})
            
            # Update the last note with safe access
            last_note = context_variables["notes"][-1]
            last_note["code_implementation"] = code_implementation
            last_note["reference_codebases"] = reference_codebases
            
            # Get values with defaults
            math_formula = last_note.get("math_formula", "No math formula provided")
            reference_papers = last_note.get("reference_papers", "No reference papers provided")
            
            ret_val = f"""\
    I have taken notes for the innovation.
    The notes are as follows:
    ## Academic Definition
    {academic_definition}
    ## Math Formula
    {math_formula}
    ## Reference papers
    {reference_papers}
    ## Code Implementation
    {code_implementation}
    ## Reference codebases
    {reference_codebases}
    """
            return Result(
                value=ret_val,
                context_variables=context_variables,
                agent=survey_agent,
            )
        except Exception as e:
            # Fallback in case of any error
            ret_val = f"""\
    Error occurred while taking notes: {str(e)}
    Academic Definition: {academic_definition}
    Code Implementation: {code_implementation}
    Reference Codebases: {reference_codebases}
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
        try:
            # Ensure notes list exists
            if "notes" not in context_variables:
                context_variables["notes"] = []
            
            # Add new note with proper structure
            context_variables["notes"].append({
                "definition": academic_definition,
                "math_formula": "To be filled by Paper Survey Agent",
                "code_implementation": "To be filled by Code Survey Agent",
                "reference_papers": "To be filled by Paper Survey Agent",
                "reference_codebases": "To be filled by Code Survey Agent"
            })
            
            ret_val = f"""\
You should explore the papers and extract the math formula for the academic definition: {academic_definition}.
"""
            return Result(
                value=ret_val,
                agent=paper_survey_agent,
                context_variables=context_variables,
            )
        except Exception as e:
            # Fallback in case of any error
            ret_val = f"""\
Error occurred while transferring to Paper Survey Agent: {str(e)}
Academic Definition: {academic_definition}
"""
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
        try:
            # Ensure notes list exists and has at least one note
            if "notes" not in context_variables:
                context_variables["notes"] = []
            
            if not context_variables["notes"]:
                context_variables["notes"].append({"definition": academic_definition})
            
            # Update the last note with safe access
            last_note = context_variables["notes"][-1]
            last_note["math_formula"] = math_formula
            last_note["reference_papers"] = reference_papers
            
            ret_val = f"""\
You should explore the codebases and extract the code implementation for the academic definition: {academic_definition} and math formula: {math_formula}.
"""
            return Result(
                value=ret_val,
                agent=code_survey_agent,
                context_variables=context_variables,
            )
        except Exception as e:
            # Fallback in case of any error
            ret_val = f"""\
Error occurred while transferring to Code Survey Agent: {str(e)}
Academic Definition: {academic_definition}
Math Formula: {math_formula}
Reference Papers: {reference_papers}
"""
            return Result(
                value=ret_val,
                agent=code_survey_agent,
                context_variables=context_variables,
            )
    survey_agent.functions = [transfer_to_paper_survey_agent, case_resolved]
    paper_survey_agent.functions.append(transfer_to_code_survey_agent)
    code_survey_agent.functions.append(transfer_back_to_survey_agent)
    return survey_agent