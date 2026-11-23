import arxiv
import json
import os
from pathlib import Path
import time
import logging
from typing import List, Dict
import requests.exceptions
import requests
from datetime import datetime
import asyncio
from typing import Dict, Optional
from collections import Counter
import string
from urllib.parse import urlparse
from benchmark_collection.utils.openai_utils import GPTClient

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('arxiv_search.log'),
        logging.StreamHandler()
    ]
)

class VenueAPI:
    def __init__(self):
        self.semantic_scholar_url = "http://api.semanticscholar.org/graph/v1/paper/search"
        self.crossref_url = "https://api.crossref.org/works"
        self.cache_file = Path('paper_titles/venue_cache.json')
        self.cache = self._load_cache()
        self.citation_cache = {}

    def _load_cache(self) -> Dict:
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logging.warning(f"Error loading cache: {str(e)}")
        return {}

    def _save_cache(self):
        try:
            self.cache_file.parent.mkdir(exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            logging.warning(f"Error saving cache: {str(e)}")

    def get_semantic_scholar_venue(self, title: str) -> str:
        try:
            params = {
                'query': title,
                'fields': 'venue,title'
            }
            response = requests.get(self.semantic_scholar_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['data'] and len(data['data']) > 0:
                    venue = data['data'][0].get('venue', '')
                    return venue if venue else ''
        except Exception as e:
            logging.warning(f"Semantic Scholar API error: {str(e)}")
        return ''

    def get_crossref_venue(self, title: str) -> str:
        try:
            params = {
                'query.title': title,
                'select': 'container-title',
                'rows': 1
            }
            headers = {
                'User-Agent': 'YourEmailAddress'
            }
            
            response = requests.get(self.crossref_url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data['message']['items']:
                    venue = data['message']['items'][0].get('container-title', [''])[0]
                    return venue if venue else ''
        except Exception as e:
            logging.warning(f"Crossref API error: {str(e)}")
        return ''

    def get_venue(self, title: str) -> Dict:
        if title in self.cache:
            return self.cache[title]

        venue_info = {
            'venue': '',
            'source': '',
            'timestamp': datetime.now().isoformat()
        }
        
        venue = self.get_semantic_scholar_venue(title)
        time.sleep(1)
        
        if venue:
            venue_info['venue'] = venue
            venue_info['source'] = 'Semantic Scholar'
        else:
            venue = self.get_crossref_venue(title)
            time.sleep(1)
            
            if venue:
                venue_info['venue'] = venue
                venue_info['source'] = 'Crossref'
            else:
                venue_info['venue'] = 'arXiv'
                venue_info['source'] = 'Default'

        self.cache[title] = venue_info
        self._save_cache()
        
        return venue_info

    def get_citations(self, title: str) -> int:
        """Get citation count from Semantic Scholar API"""
        if title in self.citation_cache:
            return self.citation_cache[title]

        try:
            params = {
                "query": title,
                "fields": "citationCount",
                "limit": 1
            }
            response = requests.get(self.semantic_scholar_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data["data"]:
                    citations = data["data"][0]["citationCount"]
                    self.citation_cache[title] = citations
                    return citations
        except Exception as e:
            logging.warning(f"Error fetching citations for {title}: {e}")
        return 0

class SearchProgress:
    def __init__(self, output_dir: Path):
        self.progress_file = output_dir / 'search_progress.json'
        self.intermediate_dir = output_dir / 'intermediate'
        self.intermediate_dir.mkdir(exist_ok=True)
        self.progress = self._load_progress()

    def _load_progress(self) -> Dict:
        try:
            if self.progress_file.exists():
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logging.warning(f"Error loading progress: {str(e)}")
        return {}

    def save_progress(self):
        try:
            with open(self.progress_file, 'w') as f:
                json.dump(self.progress, f, indent=2)
        except Exception as e:
            logging.warning(f"Error saving progress: {str(e)}")

    def is_keyword_completed(self, file_name: str, keyword: str) -> bool:
        return self.progress.get(file_name, {}).get(keyword, False)

    def mark_keyword_completed(self, file_name: str, keyword: str):
        if file_name not in self.progress:
            self.progress[file_name] = {}
        self.progress[file_name][keyword] = True
        self.save_progress()

    def save_intermediate_result(self, file_name: str, keyword: str, papers: List[Dict]):
        intermediate_file = self.intermediate_dir / f"{file_name}_{keyword.replace(' ', '_')}.json"
        try:
            result = {
                'keyword': keyword,
                'timestamp': datetime.now().isoformat(),
                'papers': papers
            }
            with open(intermediate_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error saving intermediate result: {str(e)}")

async def search_arxiv(keyword: str, venue_api: VenueAPI, exact_match: bool = True, max_results: int = 100) -> List[Dict]:
    try:
        search = arxiv.Search(
            query=keyword,
            max_results=max_results,
        )

        papers = []
        for result in search.results():
            should_include = (
                result.title.lower().strip() == keyword.lower().strip()
                if exact_match
                else True
            )
            
            if should_include:
                paper_info = {
                    'title': result.title,
                    'authors': [author.name for author in result.authors],
                    'year': result.published.year,
                    'url': result.entry_id,
                    'abstract': result.summary
                }
                
                venue_info = venue_api.get_venue(result.title)
                citations = venue_api.get_citations(result.title)
                
                paper_info.update({
                    'venue': venue_info['venue'],
                    'venue_source': venue_info['source'],
                    'venue_lookup_time': venue_info['timestamp'],
                    'citations': citations
                })
                
                papers.append(paper_info)
                if exact_match:
                    break
                elif len(papers) == 1:  # If not exact match, just get the first result
                    break

        return papers

    except Exception as e:
        logging.error(f"Error while searching for '{keyword}': {str(e)}")
        return []

async def process_input_file(file_path: Path, venue_api: VenueAPI, progress: SearchProgress, exact_match: bool = True) -> List[Dict]:
    results = []  # Changed from dict to list
    not_found = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            keywords = [line.strip() for line in f if line.strip()]
        
        for keyword in keywords:
            if progress.is_keyword_completed('initial', keyword):
                logging.info(f"Skipping already processed paper: {keyword}")
                continue
                
            logging.info(f"Searching for paper: {keyword}")
            papers = await search_arxiv(keyword, venue_api, exact_match)
            
            if papers:
                results.extend(papers)
                progress.save_intermediate_result('initial', keyword, papers)
                match_type = "exact" if exact_match else "relevant"
                logging.info(f"Found {match_type} match for paper: {keyword}")
            else:
                logging.warning(f"No match found for paper: {keyword}")
                not_found.append(keyword)
            
            progress.mark_keyword_completed('initial', keyword)
            await asyncio.sleep(3)
            
        if not_found:
            with open('papers_not_found.md', 'w', encoding='utf-8') as f:
                for title in not_found:
                    f.write(f"{title}\n")
        return results
    
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {str(e)}")
        return []

def clean_title(title: str) -> str:
    """Replace all punctuation with spaces and clean up multiple spaces"""
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    cleaned = title.translate(translator)
    cleaned = ' '.join(cleaned.split())
    return cleaned

def download_pdf(url: str, output_path: str) -> bool:
    """Download PDF from URL with error handling"""
    try:
        if 'arxiv.org' in url and not url.endswith('.pdf'):
            parsed = urlparse(url)
            paper_id = parsed.path.split('/')[-1]
            url = f"http://arxiv.org/pdf/{paper_id}.pdf"
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        if 'application/pdf' not in response.headers.get('content-type', '').lower():
            raise ValueError("URL does not point to a PDF file")
            
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    
    except Exception as e:
        logging.error(f"Error downloading {url}: {str(e)}")
        return False

async def download_papers(papers: List[Dict], output_dir: Path):
    """Download PDFs for all papers"""
    pdf_dir = output_dir / 'pdfs'
    pdf_dir.mkdir(exist_ok=True)
    
    logging.info(f"Starting download of {len(papers)} papers")
    
    for i, paper in enumerate(papers, 1):
        title = paper['title']
        url = paper['url']
        
        clean_name = clean_title(title)
        pdf_path = pdf_dir / f"{clean_name}.pdf"
        
        if pdf_path.exists():
            logging.info(f"[{i}/{len(papers)}] Already exists: {clean_name}")
            continue
            
        logging.info(f"[{i}/{len(papers)}] Downloading: {clean_name}")
        
        if download_pdf(url, str(pdf_path)):
            logging.info(f"Successfully downloaded: {clean_name}")
        else:
            logging.error(f"Failed to download: {clean_name}")
        
        await asyncio.sleep(3)

async def main():
    output_dir = Path('paper_titles')
    output_dir.mkdir(exist_ok=True)
    
    venue_api = VenueAPI()
    progress = SearchProgress(output_dir)
    
    file_path = Path('papers_to_search')
    if not file_path.exists():
        logging.error(f"Input file '{file_path}' does not exist")
        return
        
    logging.info(f"Processing file: {file_path}")
    
    results = await process_input_file(file_path, venue_api, progress, exact_match=True)
    
    if results:
        # Save search results
        output_file = output_dir / "paper_titles.json"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            logging.info(f"Results saved to {output_file}")
            
            # Download papers
            await download_papers(results, output_dir)
            
        except Exception as e:
            logging.error(f"Error saving results to {output_file}: {str(e)}")
    else:
        logging.warning("No results to save")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Process interrupted by user")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
