import numpy as np
import argparse
import os
import asyncio
import global_state
from dotenv import load_dotenv
from argparse import Namespace




def init_ai_researcher():
    pass

def get_args_research(): 
    args = Namespace()
    return args

def get_args_paper():
    args = Namespace()
    return args

def main_ai_researcher(input, reference, mode):
    # if main_autoagent.mode is None:
    #     main_autoagent.mode = mode
        
    # if main_autoagent.mode != mode:
    #     model = COMPLETION_MODEL
    #     main_autoagent.mode = mode
    #     global_state.INIT_FLAG = False

    # Default values
    category = "vq"
    instance_id = "rotation_vq"
    task_level = "task1"
    container_name = "paper_eval"
    workplace_name = "workplace"
    cache_path = "cache"
    port = 12356
    max_iter_times = 0

    match mode:
        case 'Detailed Idea Description':
            # global INIT_FLAG
            if global_state.INIT_FLAG is False:
                global_state.INIT_FLAG = True
                try:
                    current_file_path = os.path.realpath(__file__)
                    current_dir = os.path.dirname(current_file_path)
                    sub_dir = os.path.join(current_dir, "research_agent")
                    os.chdir(sub_dir)

                    from research_agent.constant import COMPLETION_MODEL
                    from research_agent import run_infer_idea, run_infer_plan

                    args = get_args_research()
                    # category="vq"
                    # instance_id="rotation_vq"
                    args.instance_path = f"../benchmark/final/{category}/{instance_id}.json"
                    args.task_level = task_level
                    args.model = COMPLETION_MODEL
                    args.container_name = container_name
                    args.workplace_name = workplace_name
                    args.cache_path = cache_path
                    args.port = port
                    args.max_iter_times = max_iter_times
                    args.category = category

                    run_infer_plan.main(args, input, reference)
                except Exception as e:
                    print(f"Error in Detailed Idea Description mode: {str(e)}")
                    # Continue execution even if there's an error
                    pass
                finally:
                    global_state.INIT_FLAG = False
        case 'Reference-Based Ideation':
            # clear_screen()
            if global_state.INIT_FLAG is False:
                global_state.INIT_FLAG = True
                try:
                    current_file_path = os.path.realpath(__file__)
                    current_dir = os.path.dirname(current_file_path)
                    sub_dir = os.path.join(current_dir, "research_agent")
                    os.chdir(sub_dir)

                    from research_agent.constant import COMPLETION_MODEL
                    from research_agent import run_infer_idea, run_infer_plan
                    from research_agent.constant import COMPLETION_MODEL
                    args = get_args_research()
                    # category="vq"
                    # instance_id="one_layer_vq"
                    # args.instance_path = f"../benchmark/final/{category}/{instance_id}.json"
                    # args.container_name = "paper_eval"
                    # args.task_level = "task1"
                    # args.model = COMPLETION_MODEL
                    # args.workplace_name = "workplace"
                    # args.cache_path = "cache"
                    # args.port = 12356
                    # args.max_iter_times = 0


                    args.instance_path = f"../benchmark/final/{category}/{instance_id}.json"
                    args.container_name = container_name
                    args.task_level = task_level
                    args.model = COMPLETION_MODEL
                    args.workplace_name = workplace_name
                    args.cache_path = cache_path
                    args.port = port
                    args.max_iter_times = max_iter_times
                    args.category = category

                    run_infer_idea.main(args, reference)
                except Exception as e:
                    print(f"Error in Reference-Based Ideation mode: {str(e)}")
                    # Continue execution even if there's an error
                    pass
                finally:
                    global_state.INIT_FLAG = False
        case 'Paper Generation Agent':
            # clear_screen()
            if global_state.INIT_FLAG is False:
                global_state.INIT_FLAG = True
                try:
                    from paper_agent import writing
                    args = get_args_paper()

                    research_field=category
                    # instance_id="rotated_vq"
                    args.research_field = research_field
                    args.instance_id = instance_id

                    asyncio.run(writing.writing(args.research_field, args.instance_id))
                except Exception as e:
                    print(f"Error in Paper Generation Agent mode: {str(e)}")
                    # Continue execution even if there's an error
                    pass
                finally:
                    global_state.INIT_FLAG = False
