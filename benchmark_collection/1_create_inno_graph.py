import json
import os
import string
import asyncio
from typing import List, Dict, Any, Tuple
from pathlib import Path
import time
from datetime import datetime, timedelta
import logging
from benchmark_collection.utils.pdf_utils import read_pdf, truncate_text
from benchmark_collection.utils.openai_utils import GPTClient

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('innovation_graph.log'),
        logging.StreamHandler()
    ]
)

def clean_title(title: str) -> str:
    """Replace all punctuation with spaces and clean up multiple spaces"""
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    cleaned = title.translate(translator)
    cleaned = ' '.join(cleaned.split())
    return cleaned

def format_time(seconds: float) -> str:
    """Convert seconds to human readable time string"""
    return str(timedelta(seconds=int(seconds)))

def setup_logging() -> str:
    """Setup logging directory and return log file path"""
    log_dir = "innovation_graph/logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(log_dir, f"llm_output_{timestamp}.log")

def log_output(log_file: str, paper_title: str, step: int, prompt: str, response: str):
    """Log LLM interaction details"""
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*80}\n")
        f.write(f"Paper: {paper_title}\n")
        f.write(f"Step: {step}\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"\n----- Prompt -----\n")
        f.write(prompt)
        f.write(f"\n----- Response -----\n")
        f.write(response)
        f.write(f"\n{'='*80}\n")

def find_pdf_file(title: str, pdf_dir: str) -> str:
    """Find PDF file by paper title"""
    cleaned_title = ' '.join(''.join(
        char if char not in string.punctuation else ' ' 
        for char in title).split()).lower()
    
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
    
    # Try exact match first
    for pdf_file in pdf_files:
        if pdf_file.lower() == cleaned_title + '.pdf':
            return os.path.join(pdf_dir, pdf_file)
    
    # Try partial match
    for pdf_file in pdf_files:
        pdf_name = os.path.splitext(pdf_file)[0].lower()
        if cleaned_title in pdf_name or pdf_name in cleaned_title:
            return os.path.join(pdf_dir, pdf_file)
    
    return None

async def process_step(client: GPTClient, step_num: int, paper: Dict, 
                      overall_instruction: str, step_instruction: str,
                      pdf_text: str, previous_results: Dict = None,
                      log_file: str = None) -> Dict:
    """Process one step of paper analysis"""
    try:
        logging.info(f"Step {step_num}/5: Analyzing paper content...")
        
        # Construct prompt
        metadata_str = json.dumps(paper, indent=2)
        prompt = f"{overall_instruction}\n\n{step_instruction}\n\nPaper Metadata:\n{metadata_str}\n\nPaper Content:\n{pdf_text}"
        
        if previous_results and step_num > 1:
            prev_results_str = json.dumps(previous_results, indent=2)
            prompt += f"\n\nResults from previous steps:\n{prev_results_str}"
            
        prompt = truncate_text(prompt, max_tokens=128000)
        
        # Add system prompt
        system_prompt = f"""You are an expert in analyzing research papers.
        You are now performing Step {step_num} of the analysis process.
        Provide your response in the exact JSON format specified in the instruction."""
        
        prompt = system_prompt + "\n\n" + prompt
        
        # Get response from LLM
        response = (await client.chat(prompt, temperature=0.7)).strip()
        if response.startswith('```json'):
            response = response[7:]
        elif response.startswith('```'):
            response = response[3:]
        if response.endswith('```'):
            response = response[:-3]
        response = response.strip()
        
        if response is None:
            logging.error(f"No response from LLM for paper: {paper['title']} (Step {step_num})")
            return None
            
        if log_file:
            log_output(log_file, paper['title'], step_num, prompt, response)

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logging.error(f"Failed to parse LLM response for paper: {paper['title']} (Step {step_num})")
            return None
            
    except Exception as e:
        logging.error(f"Error processing Step {step_num} for {paper['title']}: {str(e)}")
        return None

def load_instructions() -> Dict[str, str]:
    """Load all instruction files"""
    instructions = {}
    instruction_files = [
        ("overall", "prompts/create_innovation_graph_instruction_overall.md"),
        ("step1", "prompts/create_innovation_graph_instruction_step1.md"),
        ("step2", "prompts/create_innovation_graph_instruction_step2.md"),
        ("step3", "prompts/create_innovation_graph_instruction_step3.md"),
        ("step4", "prompts/create_innovation_graph_instruction_step4.md"),
        ("step5", "prompts/create_innovation_graph_instruction_step5.md"),
        ("task1", "prompts/create_innovation_task_instruction_task1.md"),
        ("task2", "prompts/create_innovation_task_instruction_task2.md")
    ]
    
    for name, filepath in instruction_files:
        try:
            instructions[name] = load_instruction(filepath)
        except FileNotFoundError:
            logging.warning(f"Instruction file {filepath} not found")
            instructions[name] = ""
            
    return instructions

async def process_tasks(client: GPTClient, paper: Dict, instructions: Dict[str, str], 
                       pdf_text: str, log_file: str) -> Dict:
    """Process task-specific analysis for a paper"""
    task_results = {}
    
    for task_id in ["task1", "task2"]:
        if not instructions[task_id]:
            continue
            
        try:
            prompt = f"{instructions[task_id]}\n\nPaper Content:\n{pdf_text}"
            prompt = truncate_text(prompt, max_tokens=128000)
            
            response = (await client.chat(prompt, temperature=0.7)).strip()
            if response.startswith('```json'):
                response = response[7:]
            elif response.startswith('```'):
                response = response[3:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()
            
            if response:
                log_output(log_file, paper["title"], f"task-{task_id}", prompt, response)
                task_results[task_id] = response
            else:
                logging.error(f"No response from LLM for {paper['title']} ({task_id})")
                return None
                
            await asyncio.sleep(5)
            
        except Exception as e:
            logging.error(f"Error in {task_id} for {paper['title']}: {str(e)}")
            return None
            
    return task_results

async def process_paper(client: GPTClient, paper: Dict, instructions: Dict[str, str], 
                       pdf_dir: str, log_file: str) -> Dict:
    """Process a single paper through all analysis steps and tasks"""
    try:
        # Find and read PDF
        pdf_path = find_pdf_file(paper["title"], pdf_dir)
        if pdf_path is None:
            logging.error(f"PDF not found for paper: {paper['title']}")
            return None
            
        pdf_text = read_pdf(pdf_path)
        results = {}
        
        # Process innovation graph steps
        for step in range(1, 6):
            step_key = f"step{step}"
            logging.info(f"Processing {step_key} for paper: {paper['title']}")
            
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    step_result = await process_step(
                        client, step, paper, instructions["overall"],
                        instructions[step_key], pdf_text, results, log_file
                    )
                    
                    if step_result is not None:
                        results[step_key] = step_result
                        await asyncio.sleep(5)
                        break
                    
                except Exception as e:
                    logging.error(f"Attempt {attempt + 1} failed for step {step}: {str(e)}")
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 5
                        logging.info(f"Waiting {wait_time} seconds before retry...")
                        await asyncio.sleep(wait_time)
                    else:
                        logging.error(f"All attempts failed for step {step}")
                        return None
            
            if step_key not in results:
                return None

        # Process additional tasks
        task_results = await process_tasks(client, paper, instructions, pdf_text, log_file)
        if task_results is None:
            return None
            
        # Create final result
        final_result = {
            "target": paper["title"],
            "source_papers": results["step5"]["top_papers"]
        }
        final_result.update({k: paper[k] for k in paper if k != 'title'})
        final_result.update(task_results)  # Add task results
        
        return final_result
        
    except Exception as e:
        logging.error(f"Error processing {paper['title']}: {str(e)}")
        return None

def load_anonymization_templates() -> Tuple[str, str]:
    """Load templates for model name extraction and anonymization"""
    with open("prompts/anonymize_target_paper_extract_model_name.md", "r") as f:
        extract_template = f.read()
    with open("prompts/anonymize_target_paper_instruction.md", "r") as f:
        anonymize_template = f.read()
    return extract_template, anonymize_template

async def extract_model_name(client: GPTClient, template: str, paper_title: str, pdf_text: str) -> str:
    """Extract model name from paper content"""
    try:
        # Use first quarter of the paper for model name extraction
        content_sample = pdf_text[:len(pdf_text)//4]
        prompt = f"{template}\n\nPaper Title: {paper_title}\n\nContent:\n{content_sample}"
        
        response = await client.chat(prompt)
        return response if response else "NO MODEL NAME FOUND"
    except Exception as e:
        logging.error(f"Error extracting model name: {str(e)}")
        return "NO MODEL NAME FOUND"

async def anonymize_text(client: GPTClient, template: str, model_name: str, 
                        paper_title: str, text: str) -> str:
    """Anonymize text content"""
    try:
        prompt = f"{template}\n\nModel: {model_name}\nPaper: {paper_title}\nContent:\n{text}"
        response = await client.chat(prompt)
        return response if response != "NO NEED TO PROCESS" else text
    except Exception as e:
        logging.error(f"Error anonymizing text: {str(e)}")
        return text

async def anonymize_paper(client: GPTClient, paper: Dict, pdf_text: str,
                         extract_template: str, anonymize_template: str) -> Dict:
    """Anonymize a paper and its source papers"""
    try:
        model_name = await extract_model_name(client, extract_template, paper["target"], pdf_text)
        anonymized_paper = paper.copy()
        
        # Anonymize task results
        for task_id in ["task1", "task2"]:
            if task_id in paper:
                anonymized_paper[task_id] = await anonymize_text(
                    client, anonymize_template, model_name, 
                    paper["target"], paper[task_id]
                )
                await asyncio.sleep(3)
        
        # Anonymize source papers
        for i, source in enumerate(paper["source_papers"]):
            anonymized_source = source.copy()
            for field in ["usage", "justification"]:
                if field in source:
                    anonymized_source[field] = await anonymize_text(
                        client, anonymize_template, model_name,
                        paper["target"], source[field]
                    )
                    await asyncio.sleep(3)
            anonymized_paper["source_papers"][i] = anonymized_source
        
        return anonymized_paper
    except Exception as e:
        logging.error(f"Error anonymizing paper {paper['target']}: {str(e)}")
        return paper

def filter_self_references(papers: List[Dict]) -> Tuple[List[Dict], Dict]:
    """Filter out self-references and return statistics"""
    filtered_papers = []
    self_ref_counts = {}
    total_self_refs = 0
    
    for paper in papers:
        filtered_paper = paper.copy()
        target_title = paper["target"]
        
        # Split into self-refs and non-self-refs
        non_self_refs = []
        self_refs = 0
        
        for source in paper["source_papers"]:
            if source["reference"].lower().strip() == target_title.lower().strip():
                self_refs += 1
            else:
                non_self_refs.append(source)
        
        if self_refs > 0:
            self_ref_counts[target_title] = self_refs
            total_self_refs += self_refs
        
        filtered_paper["source_papers"] = non_self_refs
        filtered_papers.append(filtered_paper)
    
    stats = {
        "papers_with_self_refs": len(self_ref_counts),
        "total_self_refs": total_self_refs,
        "details": self_ref_counts
    }
    
    return filtered_papers, stats

async def main():
    # Setup paths and directories
    input_file = Path("paper_titles/paper_titles.json")
    pdf_dir = Path("paper_titles/pdfs")
    output_dir = Path("innovation_graph")
    output_dir.mkdir(exist_ok=True)
    
    # Setup checkpointing
    checkpoint_dir = output_dir / "checkpoints"
    checkpoint_dir.mkdir(exist_ok=True)
    checkpoint_path = checkpoint_dir / "processed_papers.json"
    
    # Setup logging
    log_file = setup_logging()
    logging.info(f"Logging LLM interactions to: {log_file}")
    
    # Load all instructions including tasks
    instructions = load_instructions()

    # Load papers
    with open(input_file) as f:
        papers = json.load(f)
    
    # Initialize results and processed papers
    results = []
    processed_papers = set()
    
    # Load existing results if any
    output_path = output_dir / "innovation_graph.json"
    if output_path.exists():
        with open(output_path) as f:
            results = json.load(f)
            processed_papers = {result['target'] for result in results}
            logging.info(f"Loaded {len(results)} existing results")
    
    # Load checkpoint if exists
    if checkpoint_path.exists():
        with open(checkpoint_path) as f:
            checkpoint_data = json.load(f)
            processed_papers.update(checkpoint_data.get('failed_papers', []))
            logging.info(f"Loaded {len(checkpoint_data.get('failed_papers', []))} failed papers from checkpoint")

    # Initialize GPT client and counters
    client = GPTClient()
    failed_papers = []
    remaining_papers = [p for p in papers if p['title'] not in processed_papers]
    
    # Process papers
    start_time = time.time()
    for i, paper in enumerate(remaining_papers):
        logging.info(f"\nProcessing paper {i+1}/{len(remaining_papers)}: {paper['title']}")
        
        try:
            result = await process_paper(client, paper, instructions, pdf_dir, log_file)
            
            if result is not None:
                results.append(result)
                # Save results after each successful processing
                with open(output_path, 'w') as f:
                    json.dump(results, f, indent=2)
            else:
                failed_papers.append(paper['title'])
            
            # Update checkpoint
            with open(checkpoint_path, 'w') as f:
                json.dump({
                    'last_processed_index': i,
                    'failed_papers': failed_papers
                }, f, indent=2)
            
            await asyncio.sleep(5)
            
        except Exception as e:
            logging.error(f"Failed to process paper: {paper['title']}")
            logging.error(f"Error: {str(e)}")
            failed_papers.append(paper['title'])
            continue
    
    # Log final statistics
    total_time = time.time() - start_time
    logging.info(f"\nProcessing complete:")
    logging.info(f"Total time: {format_time(total_time)}")
    logging.info(f"Successfully processed: {len(results)} papers")
    logging.info(f"Failed to process: {len(failed_papers)} papers")
    logging.info(f"Results saved to {output_path}")

    if results:
        # Save initial results
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        logging.info(f"Innovation graph results saved to {output_path}")
        
        # Load anonymization templates
        extract_template, anonymize_template = load_anonymization_templates()
        
        # Anonymize papers
        anonymized_results = []
        for paper in results:
            pdf_path = pdf_dir / f"{clean_title(paper['target'])}.pdf"
            if pdf_path.exists():
                pdf_text = read_pdf(str(pdf_path))
                anonymized_paper = await anonymize_paper(
                    client, paper, pdf_text,
                    extract_template, anonymize_template
                )
                anonymized_results.append(anonymized_paper)
                logging.info(f"Anonymized paper: {paper['target']}")
            else:
                logging.error(f"PDF not found for anonymization: {paper['target']}")
                anonymized_results.append(paper)
        
        # Save anonymized results
        anonymized_path = output_dir / "innovation_graph_anonymized.json"
        with open(anonymized_path, 'w') as f:
            json.dump(anonymized_results, f, indent=2)
        logging.info(f"Anonymized results saved to {anonymized_path}")
        
        # Filter self-references
        filtered_results, stats = filter_self_references(anonymized_results)
        
        # Log filtering statistics
        logging.info("\nSelf-reference statistics:")
        logging.info(f"Papers with self-references: {stats['papers_with_self_refs']}")
        logging.info(f"Total self-references found: {stats['total_self_refs']}")
        logging.info("\nDetails of self-references by paper:")
        for paper, count in stats['details'].items():
            logging.info(f"{paper}: {count} self-reference(s)")
        
        # Save filtered results
        filtered_path = output_dir / "innovation_graph_final.json"
        with open(filtered_path, 'w') as f:
            json.dump(filtered_results, f, indent=2)
        logging.info(f"Final filtered results saved to {filtered_path}")

def load_instruction(filepath: str) -> str:
    """Load instruction from file"""
    with open(filepath, 'r') as f:
        return f.read().strip()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Process interrupted by user")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
