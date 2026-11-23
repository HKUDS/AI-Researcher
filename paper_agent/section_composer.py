import os
import json
import logging
from pathlib import Path
from datetime import datetime
import random
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from benchmark_collection.utils.openai_utils import GPTClient


def setup_logging(research_field):
    os.makedirs(f"{research_field}/temp", exist_ok=True)
    os.makedirs(f"{research_field}/target_sections", exist_ok=True)
    os.makedirs(f"{research_field}/methodology_checkpoints", exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'{research_field}/methodology_composition.log'),
            logging.StreamHandler()]
    )

class SectionComposer(ABC):
    def __init__(self, research_field: str, section_name: str, structure_iterations: int = 3, gpt_model='gpt-4o-mini-2024-07-18'):
        self.gpt_client = GPTClient(model=gpt_model)
        self.structure_iterations = structure_iterations
        self.research_field = research_field
        self.section_name = section_name
        
        # Create necessary directories
        self.setup_directories()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def setup_directories(self):
        """Set up necessary directories for the composer"""
        directories = [
            f"{self.research_field}/temp",
            f"{self.research_field}/target_sections",
            f"{self.research_field}/{self.section_name}_checkpoints",
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            


    def write_temp_log(self, content: str, step: str):
        """Write intermediate results to temporary log file"""
        filename = f"{self.research_field}/temp/{self.timestamp}_{step}.log"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        logging.info(f"Written intermediate result to {filename}")

    def get_checkpoint_path(self, target_paper: str) -> str:
        """Get checkpoint directory path for the target paper"""
        normalized_title = self.normalize_title(target_paper)
        return f"{self.research_field}/{self.section_name}_checkpoints/{normalized_title}"

    def save_checkpoint(self, target_paper: str, step: str, data: dict):
        """Save checkpoint data"""
        checkpoint_dir = self.get_checkpoint_path(target_paper)
        os.makedirs(checkpoint_dir, exist_ok=True)
        
        checkpoint_file = os.path.join(checkpoint_dir, f"{step}.json")
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        logging.info(f"Saved checkpoint: {checkpoint_file}")

    def load_checkpoint(self, target_paper: str, step: str) -> Optional[Dict]:
        """Load checkpoint data if exists"""
        checkpoint_file = os.path.join(
            self.get_checkpoint_path(target_paper), 
            f"{step}.json"
        )
        if os.path.exists(checkpoint_file):
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def normalize_title(self, title: str) -> str:
        """Normalize title for file naming"""
        return '_'.join(title.lower().split())

    def load_benchmark_data(self, json_path: str, target_paper: str) -> List[Dict]:
        """Load source papers from benchmark data"""
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        for item in data:
            if item['target'].lower() == target_paper.lower():
                return item['source_papers']
        return []

    def get_random_template(self) -> str:
        """Randomly select a writing template from the templates directory"""
        relative_dir = Path(self.research_field) / "writing_templates" / self.section_name
        template_files = list(relative_dir.glob("*_template.txt"))
        if not template_files:
            bundled_dir = Path(__file__).resolve().parent / relative_dir
            template_files = list(bundled_dir.glob("*_template.txt"))
        if not template_files:
            logging.warning("No templates found. Will proceed without template.")
            return ""
        
        selected_template = random.choice(template_files)
        try:
            return selected_template.read_text(encoding="utf-8")
        except Exception as e:
            logging.error(f"Error reading template {selected_template}: {str(e)}")
            return ""

    @abstractmethod
    async def generate_or_revise_structure(self, content: str, current_structure: str, iteration: int) -> str:
        """Generate or revise section structure"""
        pass

    @abstractmethod
    async def detailize_subsection(self, structure: str, current_text: str, content: str, subsection: str) -> str:
        """Detail out a specific subsection"""
        pass

    @abstractmethod
    async def final_writing_checklist(self, section_text: str) -> str:
        """Final revision checklist"""
        pass

    async def fuse_subsections(self, structure: str, subsection_contents: Dict[str, str]) -> str:
        """Fuse all subsections into one complete section"""
        prompt = f"""Combine the following subsections into a complete {self.section_name} section according to the established structure.
    The content of each subsection MUST BE PRESERVED EXACTLY as provided.

    Established structure:
    {structure}

    Subsection contents:
    {json.dumps(subsection_contents, indent=2)}

    Requirements:
    1. STRICT CONTENT PRESERVATION:
    - Keep ALL content within each subsection exactly as provided
    - Maintain all LaTeX commands, equations, and formatting
    - Preserve all citations and references

    2. STRUCTURE ADHERENCE:
    - Follow the established structure exactly
    - Include all section/subsection/subsubsection headers
    - Maintain the hierarchy of sections
    - Keep all comments from the structure

    3. FUSION GUIDELINES:
    - Only add necessary LaTeX formatting for proper section combination
    - Do not modify any technical content
    - Ensure proper spacing between sections
    - Maintain consistent formatting throughout

    Output the complete {self.section_name} section with all subsections properly combined."""

        return await self.gpt_client.chat(prompt=prompt)

    @abstractmethod
    async def compose_section(self, agent_dir: str, model_dir: str, benchmark_path: str, target_paper: str) -> str:
        """Main method to compose the section"""
        pass
