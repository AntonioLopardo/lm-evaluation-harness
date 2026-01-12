"""
CLiMP (Chinese Linguistic Minimal Pairs) utils.

Dataset: https://huggingface.co/datasets/suchirsalhan/CLiMP
Paper: Chinese BLiMP-style grammaticality judgments

Note: The ba_construction_1000.csv file has a broken header and is skipped.
"""

from datasets import Dataset
from huggingface_hub import hf_hub_download, list_repo_files
import pandas as pd


# Files to skip due to formatting issues
SKIP_FILES = {"ba_construction_1000.csv"}


def load_climp_dataset(**kwargs):
    """Load CLiMP data from individual CSV files, skipping broken ones.
    
    Returns a dict with 'train' split for compatibility with lm-eval.
    """
    files = list_repo_files("suchirsalhan/CLiMP", repo_type="dataset")
    csv_files = [f for f in files if f.endswith(".csv") and f not in SKIP_FILES]
    
    all_data = []
    for fname in csv_files:
        path = hf_hub_download("suchirsalhan/CLiMP", fname, repo_type="dataset")
        df = pd.read_csv(path)
        
        # Extract task name from filename
        task_name = fname.replace("_1000.csv", "")
        
        # Columns: Unnamed: 0, 0 (category), 1 (subcategory), 2 (sentence), 3 (label)
        for idx in range(0, len(df) - 1, 2):
            # Pairs: even index = good (label=1), odd index = bad (label=0)
            row_good = df.iloc[idx]
            row_bad = df.iloc[idx + 1]
            
            # Verify the pairing
            if row_good["3"] == 1 and row_bad["3"] == 0:
                all_data.append({
                    "sentence_good": row_good["2"],
                    "sentence_bad": row_bad["2"],
                    "category": row_good["0"],
                    "subcategory": row_good["1"],
                    "task": task_name,
                })
    
    return {"test": Dataset.from_list(all_data)}
