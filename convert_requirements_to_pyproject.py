#!/usr/bin/env python3
"""
Script to convert requirements.txt to pyproject.toml format
"""

import re
import toml
from pathlib import Path

def parse_requirements(requirements_file):
    """Parse requirements.txt and return a list of dependencies"""
    dependencies = []
    
    with open(requirements_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Remove version constraints for pyproject.toml
                # We'll use >= for minimum versions
                if '==' in line:
                    package, version = line.split('==', 1)
                    dependencies.append(f"{package}>={version}")
                elif '>=' in line:
                    dependencies.append(line)
                elif '<=' in line:
                    # Convert <= to >= for minimum version
                    package, version = line.split('<=', 1)
                    dependencies.append(f"{package}>={version}")
                elif '<' in line:
                    # Convert < to >= for minimum version
                    package, version = line.split('<', 1)
                    dependencies.append(f"{package}>={version}")
                elif '>' in line:
                    dependencies.append(line)
                else:
                    dependencies.append(line)
    
    return dependencies

def create_pyproject_toml(dependencies):
    """Create pyproject.toml content"""
    
    # Group dependencies by category
    core_deps = []
    ai_ml_deps = []
    web_deps = []
    data_deps = []
    graph_deps = []
    util_deps = []
    
    # Define package categories
    ai_ml_packages = {
        'litellm', 'openai', 'anthropic', 'transformers', 'torch', 'torchvision', 
        'torchaudio', 'accelerate', 'datasets', 'tiktoken', 'lm_eval'
    }
    
    web_packages = {
        'gradio', 'uvicorn', 'fastapi', 'httpx', 'python-dotenv', 'python-multipart'
    }
    
    data_packages = {
        'numpy', 'pandas', 'scikit-learn', 'scipy', 'matplotlib', 'seaborn'
    }
    
    graph_packages = {
        'torch-geometric', 'torch_geometric', 'networkx'
    }
    
    util_packages = {
        'click', 'rich', 'tqdm', 'PyYAML', 'requests', 'pillow', 'pydantic'
    }
    
    for dep in dependencies:
        package = dep.split('>=')[0].split('==')[0].split('<')[0].split('>')[0]
        
        if package.lower() in ai_ml_packages:
            ai_ml_deps.append(dep)
        elif package.lower() in web_packages:
            web_deps.append(dep)
        elif package.lower() in data_packages:
            data_deps.append(dep)
        elif package.lower() in graph_packages:
            graph_deps.append(dep)
        elif package.lower() in util_packages:
            util_deps.append(dep)
        else:
            core_deps.append(dep)
    
    # Create pyproject.toml structure
    pyproject_content = {
        "build-system": {
            "requires": ["setuptools>=61.0", "wheel"],
            "build-backend": "setuptools.build_meta"
        },
        "project": {
            "name": "ai-researcher",
            "version": "1.0.0",
            "description": "AI-Researcher: Autonomous Scientific Innovation",
            "authors": [
                {"name": "AI-Researcher Team", "email": "contact@ai-researcher.com"}
            ],
            "readme": "README.md",
            "requires-python": ">=3.8",
            "dependencies": []
        },
        "project.optional-dependencies": {
            "dev": [
                "pytest>=7.0.0",
                "black>=23.0.0",
                "flake8>=6.0.0",
                "mypy>=1.0.0",
            ]
        },
        "project.urls": {
            "Homepage": "https://github.com/HKUDS/AI-Researcher",
            "Repository": "https://github.com/HKUDS/AI-Researcher",
            "Documentation": "https://autoresearcher.github.io/docs"
        }
    }
    
    # Add all dependencies
    all_deps = []
    if core_deps:
        all_deps.extend(core_deps)
    if ai_ml_deps:
        all_deps.extend(ai_ml_deps)
    if web_deps:
        all_deps.extend(web_deps)
    if data_deps:
        all_deps.extend(data_deps)
    if graph_deps:
        all_deps.extend(graph_deps)
    if util_deps:
        all_deps.extend(util_deps)
    
    pyproject_content["project"]["dependencies"] = sorted(all_deps)
    
    return pyproject_content

def main():
    requirements_file = "requirements.txt"
    pyproject_file = "pyproject.toml"
    
    if not Path(requirements_file).exists():
        print(f"❌ {requirements_file} not found!")
        return
    
    print(f"📖 Reading {requirements_file}...")
    dependencies = parse_requirements(requirements_file)
    print(f"✅ Found {len(dependencies)} dependencies")
    
    print(f"🔧 Creating {pyproject_file}...")
    pyproject_content = create_pyproject_toml(dependencies)
    
    # Write to pyproject.toml
    with open(pyproject_file, 'w') as f:
        toml.dump(pyproject_content, f)
    
    print(f"✅ Successfully created {pyproject_file}")
    print(f"📦 Total dependencies: {len(pyproject_content['project']['dependencies'])}")
    
    # Show some stats
    print("\n📊 Dependency breakdown:")
    print(f"   - Core dependencies: {len([d for d in dependencies if d.split('>=')[0].split('==')[0].split('<')[0].split('>')[0].lower() not in {'litellm', 'openai', 'anthropic', 'transformers', 'torch', 'torchvision', 'torchaudio', 'accelerate', 'datasets', 'tiktoken', 'lm_eval', 'gradio', 'uvicorn', 'fastapi', 'httpx', 'python-dotenv', 'python-multipart', 'numpy', 'pandas', 'scikit-learn', 'scipy', 'matplotlib', 'seaborn', 'torch-geometric', 'torch_geometric', 'networkx', 'click', 'rich', 'tqdm', 'PyYAML', 'requests', 'pillow', 'pydantic'}])}")
    print(f"   - AI/ML dependencies: {len([d for d in dependencies if d.split('>=')[0].split('==')[0].split('<')[0].split('>')[0].lower() in {'litellm', 'openai', 'anthropic', 'transformers', 'torch', 'torchvision', 'torchaudio', 'accelerate', 'datasets', 'tiktoken', 'lm_eval'}])}")
    print(f"   - Web dependencies: {len([d for d in dependencies if d.split('>=')[0].split('==')[0].split('<')[0].split('>')[0].lower() in {'gradio', 'uvicorn', 'fastapi', 'httpx', 'python-dotenv', 'python-multipart'}])}")
    print(f"   - Data processing: {len([d for d in dependencies if d.split('>=')[0].split('==')[0].split('<')[0].split('>')[0].lower() in {'numpy', 'pandas', 'scikit-learn', 'scipy', 'matplotlib', 'seaborn'}])}")
    print(f"   - Graph libraries: {len([d for d in dependencies if d.split('>=')[0].split('==')[0].split('<')[0].split('>')[0].lower() in {'torch-geometric', 'torch_geometric', 'networkx'}])}")

if __name__ == "__main__":
    main()
