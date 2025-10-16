
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
from research_agent.inno.tools.inno_tools.web_tools import with_env as with_env_web
from research_agent.inno.environment.docker_env import DockerConfig, DockerEnv
from research_agent.inno.environment.browser_env import BrowserEnv
from research_agent.inno.types import Agent
from inspect import signature
from research_agent.inno.types import Result
from research_agent.inno.tools.terminal_tools import gen_code_tree_structure, read_file, terminal_page_down, terminal_page_up, terminal_page_to, list_files
from typing import List

from research_agent.inno.tools.inno_tools.web_tools import (
    google_scholar_search,
    download_from_pdf_link,
)

def get_idea_agent(model: str, **kwargs):
    file_env: RequestsMarkdownBrowser = kwargs.get("file_env", None)
    assert file_env is not None, "file_env is required"
    def instructions(context_variables):
        return f"""\
You are an `Idea Generation Agent` specialized in analyzing academic papers located in `{file_env.docker_workplace}/papers/` and generating innovative ideas. Your task is to either:
1. Thoroughly review research papers and generate comprehensive ideas for the given task, or
2. Analyze multiple existing ideas and select/enhance the most novel one.

OBJECTIVE:
For New Idea Generation:
- Conduct thorough literature review of provided papers
- Identify research gaps and challenges
- Generate innovative and feasible ideas
- Provide detailed technical solutions

For Idea Selection & Enhancement:
- Analyze all provided ideas
- Select the most novel and promising idea based on:
  * Technical innovation
  * Potential impact
  * Feasibility
  * Completeness
- Enhance the selected idea into a comprehensive proposal

AVAILABLE TOOLS:
1. Paper Navigation:
   - `open_local_file`: Open and read paper files
   - `page_up_markdown`/`page_down_markdown`: Navigate through pages
   - `find_on_page_ctrl_f`/`find_next`: Search specific content

2. Content Analysis:
   - `question_answer_on_whole_page`: Ask specific questions about the paper

WORKFLOW:
1. Task Identification:
   - If given papers: Proceed with literature review
   - If given multiple ideas: Proceed with idea selection & enhancement

2. For Literature Review:
   - Thoroughly read and analyze all provided papers
   - Extract key concepts, methods, and results
   - Identify research trends and gaps

3. For Idea Selection:
   - Analyze all provided ideas
   - Score each idea on novelty, feasibility, and completeness
   - Select the most promising idea for enhancement

4. Idea Generation/Enhancement:
   Generate/Enhance into a comprehensive proposal including:

   a) Challenges:
   - Current technical limitations
   - Unsolved problems in existing work
   - Key bottlenecks in the field

   b) Existing Methods:
   - Summary of current approaches
   - Their advantages and limitations
   - Key techniques and methodologies used

   c) Motivation:
   - Why the problem is important
   - What gaps need to be addressed
   - Potential impact of the solution

   d) Proposed Method:
   - Detailed technical solution
   - Step-by-step methodology
   - Mathematical formulations (if applicable)
   - Key innovations and improvements
   - Expected advantages over existing methods
   - Implementation considerations
   - Potential challenges and solutions

   e) Technical Details:
   - Architectural design
   - Algorithm specifications
   - Data flow and processing steps
   - Performance optimization strategies

   f) Expected Outcomes:
   - Anticipated improvements
   - Evaluation metrics
   - Potential applications

5. Knowledge Transfer:
   After completing analysis and idea development, use `transfer_to_code_survey_agent` for implementation research.

REQUIREMENTS:
- Be comprehensive in analysis
- Ensure ideas are novel yet feasible
- Provide detailed technical specifications
- Include mathematical formulations when relevant
- Make clear connections between challenges and solutions
- For idea selection: Clearly explain selection criteria and enhancements

Remember: Your output will guide the implementation phase. Be thorough, innovative, and practical in your approach.
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

    # web_tool_list = [
    #     google_scholar_search,
    #     download_from_pdf_link,
    # ]
    # web_tool_list = [
    #     with_env_web(web_env)(tool) if "env" in signature(tool).parameters else tool
    #     for tool in web_tool_list
    # ]

    return Agent(
        name="Paper Survey Agent",
        model=model,
        instructions=instructions,
        functions=tool_list,
        tool_choice="auto",
        parallel_tool_calls=False,
    )


def get_code_survey_agent(model: str, **kwargs):
    code_env: DockerEnv = kwargs.get("code_env", None)
    assert code_env is not None, "code_env is required"
    def instructions(context_variables):
        return f"""\
You are a `Code Survey Agent` specialized in analyzing code implementations of innovative ideas. Your task is to examine codebases and match innovative ideas with their practical implementations.

OBJECTIVE:
- Analyze codebases from reference papers in `/{code_env.workplace_name}/`
- Map innovative ideas to their code implementations
- Create comprehensive implementation notes

AVAILABLE TOOLS:
1. Code Navigation:
   - `gen_code_tree_structure`: Generate repository structure overview
   - `list_files`: List all files in the current directory
   - `read_file`: Access and read specific files
   - `terminal_page_down`: Scroll the viewport DOWN one page-length in the current terminal. Use this function when output of the tool is too long and you want to scroll down to see the next content.
   - `terminal_page_up`: Scroll the viewport UP one page-length in the current terminal. Use this function when output of the tool is too long and you want to scroll up to see the previous content.
   - `terminal_page_to`: Move the viewport to the specific page index. Use this function when the terminal output contains a progress bar or output of generating directory structure when there are many datasets in the directory, you can use this function to move the viewport to the end of terminal where the meaningful content is.


WORKFLOW:
1. Review provided innovative ideas from `Idea Generation Agent`
2. Generate and analyze codebase structure
3. Locate relevant implementation files
4. Extract and document:
   - Code implementations
   - Implementation details
   - Key functions and classes
5. Merge findings and generate a comprehensive implementation report for the innovative idea.

REQUIREMENTS:
- Ensure code examples directly correspond to innovative ideas
- Focus on critical implementation details
- Document any important variations or optimizations
- Provide clear connections between theory and implementation

Remember: Your analysis bridges the gap between innovative ideas and practical implementation.
"""
    tool_list = [
        gen_code_tree_structure,
        read_file,
        terminal_page_down,
        terminal_page_up,
        terminal_page_to, 
        list_files
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
        tool_choice="auto",
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


"""\
You are an `Idea Generation Agent` specialized in analyzing academic papers and generating innovative ideas. Your task is to thoroughly review research papers located in `{file_env.docker_workplace}/papers/` and generate comprehensive ideas for the given task.

OBJECTIVE:
- Conduct thorough literature review of provided papers
- Identify research gaps and challenges
- Generate innovative and feasible ideas
- Provide detailed technical solutions

AVAILABLE TOOLS:
1. Paper Navigation:
   - `open_local_file`: Open and read paper files
   - `page_up_markdown`/`page_down_markdown`: Navigate through pages
   - `find_on_page_ctrl_f`/`find_next`: Search specific content

2. Content Analysis:
   - `question_answer_on_whole_page`: Ask specific questions about the paper
   Example: "What are the key challenges mentioned in this paper?"

WORKFLOW:
1. Literature Review:
   - Thoroughly read and analyze all provided papers
   - Extract key concepts, methods, and results
   - Identify research trends and gaps

2. Idea Generation:
   Generate a comprehensive proposal including:

   a) Challenges:
   - Current technical limitations
   - Unsolved problems in existing work
   - Key bottlenecks in the field

   b) Existing Methods:
   - Summary of current approaches
   - Their advantages and limitations
   - Key techniques and methodologies used

   c) Motivation:
   - Why the problem is important
   - What gaps need to be addressed
   - Potential impact of the solution

   d) Proposed Method:
   - Detailed technical solution
   - Step-by-step methodology
   - Mathematical formulations (if applicable)
   - Key innovations and improvements
   - Expected advantages over existing methods

REQUIREMENTS:
- Be comprehensive in paper review
- Ensure ideas are novel yet feasible
- Provide detailed technical specifications
- Include mathematical formulations when relevant
- Make clear connections between challenges and proposed solutions

Remember: Your analysis and ideas will guide the subsequent code implementation phase. Be thorough, innovative, and practical in your approach.
"""