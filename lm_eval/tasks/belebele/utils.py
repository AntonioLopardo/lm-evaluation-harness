"""Utility functions for Belebele tasks."""


def doc_to_choice(doc):
    """Return the list of answer choices for a document.
    
    This function is needed because constructing the list in Jinja
    can break when answer text contains special characters like quotes.
    """
    return [
        doc["mc_answer1"],
        doc["mc_answer2"],
        doc["mc_answer3"],
        doc["mc_answer4"],
    ]
