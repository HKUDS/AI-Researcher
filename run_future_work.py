import argparse
import asyncio
import os
from research_agent.run_infer_idea import InnoFlow
from research_agent.inno.environment.markdown_browser import RequestsMarkdownBrowser
 
 
def get_args():
    parser = argparse.ArgumentParser(description="Extract future work proposals from research papers")
    
    # nargs="+" → 공백으로 구분된 여러 제목을 리스트로 받음
    # required=True → 필수 인자
    parser.add_argument("--papers", nargs="+", required=True, help="Paper titles (10-15 papers)")
    
    parser.add_argument("--model", type=str, default="gpt-4o-2024-08-06")

    # GitHub 검색 시 이 날짜 이후 생성된 레포지토리만 검색
    # 너무 오래된 구현은 제외하기 위해
    parser.add_argument("--date_limit", type=str, default="2025-01-01", help="Date limit for GitHub search (YYYY-MM-DD)")
    
    parser.add_argument("--workplace_name", type=str, default="workplace")
    
    parser.add_argument("--cache_path", type=str, default="cache_future_work")
    return parser.parse_args()
 
 
def main():
    args = get_args()

    # 논문 다운로드 파일들이 저장될 로컬 폴더
    # 실행하면 프로젝트 루트에 workplace_future_work/ 폴더 자동 생성됨
    local_root = os.path.join(os.getcwd(), "workplace_future_work")
    os.makedirs(local_root, exist_ok=True)
 
    # idea_agent가 open_local_file 도구로 로컬 파일을 열 때 사용하는 브라우저
    # local_root를 알아야 "papers/논문제목.tex" 경로로 파일을 찾을 수 있음
    file_env = RequestsMarkdownBrowser(
        viewport_size=1024 * 4,
        local_root=local_root,
        workplace_name=args.workplace_name,
        downloads_folder=os.path.join(local_root, args.workplace_name, "downloads"),
    )
    flow = InnoFlow(
        cache_path=args.cache_path,
        model=args.model,
        file_env=file_env,
    )
    asyncio.run(flow(
        paper_titles=args.papers,
        date_limit=args.date_limit,
        local_root=local_root,
        workplace_name=args.workplace_name,
    ))
 
 
if __name__ == "__main__":
    main()