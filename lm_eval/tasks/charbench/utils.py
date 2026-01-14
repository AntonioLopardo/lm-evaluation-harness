"""Utility functions for CharBench tasks.

CharBench: Evaluating the Role of Tokenization in Character-Level Tasks
Paper: https://arxiv.org/abs/2508.02591
Authors: Omri Uzan, Yuval Pinter (Ben-Gurion University)
"""

import re


def filter_count_character_frequency(dataset):
    """Filter to count_character_frequency task."""
    return dataset.filter(lambda x: x["task"] == "count_character_frequency")


def filter_count_unique_chars(dataset):
    """Filter to count_unique_chars task."""
    return dataset.filter(lambda x: x["task"] == "count_unique_chars")


def filter_find_first_occurrence(dataset):
    """Filter to find_first_occurrence task."""
    return dataset.filter(lambda x: x["task"] == "find_first_occurrence")


def filter_find_last_occurrence(dataset):
    """Filter to find_last_occurrence task."""
    return dataset.filter(lambda x: x["task"] == "find_last_occurrence")


def process_results(doc, results):
    """Check if prediction matches the target answer.
    
    Extracts numeric answer and compares to expected value.
    """
    pred = results[0].strip()
    target = str(doc["answer"])
    
    # Extract first number from prediction
    numbers = re.findall(r'\d+', pred)
    if numbers:
        pred_num = numbers[0]
    else:
        pred_num = pred
    
    # Exact match on the number
    exact_match = 1.0 if pred_num == target else 0.0
    
    return {"exact_match": exact_match}
