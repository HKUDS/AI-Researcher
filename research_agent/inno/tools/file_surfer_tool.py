from research_agent.inno.environment.markdown_browser import RequestsMarkdownBrowser
from functools import partial, update_wrapper
from inspect import signature
from typing import Tuple
import time
from research_agent.inno.registry import register_tool
from typing import Optional
from research_agent.inno.types import Result
import requests
import mimetypes
import base64
import uuid
import os
from research_agent.inno.checkpoint import completion
from research_agent.constant import COMPLETION_MODEL, API_BASE_URL
def with_env(env: RequestsMarkdownBrowser):
    """将env注入到工具函数中的装饰器"""
    def decorator(func):
        def wrapped(*args, **kwargs):
            return func(env=env, *args, **kwargs)
        
        # 保留原始函数的所有属性
        update_wrapper(wrapped, func)
        # 修改signature，移除env参数
        wrapped.__signature__ = signature(func).replace(
            parameters=[p for p in signature(func).parameters.values() if p.name != 'env']
        )
        return wrapped
    return decorator

def _get_browser_state(env: RequestsMarkdownBrowser) -> Tuple[str, str]:
    """
    Get the current state of the browser, including the header and content.
    """
    # print(env.address)
    header = f"Address: {env._convert_local_to_docker(env.address)}\n"
    # header = f"Address: {env.address}\n"

    if env.page_title is not None:
        header += f"Title: {env.page_title}\n"

    current_page = env.viewport_current_page
    total_pages = len(env.viewport_pages)

    address = env.address
    for i in range(len(env.history) - 2, -1, -1):  # Start from the second last
        if env.history[i][0] == address:
            header += f"You previously visited this page {round(time.time() - env.history[i][1])} seconds ago.\n"
            break
    prefix = f"Your browser is currently open to the page '{env.page_title}'\n" if env.page_title is not None else ""
    
    header = prefix + header
    header += f"Viewport position: Showing page {current_page+1} of {total_pages}.\n"
    return (header, env.viewport)

@register_tool("open_local_file")
def open_local_file(env: RequestsMarkdownBrowser, path: str):
    """
    Open a local file at a path in the text-based browser and return current viewport content.

    Args:
        path: The absolute path of a local file to visit.
    """
    try: 
        # assert DOCKER_WORKPLACE_NAME in path, f"The path must be a absolute path from `/{DOCKER_WORKPLACE_NAME}/` directory"
        # local_path = path.replace('/' + DOCKER_WORKPLACE_NAME, LOCAL_ROOT + f'/{DOCKER_WORKPLACE_NAME}')
        # print(local_path)
        path = env._convert_docker_to_local(path)
        env.open_local_file(path)
        header, content = _get_browser_state(env)
        final_response = header.strip() + "\n=======================\n" + content
        return final_response
    except Exception as e:
        return f"Error in `open_local_file`: {e}"
    
@register_tool("page_up_markdown")
def page_up_markdown(env: RequestsMarkdownBrowser):
    """
    Scroll the viewport UP one page-length in the current file and return the new viewport content.
    """
    try: 
        env.page_up()
        header, content = _get_browser_state(env)
        final_response = header.strip() + "\n=======================\n" + content
        return final_response
    except Exception as e:
        return f"Error in `page_up`: {e}"
    
@register_tool("page_down_markdown")
def page_down_markdown(env: RequestsMarkdownBrowser):
    """
    Scroll the viewport DOWN one page-length in the current file and return the new viewport content.
    """
    try: 
        env.page_down()
        header, content = _get_browser_state(env)
        final_response = header.strip() + "\n=======================\n" + content
        return final_response
    except Exception as e:
        return f"Error in `page_down`: {e}"
    
@register_tool("find_on_page_ctrl_f")
def find_on_page_ctrl_f(env: RequestsMarkdownBrowser, search_string: str):
    """
    Scroll the viewport to the first occurrence of the search string. This is equivalent to Ctrl+F.

    Args:
        search_string: The string to search for on the page. This search string supports wildcards like '*'
    """
    try: 
        env.find_on_page(search_string)
        header, content = _get_browser_state(env)
        final_response = header.strip() + "\n=======================\n" + content
        return final_response
    except Exception as e:
        return f"Error in `find_on_page_ctrl_f`: {e}"
    
@register_tool("find_next")
def find_next(env: RequestsMarkdownBrowser):
    """
    Scroll the viewport to next occurrence of the search string.
    """
    try: 
        env.find_next()
        header, content = _get_browser_state(env)
        final_response = header.strip() + "\n=======================\n" + content
        return final_response
    except Exception as e:
        return f"Error in `find_next`: {e}" 

def _encode_image(image_path: str, env: RequestsMarkdownBrowser):
    """
    Encode an image to base64.
    """
    if image_path.startswith("http"):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        request_kwargs = {
            "headers": {"User-Agent": user_agent},
            "stream": True,
        }

        # Send a HTTP request to the URL
        response = requests.get(image_path, **request_kwargs)
        response.raise_for_status()
        content_type = response.headers.get("content-type", "")

        extension = mimetypes.guess_extension(content_type)
        if extension is None:
            extension = ".download"
    
        fname = str(uuid.uuid4()) + extension
        download_path = os.path.abspath(os.path.join(env.local_workplace, "downloads", fname))

        with open(download_path, "wb") as fh:
            for chunk in response.iter_content(chunk_size=512):
                fh.write(chunk)

        image_path = download_path
    else: 
        image_path = env._convert_docker_to_local(image_path)
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
@register_tool("visualizer")
def visualizer(env: RequestsMarkdownBrowser, image_path: str, question: Optional[str] = None) -> Result:
    """
    A tool that can answer questions about attached images.
    Args:
        image_path: The path to the image on which to answer the question. This should be a local path to downloaded image.
        question: the question to answer (default: "Please write a detailed caption for this image.")
    """
    try:
        if not question:
            question = "Please write a detailed caption for this image."
        
        if not isinstance(image_path, str):
            raise Exception("You should provide only one string as argument to this tool!")

        base64_image = _encode_image(image_path, env)

        ret_str = question

        msg = [{"role": "user", "content": [
            {"type": "text", "text": question},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
        ]}]
        res = completion(model=COMPLETION_MODEL, messages=msg)
        ret_str = res.choices[0].message.content
        return Result(
            value=ret_str,
            # image=base64_image
        )
    except Exception as e:
        return Result(
            value=f"Error in `visualizer`: {e}",
        )

def question_answer_on_whole_page(env: RequestsMarkdownBrowser, question: str) -> str:
    """
    Ask a question on the whole page and return the answer.
    """
    try: 

        retrieved_content = env.retrieve_on_page(question)
        mathnote = r"""\
Note that if you need to write mathematical formulas in your answer:
1. DO NOT use any custom \newcommand shortcuts from the paper
2. Instead, expand all custom commands to their full LaTeX form, for example:
   - Change \bx to \mathbf{x}
   - Change \E to \mathbb{E}
   - Change \grad to \nabla
3. Only use standard LaTeX commands that are built-in
4. Make sure your formulas are self-contained and can be compiled without any custom definitions

For example, if the paper uses "\bx \sim \pdata", write it as "\mathbf{x} \sim p_{\mathrm{data}}" instead.
"""
        wrap_ques = f"""\
I am reading a paper. I have a question about the paper. 
The question is: {question}
I have retrieved the following content from the paper:
{retrieved_content}
Please answer my question based on the content.
{mathnote}
        """
        msg = [{"role": "user", "content": [
            {"type": "text", "text": wrap_ques}
        ]}]
        res = completion(model=COMPLETION_MODEL, messages=msg, base_url=API_BASE_URL)
        answer = res.choices[0].message.content
        return answer
    except FileNotFoundError as e:
        return f"Before ask a question on the whole page, you must use `open_local_file` to open a file first."
    except Exception as e:
        return f"Error in `question_answer_on_whole_page`: {e}"


if __name__ == "__main__":
    local_root = os.getcwd()
    os.environ["COMPLETION_MODEL"] = "deepseek/deepseek-chat"

    workplace_name = 'workplace_meta'
    env = RequestsMarkdownBrowser(viewport_size=1024 * 5, local_root=local_root, workplace_name=workplace_name, downloads_folder=os.path.join(local_root, workplace_name, "downloads"))
    print("Open file", "~"*100)
    print(open_local_file(env, f"/{workplace_name}/denoising_diffusion_implicit_models.tex"))
    print("Question answer on whole page", "~"*100)
    
    print(question_answer_on_whole_page(env, f"Please give me the formula of the ddim model. And compare it with the ddpm model mathematically."))
    # print(visualizer("/workplace_meta/downloads/workflow.png").image)
    # print(visualizer("/workplace_meta/downloads/workflow.png", "What is the main idea of this paper?").image)