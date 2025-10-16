TASK = r"Develop new reasoning techniques for math reasoning tasks."

DATASET = r"""
The datasets for math reasoning: \textbf{MATH-500} (a test set of 500 math reasoning tasks), you can load the dataset using the following code:

\begin{verbatim}
from datasets import load_dataset

test_dataset = list(
        load_dataset(
            "HuggingFaceH4/MATH-500", "default", split="test", trust_remote_code=True
        )
    )
\end{verbatim}
"""

BASELINE = r"""
DeepSeek-Chat (i.e., Deepseek v3 model)
"""

COMPARISON = r"""
DeepSeek-Chat: 73.80% (pass@1)
"""

EVALUATION = r"""
pass@1 means the success rate of the first choice of the output of the model. you can refer to get_score.py to get the score of the model.
"""

REF = r"""
The exmaple of math reasoning on MATH-500 dataset is in the directory `/workplace/dataset_candidate/math_reasoning`: 
# Reasoning on MATH-500

Reasoning on MATH-500 dataset with DeepSeek Chat.

```bash
cd /path/to/math_reasoning
python run_infer.py 
```

Args:

- `--save_dir`: The directory to save the results.
- `--model`: The model to use.
- `--base_url`: The base URL of the API.
- `--limit`: The number of tasks to process.
- `--stride`: The stride of the tasks to process.
- `--offset`: The offset of the tasks to process.

Use the OpenAI-compatible API of DeepSeek Chat.

## Get score

```bash
python get_score.py --save_dir evaluation_results/math500/math500_deepseek-chat
```

Args:

- `--save_dir`: The directory to save the results.

The API key of DeepSeek Chat is in the directory `/workplace/dataset_candidate/math_reasoning/.env`, that is `sk-d4656d7459264eb8acf55848081cf6bc`. Other models are not supported.

[IMPORTANT]
1. Note that for reasoning tasks, DO NOT follow the directory structure with `training`, `testing`, etc. Construct the directory structure similar to `math_reasoning`. Focus on the reasoning techniques, and refer to the exmaple of `math_reasoning` for more details.
2. First evaluate with limit 10 tasks to make sure the model is working, and then evaluate with limit 500 tasks.
"""