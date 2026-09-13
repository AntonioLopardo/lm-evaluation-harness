"""HuggingFace datasets loading script for the EXECUTE benchmark.

EXECUTE: Expandable X(cross)-lingual Extension of CUTE
Paper: https://aclanthology.org/2025.findings-acl.95/

Reconstruction of the untracked `/home/execute_benchmark/execute_hf.py` that the TMMC evals
used. Behaviour is identical; data is fetched from the public upstream repo instead of a
hard-coded local checkout.

Data format (per language dir `data/tasks/<lang>/`):
  * `<task>.tsv`   — header row with `input1[, input2, ...]` and `label` columns
  * `prompts.pkl`  — dict  task -> ONE shared few-shot preamble string ending in a
                     `Question: ... "{}" ...` template with `{}` placeholders.
                     The prompt is `preamble.format(*inputs)`. (The `execute_dataset.py`
                     that ships in the harness indexes this dict as `[task][i]`, which
                     returns a single character; that is a bug in the shipped builder.)
Emits `answer` (not `label`), which is what the task yamls' doc_to_target reads.
"""

import os
import pickle
from pathlib import Path

import datasets

_DESCRIPTION = """
EXECUTE is a multilingual extension of the CUTE benchmark that tests LLMs'
character-level understanding across multiple languages with diverse scripts.
"""

_CITATION = """
@inproceedings{edman2025execute,
  title={EXECUTE: A Multilingual Benchmark for LLM Token Understanding},
  author={Edman, Lukas and Schmid, Helmut and Fraser, Alexander},
  booktitle={Findings of ACL},
  year={2025}
}
"""

# Public upstream data; override with EXECUTE_DATA_DIR=<local data/tasks dir> if offline.
_UPSTREAM = "https://raw.githubusercontent.com/Leukas/EXECUTE/main/data/tasks"

_LANGUAGES = ["amh", "ara", "deu", "eng", "hin", "jpn", "kor", "rus", "spa", "zho"]
_TASKS = [
    'spell', 'spell_inverse', 'contains_char', 'contains_word',
    'ins_char', 'ins_word', 'del_char', 'del_word',
    'sub_char', 'sub_word', 'swap_char', 'swap_word',
]
_CONFIGS = [f"{lang}_{task}" for lang in _LANGUAGES for task in _TASKS]


class ExecuteConfig(datasets.BuilderConfig):
    def __init__(self, lang: str, task: str, **kwargs):
        super().__init__(name=f"{lang}_{task}", **kwargs)
        self.lang = lang
        self.task = task


class Execute(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        ExecuteConfig(lang=c.split("_")[0], task="_".join(c.split("_")[1:]), description=f"EXECUTE {c}")
        for c in _CONFIGS
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({
                "prompt": datasets.Value("string"),
                "answer": datasets.Value("string"),
            }),
            supervised_keys=None,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        lang, task = self.config.lang, self.config.task
        local_dir = os.environ.get("EXECUTE_DATA_DIR")
        if local_dir:
            tsv_path = Path(local_dir) / lang / f"{task}.tsv"
            prompts_path = Path(local_dir) / lang / "prompts.pkl"
        else:
            tsv_path = Path(dl_manager.download(f"{_UPSTREAM}/{lang}/{task}.tsv"))
            prompts_path = Path(dl_manager.download(f"{_UPSTREAM}/{lang}/prompts.pkl"))
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"tsv_path": str(tsv_path), "prompts_path": str(prompts_path), "task": task},
            ),
        ]

    def _generate_examples(self, tsv_path, prompts_path, task):
        template = ""
        if os.path.exists(prompts_path):
            with open(prompts_path, 'rb') as f:
                prompt_templates = pickle.load(f)
            template = prompt_templates.get(task, "")

        with open(tsv_path, 'r', encoding='utf-8') as f:
            header = f.readline().rstrip('\n').split('\t')
            for idx, line in enumerate(f):
                parts = line.rstrip('\n').split('\t')
                if len(parts) < len(header):
                    continue
                row = {header[i]: parts[i] for i in range(len(header))}
                inputs = [row[k] for k in (f"input{i}" for i in range(1, 10)) if k in row]
                if template and inputs:
                    try:
                        prompt = template.format(*inputs)
                    except (IndexError, KeyError):
                        prompt = f"Input: {' | '.join(inputs)}"
                else:
                    prompt = f"Input: {' | '.join(inputs)}"
                yield idx, {"prompt": prompt, "answer": row.get("label", "")}
