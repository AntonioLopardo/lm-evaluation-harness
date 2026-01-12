"""Utility functions for ITALIC tasks."""


def doc_to_text(doc):
    """Format question with options."""
    prompt = doc["question"] + "\n"
    for i, opt in enumerate(doc["options"]):
        prompt += f"{chr(65+i)}. {opt}\n"
    prompt += "Risposta:"
    return prompt


def doc_to_choice(doc):
    """Return the options."""
    return doc["options"]


def doc_to_target(doc):
    """Return the correct answer index."""
    return doc["answer"]
