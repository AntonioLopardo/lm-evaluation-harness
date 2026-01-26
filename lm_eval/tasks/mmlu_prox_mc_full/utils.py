"""Utility functions for MMLU-ProX MC Full tasks."""

from functools import partial


SUBJECTS = [
    "biology",
    "business",
    "chemistry",
    "computer_science",
    "economics",
    "engineering",
    "health",
    "history",
    "law",
    "math",
    "other",
    "philosophy",
    "physics",
    "psychology",
]


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


def process_docs(dataset, subject):
    return dataset.filter(lambda x: x["category"] == subject)


process_functions = {
    f"process_{subject}": partial(process_docs, subject=subject) for subject in SUBJECTS
}

globals().update(process_functions)
