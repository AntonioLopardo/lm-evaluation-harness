"""Utility functions for MMLU-ProX MC Full tasks."""

from functools import partial


# Map from task name suffix (with underscores) to actual category in dataset (with spaces)
SUBJECT_MAP = {
    "biology": "biology",
    "business": "business",
    "chemistry": "chemistry",
    "computer_science": "computer science",
    "economics": "economics",
    "engineering": "engineering",
    "health": "health",
    "history": "history",
    "law": "law",
    "math": "math",
    "other": "other",
    "philosophy": "philosophy",
    "physics": "physics",
    "psychology": "psychology",
}


def doc_to_choice(doc):
    """Return the list of non-null answer choices for a document.
    
    MMLU-ProX has variable number of options (option_0 through option_9).
    We filter out None values.
    """
    choices = []
    for i in range(10):
        opt = doc.get(f"option_{i}")
        if opt is not None:
            choices.append(opt)
    return choices


def process_docs(dataset, category):
    """Filter dataset by category name (with spaces)."""
    return dataset.filter(lambda x: x["category"] == category)


# Create process functions with proper category names
process_functions = {
    f"process_{task_suffix}": partial(process_docs, category=category_name) 
    for task_suffix, category_name in SUBJECT_MAP.items()
}

globals().update(process_functions)
