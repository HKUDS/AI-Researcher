# from .code_knowledge import gen_code_tree_structure
# from .execution import execute_command
# from .files import read_file, create_file, write_file, list_files, create_directory
# from .PythonAction import run_python
# from .rag_code import code_rag
# from .tool_retriever import get_api_doc
# from .rag_code_tree import code_tree_rag
# from .inner import case_resolved
# from .code_report import check_tool, check_agent
# from .github_ops import get_current_branch, get_diff, push_changes, submit_pull_request

# import os
# import importlib
# from metachain.registry import registry

# # 获取当前目录下的所有 .py 文件
# current_dir = os.path.dirname(__file__)
# for file in os.listdir(current_dir):
#     if file.endswith('.py') and not file.startswith('__'):
#         module_name = file[:-3]
#         importlib.import_module(f'metachain.tools.{module_name}')

# # 导出所有注册的工具
# globals().update(registry.tools)

# __all__ = list(registry.tools.keys())

import os
import importlib
from research_agent.inno.registry import registry

def import_tools_recursively(base_dir: str, base_package: str):
    """Recursively import all tools in .py files
    
    Args:
        base_dir: the root directory to start searching
        base_package: the base name of the Python package
    """
    for root, dirs, files in os.walk(base_dir):
        # get the relative path to the base directory
        rel_path = os.path.relpath(root, base_dir)
        
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                # build the module path
                if rel_path == '.':
                    # in the root directory
                    module_path = f"{base_package}.{file[:-3]}"
                else:
                    # in the subdirectory
                    package_path = rel_path.replace(os.path.sep, '.')
                    module_path = f"{base_package}.{package_path}.{file[:-3]}"
                
                try:
                    importlib.import_module(module_path)
                except Exception as e:
                    print(f"Warning: Failed to import {module_path}: {e}")

# get the current directory and import all tools
current_dir = os.path.dirname(__file__)
import_tools_recursively(current_dir, 'research_agent.inno.tools')

# export all tool creation functions
globals().update(registry.tools)

__all__ = list(registry.tools.keys())