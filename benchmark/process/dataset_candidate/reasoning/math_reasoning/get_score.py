from pathlib import Path
from tqdm import tqdm
import multiprocessing
from copy import deepcopy
import re
from lm_eval.tasks.minerva_math.utils import (
    last_boxed_only_string,
    normalize_final_answer,
    get_unnormalized_answer,
    remove_boxed,
    is_equiv,
)

import yaml
import argparse

def load_yaml(path: Path):
    with open(path, "r") as f:
        data = yaml.load(f, Loader=yaml.CLoader)

    return data


def save_yaml(path: Path, data, sort_keys=True):
    with open(path, "w") as f:
        yaml.dump(data, f, sort_keys=sort_keys)


ANS_RE_GSM8k = re.compile(r"#### (\-?[\$0-9\.\,]+)")
INVALID_ANS_GSM8k = "[invalid]"
GSM8K_IGNORE_REGEXES = [",", "\\$", "\\.$"]


def filter_ignores(st, regexes_to_ignore):
    if regexes_to_ignore is not None:
        for s in regexes_to_ignore:
            st = re.sub(s, "", st)
    return st


def extract_answer_gsm8k(completion):
    match = ANS_RE_GSM8k.search(completion)
    if match:
        match_str = match.group(1).strip()
        match_str = filter_ignores(
            match_str,
            GSM8K_IGNORE_REGEXES,
        )
        return match_str
    else:
        return INVALID_ANS_GSM8k


def is_correct_gsm8k(model_completion, gt_example):
    gt_answer = extract_answer_gsm8k(gt_example)
    assert gt_answer != INVALID_ANS_GSM8k
    model_answer = extract_answer_gsm8k(model_completion)
    return model_answer == gt_answer or is_equiv(model_answer, gt_answer)

def my_get_unnormalized_answer(og_pred):
    og_pred = get_unnormalized_answer(og_pred)
    # print(og_pred)
    og_pred = re.sub(r"\\+[\(\[](.+?)\\+[\)\]]", "\\1", og_pred)
    return og_pred
def clean_latex_string(text):
    # 替换双斜杠为单斜杠
    text = text.replace('\\\\', '\\')
    # 处理其他常见的转义字符
    text = text.replace('\\n', '\n')
    return text

def is_correct_minerva(og_pred, gt):
    og_pred = clean_latex_string(og_pred)
    pred = normalize_final_answer(my_get_unnormalized_answer(og_pred))
    # print(pred)
    # print(gt)
    # gt = normalize_final_answer(remove_boxed(last_boxed_only_string(gt)))
    # string equality check needed because of https://github.com/EleutherAI/lm-evaluation-harness/issues/2212
    return pred == gt or is_equiv(pred, gt)




def is_correct(sample: str, gt_answer: str, dset: str):
    if dset == "gsm8k":
        return is_correct_gsm8k(sample, gt_answer)
    elif dset == "math":
        return is_correct_minerva(sample, gt_answer)
    else:
        raise ValueError(f"Dataset {dset} not supported")




def get_tasks(config):
    sample_paths = Path(config.samples_dir).glob("*.yaml")

    tasks = []
    for sample_path in tqdm(sample_paths, desc="Loading generations"):
        save_path = config.save_dir / sample_path.name

        task_config = deepcopy(config)
        task_config.sample_path = sample_path
        task_config.save_path = save_path

        tasks.append(task_config)

    return tasks


def main(args):
    save_dir = Path(args.save_dir).absolute()
    
    tasks = list(save_dir.glob("*.yaml"))
    corrects = []

    for task in tqdm(tasks, desc="Evaluating"):
        result = load_yaml(task)
    
        correct = is_correct(result["answer"], result["gt_answer"], "math")
        corrects.append(correct)
        # break

    print(f"Accuracy: {sum(corrects) / len(corrects)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_dir", type=str, default="evaluation_results/math500/math500_deepseek-chat") # 0.756
    args = parser.parse_args()
    main(args)
