"""Utility functions for IndicMMLU-Pro tasks."""

choices = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


def doc_to_text(doc):
    """Format question with options."""
    prompt = doc["question"] + "\n"
    for i, opt in enumerate(doc["options"]):
        if i >= len(choices):
            break
        prompt += f"{choices[i]}. {opt}\n"
    prompt += "उत्तर:"  # "Answer:" in Hindi
    return prompt


def doc_to_choice(doc):
    """Return the list of options."""
    return doc["options"][:len(choices)]


def doc_to_target(doc):
    """Return the correct answer index."""
    return doc["answer_index"]
