"""Utility functions for SyntaxGym tasks."""


def doc_to_choice(doc):
    """Extract plausible and implausible sentences from conditions."""
    conditions = doc["conditions"]
    names = conditions["condition_name"]
    contents = conditions["content"]

    # Find plaus and implaus indices
    plaus_idx = names.index("plaus")
    implaus_idx = names.index("implaus")

    return [contents[plaus_idx], contents[implaus_idx]]


def doc_to_target(doc):
    """Target is always 0 (plausible sentence)."""
    return 0
