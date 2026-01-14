"""Utility functions for StringBench tasks.

StringLLM: Understanding the String Processing Capability of Large Language Models
Paper: https://arxiv.org/abs/2410.01208 (ICLR 2025)
"""


def process_results(doc, results):
    """Check if prediction matches the target answer.
    
    Normalizes by stripping whitespace for comparison.
    Handles boolean, numeric, and string comparisons.
    """
    pred = results[0].strip()
    target = str(doc["answer"]).strip()
    
    # Try to normalize booleans
    pred_lower = pred.lower()
    target_lower = target.lower()
    
    # Boolean normalization
    bool_map = {'true': 'True', 'false': 'False', 'yes': 'True', 'no': 'False'}
    if pred_lower in bool_map:
        pred = bool_map[pred_lower]
    if target_lower in bool_map:
        target = bool_map[target_lower]
    
    # Exact match
    exact_match = 1.0 if pred == target else 0.0
    
    return {"exact_match": exact_match}
