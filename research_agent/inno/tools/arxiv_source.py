import urllib.parse
import feedparser
import time
import requests
import re
import tarfile
import os
from typing import List


def search_arxiv(query, max_results=10):
    """
    search arxiv papers
    
    Args:
        query (str): search keyword
        max_results (int): max return results
        
    Returns:
        list: list of papers info
    """
    # API URL 구축
    base_url = 'http://export.arxiv.org/api/query?'

    
    # API 매개변수 설정
    params = {
        'search_query': f'ti:{query}',
        'start': 0,
        'max_results': max_results,
        'sortBy': 'relevance',
        'sortOrder': 'descending'
    }
    
    # 전체 쿼리 URL 생성
    query_url = base_url + urllib.parse.urlencode(params)
    
    # 요청 전송 및 결과 파싱
    response = feedparser.parse(query_url)
    
    # 논문 정보 추출
    papers = []
    for entry in response.entries:
        paper = {
            'title': entry.title,
            'author': [author.name for author in entry.authors],
            'published': entry.published,
            'summary': entry.summary,
            'url': entry.link,
            'pdf_url': next(link.href for link in entry.links if link.type == 'application/pdf')
        }
        papers.append(paper)
        
        # API 속도 제한 준수
        time.sleep(0.5)
    
    return papers

def extract_tex_content(tar_path, ):
    """
    Extract all .tex file contents from a tar.gz archive.

    Args:
        tar_path: path to the tar.gz file

    Returns:
        str: concatenated contents of all .tex files, each prefixed with its filename
    """
    try:
        all_content = []
        
        with tarfile.open(tar_path, 'r:gz') as tar:
            # 모든 .tex 파일 가져오기
            tex_files = [f for f in tar.getmembers() if f.name.endswith('.tex')]
            
            for tex_file in tex_files:
                # 파일 내용 추출
                f = tar.extractfile(tex_file)
                if f is not None:
                    try:
                        # utf-8로 디코딩 시도
                        content = f.read().decode('utf-8')
                    except UnicodeDecodeError:
                        # utf-8 실패 시 latin-1 시도
                        f.seek(0)
                        content = f.read().decode('latin-1')
                    
                    # 파일명과 내용 추가
                    all_content.append(f"\n{'='*50}\nFilename: {tex_file.name}\n{'='*50}\n")
                    all_content.append(content)
                    all_content.append("\n\n")
        
        # 모든 내용을 하나의 문자열로 결합
        return "".join(all_content)
    
    except Exception as e:
        return f"Extract failed with error: {str(e)}"

def download_arxiv_source(arxiv_url, local_root, workplace_name, title: str):
    """
    download arxiv paper source file
    
    Args:
        arxiv_url: arxiv paper url, e.g. 'http://arxiv.org/abs/2006.11239v2'
        local_root: local root directory
        workplace_name: workplace name
    """
    try:
        # URL에서 논문 ID 추출
        paper_id = re.search(r'abs/([^/]+)', arxiv_url).group(1)
        
        # 소스 URL 생성
        source_url = f'http://arxiv.org/src/{paper_id}'
        
        # 요청보내기
        response = requests.get(source_url)
        
        # 상태 코드 확인
        if response.status_code == 200:
            try: 
                paper_src_dir = os.path.join(local_root, workplace_name, "paper_source")
                os.makedirs(paper_src_dir, exist_ok=True)
                filepath = os.path.join(paper_src_dir, f"{title.replace(' ', '_').lower()}.tar.gz")
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                tex_content = extract_tex_content(filepath)
                paper_tex_dir = os.path.join(local_root, workplace_name, "papers")
                os.makedirs(paper_tex_dir, exist_ok=True)
                with open(os.path.join(paper_tex_dir, f"{title.replace(' ', '_').lower()}.tex"), 'w') as f:
                    f.write(tex_content)
                return {"status": 0, "message": f"Download paper '{title}' successfully", "path": f"/{workplace_name}/papers/{title.replace(' ', '_').lower()}.tex"}
            except Exception as e:
                return {"status": -1, "message": f"Download paper '{title}' failed with error: {str(e)}", "path": None}
        else:
            return {"status": -1, "message": f"Download paper '{title}' failed with HTTP status code {response.status_code}", "path": None}
            
    except Exception as e:
        return {"status": -1, "message": f"Download paper '{title}' failed with error: {str(e)}", "path": None}







# 유사도 함수 새로 추가 - 두 제목이 얼마나 비슷한지 0.0~1.0 숫자로 계산
def _title_similarity(a: str, b: str) -> float:
    """Compute word-overlap Jaccard similarity between two titles (case-insensitive)."""
    stop = {"a", "an", "the", "of", "in", "on", "for", "and", "with", "to", "from", "is", "are"}
    def tokenize(s):
        return set(re.sub(r'[^\w\s]', '', s.lower()).split()) - stop  # 특수문자 제거, 대소문자 무시, 의미없는 단어 제거
    wa = tokenize(a)
    wb = tokenize(b)
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)  # Jaccard 유사도: 공통 단어 수 ÷ 전체 단어 수





def _search_best_match(title: str, max_results: int = 5):
    """
    Attempts multiple search strategies sequentially to return the most similar paper.
    Returns: (best_paper dict, similarity float, used_strategy str)
    If all strategies fail, returns (None, 0.0, "").
    """
    stop = {"a", "an", "the", "of", "in", "on", "for", "and", "with", "to", "from", "is", "are"}

    def key_words(t):
        # 불용어 제거 후 핵심 단어만 추출
        words = re.sub(r'[^\w\s]', '', t.lower()).split()
        return [w for w in words if w not in stop]

    # arxiv API(Solr)에서 하이픈은 NOT 연산자로 해석되므로 공백으로 치환
    safe_title = title.replace("-", " ")

    strategies = []

    # 전략 1: 제목 전체로 ti: 검색 (하이픈 → 공백)
    strategies.append(("full title (ti:)", f"ti:{safe_title}"))

    # 전략 2: 핵심 단어 앞 3개로 ti: 검색 (부제목 등 노이즈 제거)
    kw = key_words(safe_title)
    if len(kw) >= 2:
        short_query = " ".join(kw[:3])
        strategies.append(("short keywords (ti:)", f"ti:{short_query}"))

    # 전략 3: 전체 필드(all:) 검색 — ti:에 없는 논문도 포함
    strategies.append(("all fields (all:)", f"all:{safe_title}"))

    best_paper, best_sim, best_strategy = None, 0.0, ""


    base_url = 'http://export.arxiv.org/api/query?'

    for strategy_name, query in strategies:
        params = {
            'search_query': query,
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending',
        }
        response = feedparser.parse(base_url + urllib.parse.urlencode(params))
        papers = []
        for entry in response.entries:
            papers.append({
                'title': entry.title,
                'author': [a.name for a in entry.authors],
                'published': entry.published,
                'summary': entry.summary,
                'url': entry.link,
                'pdf_url': next(l.href for l in entry.links if l.type == 'application/pdf'),
            })
            time.sleep(0.3)

        if not papers:
            continue

        candidate = max(papers, key=lambda p: _title_similarity(p['title'], title))
        sim = _title_similarity(candidate['title'], title)

        if sim > best_sim:
            best_paper, best_sim, best_strategy = candidate, sim, strategy_name

        # 충분히 좋은 결과면 더 이상 시도하지 않음
        if best_sim >= 0.6:
            break

    return best_paper, best_sim, best_strategy





def download_arxiv_source_by_title(paper_list: List[str], local_root: str, workplace_name: str):
    """
    download arxiv paper source file by title
    
    Args:
        title: paper title
        paper_dir: paper directory
    """
    ret_msg = []
    for title in paper_list:

        best_paper, similarity, strategy = _search_best_match(title, max_results=5)

        if best_paper is None:
            ret_msg.append(f"Cannot find the paper '{title}' in arxiv (all search strategies exhausted).")
            continue
        
        # 완전 다른 논문. 다운로드 안함, 경고만 출력
        if similarity < 0.3:
            ret_msg.append(
                f"WARNING: Could not find a close match for '{title}' in arxiv. "
                f"Best candidate was '{best_paper['title']}' (similarity={similarity:.2f}). "
                f"Skipping download to avoid saving the wrong paper."
            )
            continue

        # 애매함. 일단 다운로드 하되 경고 출력
        if similarity < 0.6:
            ret_msg.append(
                f"WARNING: Weak title match for '{title}'. "
                f"Closest arxiv result: '{best_paper['title']}' (similarity={similarity:.2f}). "
                f"Proceeding with download but please verify."
            )

        # 정상 다운로드
        download_info = download_arxiv_source(best_paper['url'], local_root, workplace_name, title)

        # 다운로드 결과 메시지에 매칭 정보 추가
        if download_info["status"] == -1:
            ret_msg.append(download_info["message"])
        else:
            msg = (
                download_info["message"]
                + f"\nMatched arxiv title: '{best_paper['title']}' (similarity={similarity:.2f})"
                + f"\nThe paper is downloaded to path: {download_info['path']}"
            )
            ret_msg.append(msg)

    return "\n".join(ret_msg)
    