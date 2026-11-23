import argparse
import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

import global_state


PROJECT_DIR = Path(__file__).resolve().parent
ENV_FILE = PROJECT_DIR / ".env"
DEFAULT_CATEGORY = "vq"
DEFAULT_INSTANCE_ID = "one_layer_vq"


def init_ai_researcher():
    a = 1


def get_args_research(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance_path", type=str, default="benchmark/final/vq/one_layer_vq.json")
    parser.add_argument("--container_name", type=str, default="paper_eval")
    parser.add_argument("--task_level", type=str, default="task1")
    parser.add_argument("--model", type=str, default="gpt-4o-2024-08-06")
    parser.add_argument("--workplace_name", type=str, default="workplace")
    parser.add_argument("--cache_path", type=str, default="cache")
    parser.add_argument("--port", type=int, default=12345)
    parser.add_argument("--max_iter_times", type=int, default=0)
    parser.add_argument("--category", type=str, default=DEFAULT_CATEGORY)
    return parser.parse_args(argv)


def get_args_paper(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--research_field", type=str, default=os.getenv("CATEGORY") or DEFAULT_CATEGORY)
    parser.add_argument("--instance_id", type=str, default=os.getenv("INSTANCE_ID") or DEFAULT_INSTANCE_ID)
    return parser.parse_args(argv)


def _get_env_int(name, default):
    value = os.getenv(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError as error:
        raise ValueError(f"{name} must be an integer. Check your .env or environment.") from error


def main_ai_researcher(input, reference, mode):
    if global_state.INIT_FLAG:
        return

    previous_dir = Path.cwd()
    global_state.INIT_FLAG = True
    try:
        load_dotenv(ENV_FILE)
        match mode:
            case "Detailed Idea Description" | "Reference-Based Ideation":
                args = get_args_research([])
                args.category = os.getenv("CATEGORY") or DEFAULT_CATEGORY
                instance_id = os.getenv("INSTANCE_ID") or DEFAULT_INSTANCE_ID
                args.instance_path = str(PROJECT_DIR / "benchmark" / "final" / args.category / f"{instance_id}.json")
                args.task_level = os.getenv("TASK_LEVEL") or args.task_level
                args.container_name = os.getenv("CONTAINER_NAME") or args.container_name
                args.workplace_name = os.getenv("WORKPLACE_NAME") or args.workplace_name
                args.cache_path = os.getenv("CACHE_PATH") or args.cache_path
                args.port = _get_env_int("PORT", args.port)
                args.max_iter_times = _get_env_int("MAX_ITER_TIMES", args.max_iter_times)

                os.chdir(PROJECT_DIR / "research_agent")
                from research_agent.constant import COMPLETION_MODEL

                args.model = COMPLETION_MODEL
                if mode == "Detailed Idea Description":
                    from research_agent import run_infer_plan

                    run_infer_plan.main(args, input, reference)
                else:
                    from research_agent import run_infer_idea

                    run_infer_idea.main(args, reference)
            case "Paper Generation Agent":
                os.chdir(PROJECT_DIR)
                from paper_agent import writing

                args = get_args_paper([])
                asyncio.run(writing.writing(args.research_field, args.instance_id))
    finally:
        os.chdir(previous_dir)
        global_state.INIT_FLAG = False
