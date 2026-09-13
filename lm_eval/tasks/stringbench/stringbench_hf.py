"""HuggingFace datasets loading script for StringBench.

StringLLM: Understanding the String Processing Capability of Large Language Models
Paper: https://arxiv.org/abs/2410.01208 (ICLR 2025)

Reconstruction of the untracked `/home/StringLLM/stringbench_hf.py` that the TMMC evals
used. Behaviour is identical; the only change is that the data is fetched from the public
upstream repo instead of a hard-coded local checkout. Answers are derived by executing
each item's reference `solution` snippet, exactly as the original did (so upstream items
whose snippet fails yield "ERROR: ..." answers, which are unscoreable).
"""

import datasets
import json
import os
import re

_DESCRIPTION = "StringBench: A benchmark for evaluating LLM string processing capability"
_HOMEPAGE = "https://github.com/wxl-lxw/StringLLM"
_LICENSE = "MIT"

# Public upstream data; override with STRINGLLM_DATA_DIR=<local dir with {type}.json> if offline.
_UPSTREAM = "https://raw.githubusercontent.com/wxl-lxw/StringLLM/main/data/test"

STRING_TYPES = ['hash', 'multilingual', 'random_string']
TASKS = ['all', 'indexing', 'slicing', 'length', 'count', 'contain', 'reverse', 'find']


def execute_solution(solution_code: str, variables: dict) -> str:
    """Execute the Python solution code to get the answer."""
    code = solution_code.replace('```python', '').replace('```', '').strip()
    code = re.sub(r'print\s*\(.*\)', '', code).strip()
    local_vars = dict(variables)
    try:
        exec(code, {}, local_vars)
        return str(local_vars.get('answer', ''))
    except Exception as e:  # noqa: BLE001 - faithful to the original loader
        return f"ERROR: {e}"


def format_query(query_template: str, variables: dict) -> str:
    """Format the query template with variable values."""
    result = query_template
    for key, value in variables.items():
        result = result.replace(f'{{{key}+1}}', str(value + 1) if isinstance(value, int) else str(value))
        result = result.replace(f'{{{key}}}', str(value))
    return result


class StringBenchConfig(datasets.BuilderConfig):
    def __init__(self, string_type: str, task_filter: str = None, **kwargs):
        name = f"{string_type}_{task_filter}" if task_filter else string_type
        super().__init__(name=name, version=datasets.Version("1.0.0"), **kwargs)
        self.string_type = string_type
        # 'all' means no filter
        self.task_filter = None if task_filter == 'all' else task_filter


class StringBench(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        StringBenchConfig(string_type=stype, task_filter=task)
        for stype in STRING_TYPES for task in TASKS
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({
                "prompt": datasets.Value("string"),
                "answer": datasets.Value("string"),
                "task": datasets.Value("string"),
            }),
            homepage=_HOMEPAGE,
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager):
        local_dir = os.environ.get("STRINGLLM_DATA_DIR")
        if local_dir:
            data_path = os.path.join(local_dir, f"{self.config.string_type}.json")
        else:
            data_path = dl_manager.download(f"{_UPSTREAM}/{self.config.string_type}.json")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"data_path": data_path, "task_filter": self.config.task_filter},
            ),
        ]

    def _generate_examples(self, data_path, task_filter):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data not found: {data_path}")
        with open(data_path, 'r') as f:
            raw_data = json.load(f)

        idx = 0
        for item in raw_data:
            if task_filter:
                if 'manipulations' not in item or task_filter not in item['manipulations']:
                    continue
            query_template = item['query'][0]
            variables = item['variables']
            prompt = format_query(query_template, variables)
            answer = execute_solution(item['solution'], variables)
            yield idx, {
                'prompt': prompt,
                'answer': answer,
                'task': item.get('manipulations', ['unknown'])[0] if item.get('manipulations') else 'unknown',
            }
            idx += 1
