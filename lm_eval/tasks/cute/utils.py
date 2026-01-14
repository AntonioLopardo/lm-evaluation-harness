"""Utility functions for CUTE benchmark tasks."""


def process_results(doc, results):
    """Check if prediction matches the target answer.
    
    Normalizes by stripping whitespace and lowercasing for comparison.
    """
    pred = results[0].strip().lower()
    target = doc["answer"].strip().lower()
    
    # Exact match
    exact_match = 1.0 if pred == target else 0.0
    
    return {"exact_match": exact_match}
