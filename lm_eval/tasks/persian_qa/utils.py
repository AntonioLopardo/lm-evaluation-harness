"""Utility functions for Persian QA task."""


def filter_answerable(dataset):
    """Filter out unanswerable questions (those with empty answers.text lists).
    
    The Persian QA dataset is in SQuAD format where some questions are unanswerable
    and have empty answers.text lists. This function filters those out.
    """
    return dataset.filter(lambda doc: len(doc["answers"]["text"]) > 0)


def process_results(doc, results):
    """Check if prediction matches any of the target answers.
    
    Normalizes by stripping whitespace and lowercasing for comparison.
    Persian QA may have multiple valid answers in answers.text.
    """
    pred = results[0].strip().lower()
    targets = [t.strip().lower() for t in doc["answers"]["text"]]
    
    # Exact match against any target
    exact_match = 1.0 if pred in targets else 0.0
    
    return {"exact_match": exact_match}
