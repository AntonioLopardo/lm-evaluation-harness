def format_choices(doc):
    """Format the choice list into readable options."""
    choices = []
    for pair in doc["choice"]:
        choices.append(f"{pair[0]} is to {pair[1]}")
    return choices


def format_stem(doc):
    """Format the stem into a question."""
    return f"{doc['stem'][0]} is to {doc['stem'][1]} as"
