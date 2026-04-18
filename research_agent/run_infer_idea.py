import json
from research_agent.inno.workflow.flowcache import FlowModule, ToolModule, AgentModule

# 필요 없는 import지우고 기존에 합쳐져있던 import 중 필요한 것만 import
from research_agent.inno.tools.inno_tools.code_search import search_github_repos
from research_agent.inno.agents.inno_agent.idea_agent import get_idea_agent

from research_agent.inno.tools.arxiv_source import download_arxiv_source_by_title
from tqdm import tqdm

# 사용하는 모델 안내 추가
from research_agent.constant import CHEEP_MODEL
from research_agent.inno.environment.markdown_browser import RequestsMarkdownBrowser
import asyncio
import argparse
import os

# Any형식 제거
from typing import List, Dict, Union
from research_agent.inno.logger import MetaChainLogger


# 실현가능성 탐색을 위해 github_search는 남겨둠.
def github_search(metadata: Dict) -> str:
    github_result = ""
    for source_paper in tqdm(metadata["source_papers"]):
        github_result += search_github_repos(metadata, source_paper["reference"], 10)
        github_result += "*"*30 + "\n"
    return github_result

class InnoFlow(FlowModule):
    def __init__(self, cache_path: str, log_path: Union[str, None, MetaChainLogger] = None, model: str = "gpt-4o-2024-08-06", file_env: RequestsMarkdownBrowser = None):
        super().__init__(cache_path, log_path, model)
        self.git_search = ToolModule(github_search, cache_path)

        # 논문 제목을 가지게 되면 그걸 arxiv에 검색해서 논문전문을 다운로드 / idea_agent 사용.
        self.download_paper = ToolModule(download_arxiv_source_by_title, cache_path)
        self.idea_agent = AgentModule(get_idea_agent(model=CHEEP_MODEL, file_env=file_env), self.client, cache_path)
 
    async def forward(self, paper_titles: List[str], date_limit: str, local_root: str, workplace_name: str, *args, **kwargs):
        references = "\n".join(f"- {t}" for t in paper_titles)


        context_variables = {
            "working_dir": workplace_name, # TODO: change to the codebase path
            "date_limit": date_limit,
            "notes": [],
        }


        # [1단계] 논문 다운로드 → 아이디어 초안 생성
        download_res = self.download_paper({
            "paper_list": paper_titles,
            "local_root": local_root,
            "workplace_name": workplace_name,
        })

        draft_query = f"""\
I have a list of research papers to analyze:
{references}

I have downloaded the papers in TeX format for reading:
{download_res}

Your task is to thoroughly analyze these papers and generate EXACTLY 5 draft future work proposals.
Focus on:
- Research gaps and unsolved problems identified in the papers
- Weaknesses and limitations of current methods
- Promising directions for follow-up research
- Topics that are novel, feasible, and underexplored

Do not assess GitHub feasibility yet — that will be done in the next step.
"""

        messages = [{"role": "user", "content": draft_query}]
        draft_messages, context_variables = await self.idea_agent(messages, context_variables)
        draft_ideas = draft_messages[-1]["content"]



        # [2단계] GitHub 검색 → 실현 가능성 검증 후 최종 출력
        metadata = {
            "source_papers": [{"reference": t} for t in paper_titles],
            "date_limit": date_limit,
        }
        github_result = self.git_search({"metadata": metadata})

        refine_query = f"""\
You previously generated 5 draft future work proposals based on paper analysis:
{draft_ideas}

Now review the GitHub search results showing what has already been implemented in related repositories:
{github_result}

Based on these results:
1. For each of the 5 proposals, assess whether it is already implemented or covered by existing work on GitHub.
2. If a proposal overlaps with existing implementations, refine it to highlight a clear differentiation point, or replace it with a more novel direction.
3. Output the final 5 future work proposals, each with an explicit feasibility note referencing the GitHub evidence.
"""

        messages = [{"role": "user", "content": refine_query}]
        final_messages, context_variables = await self.idea_agent(messages, context_variables, iter_times="refine")
        result = final_messages[-1]["content"]
        print(result)
        return result
