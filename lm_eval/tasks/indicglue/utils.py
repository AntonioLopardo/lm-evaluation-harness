"""Utility functions for IndicGLUE tasks."""

from functools import partial


# COPA utilities

def convert_choice(choice):
    """Lowercase the first character of a choice."""
    return choice[0].lower() + choice[1:]


def copa_doc_to_text(doc, connector):
    """Format COPA premise with appropriate connector."""
    # Drop the period if present
    premise = doc["premise"].strip()
    if premise.endswith("।"):  # Hindi/Devanagari period
        premise = premise[:-1]
    elif premise.endswith("."):
        premise = premise[:-1]
    conn = connector[doc["question"]]
    return premise + f" {conn}"


def copa_doc_to_choice(doc):
    """Return choices for COPA."""
    return [convert_choice(doc["choice1"]), convert_choice(doc["choice2"])]


# COPA connectors for different languages
copa_doc_to_text_hi = partial(
    copa_doc_to_text,
    connector={
        "cause": "क्योंकि",  # because
        "effect": "इसलिए",  # therefore
    },
)

copa_doc_to_text_gu = partial(
    copa_doc_to_text,
    connector={
        "cause": "કારણ કે",  # because
        "effect": "તેથી",  # therefore
    },
)

copa_doc_to_text_mr = partial(
    copa_doc_to_text,
    connector={
        "cause": "कारण",  # because
        "effect": "म्हणून",  # therefore
    },
)


# WNLI utilities

def wnli_doc_to_text_hi(doc):
    """Format WNLI document for Hindi."""
    return f"आधार वाक्य: {doc['premise']}\nप्रश्न: क्या यह सही है? {doc['hypothesis']}\nउत्तर:"


def wnli_doc_to_text_gu(doc):
    """Format WNLI document for Gujarati."""
    return f"આધાર વાક્ય: {doc['premise']}\nપ્રશ્ન: શું આ સાચું છે? {doc['hypothesis']}\nજવાબ:"


def wnli_doc_to_text_mr(doc):
    """Format WNLI document for Marathi."""
    return f"आधारभूत वाक्य: {doc['premise']}\nप्रश्न: हे बरोबर आहे का? {doc['hypothesis']}\nउत्तर:"


# Label mappings for WNLI
# IndicGLUE WNLI uses: 1 = entailment, 2 = not_entailment
def wnli_doc_to_target(doc):
    """Map WNLI labels to target index."""
    # Label 1 = entailment -> index 0 (हां/હા/होय)
    # Label 2 = not_entailment -> index 1 (नहीं/ના/नाही)
    return 0 if doc["label"] == 1 else 1


def wnli_doc_to_choice_hi(doc):
    """Return choices for Hindi WNLI."""
    return ["हां", "नहीं"]  # Yes, No


def wnli_doc_to_choice_gu(doc):
    """Return choices for Gujarati WNLI."""
    return ["હા", "ના"]  # Yes, No


def wnli_doc_to_choice_mr(doc):
    """Return choices for Marathi WNLI."""
    return ["होय", "नाही"]  # Yes, No
