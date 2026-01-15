"""
Take in a YAML, and output all other splits with this YAML

Supports two evaluation modes:
1. Letter scoring (default): Scores probability of letters A, B, C, D
2. Full answer scoring (--mc_full): Scores probability of complete answer text

Usage examples:
    # Generate letter-scoring configs (default, existing behavior)
    python _generate_configs.py --base_yaml_path _default_template_yaml

    # Generate full-answer-scoring configs
    python _generate_configs.py --base_yaml_path _default_template_mc_full_yaml --task_prefix mc_full
"""

import argparse
import os

import requests
import yaml
from tqdm import tqdm

from lm_eval.utils import logging


API_URL = "https://datasets-server.huggingface.co/splits?dataset=facebook/belebele"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_yaml_path", required=True)
    parser.add_argument("--save_prefix_path", default="belebele")
    parser.add_argument("--cot_prompt_path", default=None)
    parser.add_argument("--task_prefix", default="")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # get filename of base_yaml so we can `"include": ` it in our other YAMLs.
    base_yaml_name = os.path.split(args.base_yaml_path)[-1]
    with open(args.base_yaml_path, encoding="utf-8") as f:
        base_yaml = yaml.full_load(f)

    if args.cot_prompt_path is not None:
        import json

        with open(args.cot_prompt_path, encoding="utf-8") as f:
            cot_file = json.load(f)

    def query():
        response = requests.get(API_URL)
        return response.json()["splits"]

    print(query())
    languages = [split["split"] for split in query()]

    for lang in tqdm([lang for lang in languages if "default" not in lang]):
        # Generate task name with optional prefix
        if args.task_prefix != "":
            task_name = f"belebele_{args.task_prefix}_{lang}"
            file_prefix = f"{args.save_prefix_path}_{args.task_prefix}"
        else:
            task_name = f"belebele_{lang}"
            file_prefix = args.save_prefix_path

        yaml_dict = {
            "include": base_yaml_name,
            "task": task_name,
            "test_split": lang,
            "fewshot_split": lang,
            "dataset_name": lang,
        }

        file_save_path = file_prefix + f"_{lang}.yaml"
        logging.info(f"Saving yaml for subset {lang} to {file_save_path}")
        with open(file_save_path, "w", encoding="utf-8") as yaml_file:
            yaml.dump(
                yaml_dict,
                yaml_file,
                width=float("inf"),
                allow_unicode=True,
                default_style='"',
            )

    # write group config out
    if args.task_prefix != "":
        group_name = f"belebele_{args.task_prefix}"
        group_file_name = f"_belebele_{args.task_prefix}.yaml"
    else:
        group_name = "belebele"
        group_file_name = "_belebele.yaml"

    group_yaml_dict = {
        "group": group_name,
        "task": [
            (
                f"belebele_{args.task_prefix}_{lang}"
                if args.task_prefix != ""
                else f"belebele_{lang}"
            )
            for lang in languages
            if "default" not in lang
        ],
        "aggregate_metric_list": [
            {"metric": "acc", "aggregation": "mean", "weight_by_size": True},
            {"metric": "acc_norm", "aggregation": "mean", "weight_by_size": True},
        ],
        "metadata": {"version": 0.1},
    }

    file_save_path = group_file_name

    with open(file_save_path, "w", encoding="utf-8") as group_yaml_file:
        yaml.dump(
            group_yaml_dict,
            group_yaml_file,
            width=float("inf"),
            allow_unicode=True,
            default_style='"',
        )
