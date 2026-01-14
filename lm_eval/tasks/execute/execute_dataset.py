"""EXECUTE dataset loader for lm-evaluation-harness.

EXECUTE: Expandable X(cross)-lingual Extension of CUTE
Paper: https://aclanthology.org/2025.findings-acl.95/
GitHub: https://github.com/Leukas/EXECUTE
"""

import os
import pickle
from pathlib import Path
from typing import Dict, List, Any

import datasets


# Path to the EXECUTE benchmark data
EXECUTE_DATA_PATH = Path("/home/execute_benchmark/data/tasks")


class ExecuteDataset:
    """Loader for EXECUTE benchmark data."""
    
    LANGUAGES = ["amh", "ara", "deu", "eng", "hin", "jpn", "kor", "rus", "spa", "zho"]
    
    TASKS = [
        'spell', 'spell_inverse', 'contains_char', 'contains_word',
        'ins_char', 'ins_word', 'del_char', 'del_word',
        'sub_char', 'sub_word', 'swap_char', 'swap_word',
    ]
    
    # Prompt templates
    PROMPTS = {
        "spell": 'Spell out the word, putting spaces between each letter, based on the following examples:\n            \n            1. Spell out the word " {} ". Answer: " {} "\n            2. Spell out the word " {} ". Answer: " {} "\n            3. Spell out the word " {} ". Answer: " {} "\n            4. Spell out the word " {} ". Answer: " {} "\n            \n            Question: Spell out the word " {} ".',
        "spell_inverse": 'Write the word that is spelled out, without any spaces, based on the following examples:\n            \n            1. Write the word " {} ".  Answer: " {} "\n            2. Write the word " {} ". Answer: " {} "\n            3. Write the word " {} ". Answer: " {} "\n            4. Write the word " {} ". Answer: " {} "\n            \n            Question: Write the word " {} ".',
        "contains_char": 'Answer whether the specified letter is in the given word, based on the following examples:\n            \n            1. Is there a " {} " in " {} "? Answer: " {} "\n            2. Is there a " {} " in " {} "? Answer: " {} "\n            3. Is there a " {} " in " {} "? Answer: " {} "\n            4. Is there a " {} " in " {} "? Answer: " {} "\n            \n            Question: Is there a " {} " in " {} "?',
        "contains_word": 'Answer whether the specified word is in the given sentence (case insensitive), based on the following examples:\n            \n            1. Is there a " {} " in " {} "? Answer: " {} "\n            2. Is there a " {} " in " {} "? Answer: " {} "\n            3. Is there a " {} " in " {} "? Answer: " {} "\n            4. Is there a " {} " in " {} "? Answer: " {} "\n            \n            Question: Is there a " {} " in " {} "?',
        "ins_char": 'Add the specified letter after every instance of the second specified letter in a given word, based on the following examples:\n            \n            1. Add an " {} " after every " {} " in " {} ". Answer: " {} "\n            2. Add an " {} " after every " {} " in " {} ". Answer: " {} "\n            3. Add an " {} " after every " {} " in " {} ". Answer: " {} "\n            4. Add an " {} " after every " {} " in " {} ". Answer: " {} "\n            \n            Question: Add an " {} " after every " {} " in " {} ".',
        "ins_word": 'Add the specified word after every instance of the second specified word in a given sentence, based on the following examples:\n            \n            1. Add " {} " after every " {} " in " {} ". Answer: " {} "\n            2. Add " {} " after every " {} " in " {} ". Answer: " {} "\n            3. Add " {} " after every " {} " in " {} ". Answer: " {} "\n            4. Add " {} " after every " {} " in " {} ". Answer: " {} "\n            \n            Question: Add " {} " after every " {} " in " {} ".',
        "del_char": 'Delete every instance of a specified letter in a given word, based on the following examples:\n            \n            1. Delete every instance of " {} " in " {} ". Answer: " {} "\n            2. Delete every instance of " {} " in " {} ". Answer: " {} "\n            3. Delete every instance of " {} " in " {} ". Answer: " {} "\n            4. Delete every instance of " {} " in " {} ". Answer: " {} "\n            \n            Question: Delete every instance of " {} " in " {} ".',
        "del_word": 'Delete every instance of a specified word in a given sentence, based on the following examples:\n            \n            1. Delete every instance of " {} " in " {} ". Answer: " {} "\n            2. Delete every instance of " {} " in " {} ". Answer: " {} "\n            3. Delete every instance of " {} " in " {} ". Answer: " {} "\n            4. Delete every instance of " {} " in " {} ". Answer: " {} "\n            \n            Question: Delete every instance of " {} " in " {} ".',
        "swap_char": 'Swap the positions of two specified letters in a given word, based on the following examples:\n            \n            1. Swap " {} " and " {} " in " {} ". Answer: " {} "\n            2. Swap " {} " and " {} " in " {} ". Answer: " {} "\n            3. Swap " {} " and " {} " in " {} ". Answer: " {} "\n            4. Swap " {} " and " {} " in " {} ". Answer: " {} "\n            \n            Question: Swap " {} " and " {} " in " {} ".',
        "swap_word": 'Swap the positions of two specified words in a given sentence, based on the following examples:\n            \n            1. Swap " {} " and " {} " in " {} ". Answer: " {} "\n            2. Swap " {} " and " {} " in " {} ". Answer: " {} "\n            3. Swap " {} " and " {} " in " {} ". Answer: " {} "\n            4. Swap " {} " and " {} " in " {} ". Answer: " {} "\n            \n            Question: Swap " {} " and " {} " in " {} ".',
        "sub_char": 'Substitute the first specified letter with the second specified letter in a given word, based on the following examples:\n            \n            1. Substitute " {} " with " {} " in " {} ". Answer: " {} "\n            2. Substitute " {} " with " {} " in " {} ". Answer: " {} "\n            3. Substitute " {} " with " {} " in " {} ". Answer: " {} "\n            4. Substitute " {} " with " {} " in " {} ". Answer: " {} "\n            \n            Question: Substitute " {} " with " {} " in " {} ".',
        "sub_word": 'Substitute the first specified word with the second specified word in a given sentence, based on the following examples:\n            \n            1. Substitute " {} " with " {} " in " {} ". Answer: " {} "\n            2. Substitute " {} " with " {} " in " {} ". Answer: " {} "\n            3. Substitute " {} " with " {} " in " {} ". Answer: " {} "\n            4. Substitute " {} " with " {} " in " {} ". Answer: " {} "\n            \n            Question: Substitute " {} " with " {} " in " {} ".',
    }
    
    @classmethod
    def load(cls, lang: str, task: str) -> datasets.Dataset:
        """Load a task dataset for a specific language."""
        tsv_path = EXECUTE_DATA_PATH / lang / f"{task}.tsv"
        if not tsv_path.exists():
            raise FileNotFoundError(f"Task data not found: {tsv_path}")
        
        # Load few-shot prompts
        prompts_path = EXECUTE_DATA_PATH / lang / "prompts.pkl"
        fewshot_prompts = None
        if prompts_path.exists():
            with open(prompts_path, 'rb') as f:
                fewshot_prompts = pickle.load(f)
        
        # Load TSV data
        data = []
        with open(tsv_path, 'r', encoding='utf-8') as f:
            header = f.readline().strip().split('\t')
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= len(header):
                    row = {header[i]: parts[i] for i in range(len(header))}
                    data.append(row)
        
        # Build prompts for each sample
        samples = []
        for i, row in enumerate(data):
            # Get few-shot examples from the prompts pickle
            if fewshot_prompts and task in fewshot_prompts:
                prompt = fewshot_prompts[task][i] if i < len(fewshot_prompts[task]) else None
            else:
                prompt = None
            
            samples.append({
                "prompt": prompt if prompt else cls._build_simple_prompt(task, row, data),
                "label": row.get("label", ""),
                "lang": lang,
                "task": task,
            })
        
        return datasets.Dataset.from_list(samples)
    
    @classmethod
    def _build_simple_prompt(cls, task: str, row: Dict, all_data: List[Dict]) -> str:
        """Build a simple prompt when pre-built prompts are unavailable."""
        template = cls.PROMPTS.get(task, "")
        
        # Get inputs from row
        inputs = []
        for key in sorted(row.keys()):
            if key.startswith("input"):
                inputs.append(row[key])
        
        # Use first 4 samples as few-shot examples
        fewshot = []
        for ex in all_data[:4]:
            ex_inputs = []
            for key in sorted(ex.keys()):
                if key.startswith("input"):
                    ex_inputs.append(ex[key])
            ex_inputs.append(ex.get("label", ""))
            fewshot.extend(ex_inputs)
        
        # Add current input
        fewshot.extend(inputs)
        
        try:
            return template.format(*fewshot)
        except (IndexError, KeyError):
            # Fallback: just return the inputs as a simple prompt
            return f"Task: {task}\nInput: {' | '.join(inputs)}"


def load_execute_dataset(lang: str, task: str) -> datasets.Dataset:
    """Load EXECUTE dataset for a language and task."""
    return ExecuteDataset.load(lang, task)
