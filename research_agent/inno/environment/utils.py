from research_agent.inno.util import run_command_in_container
from research_agent.constant import DOCKER_WORKPLACE_NAME
import os
from pathlib import Path
import shutil

def setup_metachain():
    cmd = "pip list | grep metachain"
    response = run_command_in_container(cmd)
    if response['status'] == 0:
        print("Metachain is already installed.")
        return
    cmd = f"cd /{DOCKER_WORKPLACE_NAME}/metachain && pip install -e ."
    response = run_command_in_container(cmd)
    if response['status'] == 0:
        print("Metachain is installed.")
        return
    else:
        raise Exception(f"Failed to install metachain. {response['result']}")


def setup_dataset(category: str, local_workplace: str):
    # 构建目标路径
    dataset_candidate_path = os.path.join(local_workplace, "dataset_candidate")
    
    # 检查目标目录是否存在
    if os.path.exists(dataset_candidate_path):
        print("dataset_candidate exists")
        return
    
    # 检查源目录是否存在
    repo_dir = Path(__file__).resolve().parents[3]
    source_path = repo_dir / "benchmark" / "process" / "dataset_candidate" / category
    if not os.path.exists(source_path):
        raise Exception(f"source path {source_path} not exists")
    
    try:
        # 复制整个目录内容到 dataset_candidate
        shutil.copytree(source_path, dataset_candidate_path)
        print(f"copy {source_path} to {dataset_candidate_path} success")
    except Exception as e:
        raise Exception(f"copy {source_path} to {dataset_candidate_path} failed: {str(e)}")
