"""Utility functions for WinoX tasks."""


def doc_to_text_de(doc):
    """Return the text after the blank in German context."""
    context = doc["context_de"]
    idx = context.index("_") + 1
    return context[idx:].strip()


def doc_to_text_fr(doc):
    """Return the text after the blank in French context."""
    context = doc["context_fr"]
    idx = context.index("_") + 1
    return context[idx:].strip()


def doc_to_text_ru(doc):
    """Return the text after the blank in Russian context."""
    context = doc["context_ru"]
    idx = context.index("_") + 1
    return context[idx:].strip()


def doc_to_target(doc):
    """Return target index (0 or 1)."""
    # answer is 1-indexed, convert to 0-indexed
    return doc["answer"] - 1


def doc_to_choice_de(doc):
    """Return choices with context prefix for German."""
    context = doc["context_de"]
    idx = context.index("_")
    prefix = context[:idx]
    return [prefix + doc["option1_de"], prefix + doc["option2_de"]]


def doc_to_choice_fr(doc):
    """Return choices with context prefix for French."""
    context = doc["context_fr"]
    idx = context.index("_")
    prefix = context[:idx]
    return [prefix + doc["option1_fr"], prefix + doc["option2_fr"]]


def doc_to_choice_ru(doc):
    """Return choices with context prefix for Russian."""
    context = doc["context_ru"]
    idx = context.index("_")
    prefix = context[:idx]
    return [prefix + doc["option1_ru"], prefix + doc["option2_ru"]]
