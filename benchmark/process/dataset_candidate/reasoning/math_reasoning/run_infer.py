import torch
from datasets import load_dataset
from tqdm import tqdm
import multiprocessing
import random
import requests
from functools import partial
import argparse
from pathlib import Path    
import yaml
import importlib
import os
import asyncio
from prompts import MATH_COT_PROMPT
from constant import *

import openai

def save_yaml(path: Path, data, sort_keys=True):
    with open(path, "w") as f:
        yaml.dump(data, f, sort_keys=sort_keys)

async def run_inference(item, save_dir, model, base_url):

    outpath = save_dir / f"{item['id']}.yaml"
    if outpath.exists():
        return

    prompt = MATH_COT_PROMPT + f"\n\nPlease answer the following math question. You should think step by step to solve it.\n\nProblem:\n{item['problem']}\n\n"
    prompt += "Please given your final answer (answer ONLY) within the format of `Final Answer: The final answer is <answer>. I hope it is correct.` after your reasoning \n"
    prompt += "For example: According to ...\nFinal Answer: The final answer is $24$. I hope it is correct.\n"

    client = openai.AsyncOpenAI(base_url=base_url)
    messages = [
        {"role": "user", "content": prompt},
    ]

    response = await client.chat.completions.create(
        model=model,
        messages=messages,
    )
    answer = response.choices[0].message.content

    out = {
        "prompt": prompt,
        "question": item["problem"],
        "answer": answer,
        "gt_answer": item["answer"],
    }

    save_yaml(outpath, out)


async def main(args):

    test_dataset = list(
        load_dataset(
            "HuggingFaceH4/MATH-500", "default", split="test", trust_remote_code=True
        )
    )

    print(f"Number of test items: {len(test_dataset)}")

    random.seed(12345)


    for i, data in enumerate(test_dataset):
        data["id"] = i

    random.shuffle(test_dataset)

    if args.limit is not None:
        limit = args.limit
    else:
        limit = len(test_dataset)

    if args.stride is not None:
        stride = args.stride
    else:
        stride = 1

    if args.offset is not None:
        offset = args.offset
    else:
        offset = 0

    test_dataset = test_dataset[offset:limit:stride]

    print(f"Total number of items to process: {len(test_dataset)}")

    save_dir = os.path.join(args.save_dir, "math500" + "_" + args.model)
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    predictions = []
    for item in tqdm(test_dataset):
        predictions.append(await run_inference(item, save_dir, args.model, args.base_url))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--stride", type=int, default=None)
    parser.add_argument("--offset", type=int, default=None)
    parser.add_argument("--save_dir", type=str, default="evaluation_results/math500")
    parser.add_argument("--model", type=str, default="deepseek-chat")
    parser.add_argument("--base_url", type=str, default="https://api.deepseek.com")
    args = parser.parse_args()
    asyncio.run(main(args))
