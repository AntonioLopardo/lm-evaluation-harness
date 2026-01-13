def doc_to_text(doc):
    """Return the answer index (0 or 1) for the correct option."""
    answer_to_num = {"1": 0, "2": 1}
    return answer_to_num[str(doc["answer"])]


def doc_to_target(doc):
    """Return the text after the blank marker."""
    idx = doc["sentence"].index("_") + 1
    return doc["sentence"][idx:].strip()


def doc_to_choice(doc):
    """Create full sentences by inserting each option at the blank position."""
    idx = doc["sentence"].index("_")
    options = [doc["option1"], doc["option2"]]
    return [doc["sentence"][:idx] + opt for opt in options]
