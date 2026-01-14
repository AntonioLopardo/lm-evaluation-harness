"""EXECUTE dataset builder for lm-evaluation-harness.

Loads EXECUTE benchmark data from local TSV files and builds prompts.
Paper: https://aclanthology.org/2025.findings-acl.95/
"""

import pickle
from pathlib import Path
from typing import Dict, List, Optional

import datasets


EXECUTE_DATA_PATH = Path("/home/execute_benchmark/data/tasks")

LANGUAGES = {
    "amh": "Amharic",
    "ara": "Arabic", 
    "deu": "German",
    "eng": "English",
    "hin": "Hindi",
    "jpn": "Japanese",
    "kor": "Korean",
    "rus": "Russian",
    "spa": "Spanish",
    "zho": "Chinese",
}

TASKS = [
    'spell', 'spell_inverse', 'contains_char', 'contains_word',
    'ins_char', 'ins_word', 'del_char', 'del_word',
    'sub_char', 'sub_word', 'swap_char', 'swap_word',
]


def load_execute_data(lang: str, task: str) -> datasets.Dataset:
    """Load EXECUTE dataset for a specific language and task.
    
    Args:
        lang: ISO-3 language code (e.g., 'eng', 'ara', 'zho')
        task: Task name (e.g., 'spell', 'contains_char')
    
    Returns:
        HuggingFace Dataset with 'prompt' and 'answer' columns
    """
    lang_path = EXECUTE_DATA_PATH / lang
    if not lang_path.exists():
        raise FileNotFoundError(f"Language not found: {lang}")
    
    tsv_path = lang_path / f"{task}.tsv"
    if not tsv_path.exists():
        raise FileNotFoundError(f"Task not found: {task} for language {lang}")
    
    # Load prompt template
    prompts_path = lang_path / "prompts.pkl"
    if prompts_path.exists():
        with open(prompts_path, 'rb') as f:
            prompt_templates = pickle.load(f)
        template = prompt_templates.get(task, "")
    else:
        template = ""
    
    # Load TSV data
    with open(tsv_path, 'r', encoding='utf-8') as f:
        header = f.readline().strip().split('\t')
        rows = []
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= len(header):
                row = {header[i]: parts[i] for i in range(len(header))}
                rows.append(row)
    
    # Build samples with prompts
    samples = []
    for row in rows:
        # Get inputs (input1, input2, etc.)
        inputs = []
        for i in range(1, 10):
            key = f"input{i}"
            if key in row:
                inputs.append(row[key])
        
        # Build prompt
        if template and inputs:
            try:
                prompt = template.format(*inputs)
            except (IndexError, KeyError):
                prompt = f"Input: {' | '.join(inputs)}"
        else:
            prompt = f"Input: {' | '.join(inputs)}"
        
        samples.append({
            "prompt": prompt,
            "answer": row.get("label", ""),
        })
    
    return datasets.Dataset.from_list(samples)


def get_execute_dataset(lang: str, task: str):
    """Factory function for loading EXECUTE datasets."""
    return load_execute_data(lang, task)
