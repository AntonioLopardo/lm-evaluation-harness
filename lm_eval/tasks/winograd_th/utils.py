"""Utility functions for Thai Winograd Schema task.

Dataset format:
- text: The full sentence containing the pronoun
- pronoun: The pronoun to resolve (e.g., "พวกเขา")
- options: List of two candidate referents
- label: Index (0 or 1) of the correct option
- pronoun_loc: Character position of the pronoun in the text

The task uses "multiple input" mode: we create two contexts by replacing
the pronoun with each option, and the model picks which makes more sense.
"""

from typing import Dict, List


def doc_to_text(doc: Dict) -> int:
    """
    Return index of the correct choice.

    In multiple-choice "multiple input" mode, this returns the label
    indicating which context (with substituted option) is correct.
    """
    return doc["label"]


def doc_to_target(doc: Dict) -> str:
    """
    Return the target completion (text after the pronoun).

    In "multiple input" mode, both choices share the same target.
    """
    text = doc["text"]
    pronoun = doc["pronoun"]
    pronoun_loc = doc["pronoun_loc"]

    # Return the text after the pronoun
    end_of_pronoun = pronoun_loc + len(pronoun)
    return text[end_of_pronoun:]


def doc_to_choice(doc: Dict) -> List[str]:
    """
    Return the two contexts with the pronoun replaced by each option.

    These serve as the different "inputs" in multiple-choice multiple input mode.
    """
    text = doc["text"]
    pronoun = doc["pronoun"]
    pronoun_loc = doc["pronoun_loc"]
    options = doc["options"]

    # Text before the pronoun
    prefix = text[:pronoun_loc]

    # Create two versions with each option substituted for the pronoun
    return [prefix + opt for opt in options]
