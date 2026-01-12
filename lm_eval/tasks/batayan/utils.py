"""Utility functions for BATAYAN tasks."""


def process_nli_doc(doc):
    """Process NLI document."""
    prompts = doc["prompts"][0]
    return {
        "sentence1": prompts["sentence1"],
        "sentence2": prompts["sentence2"],
        "label": doc["label"],
        "text_label": doc["text_label"],
    }


def doc_to_text_nli(doc):
    """Format NLI prompt in Filipino."""
    prompts = doc["prompts"][0]
    return f"{prompts['sentence1']}\nTanong: Ang pangalawang pangungusap ay totoo, hindi totoo, o walang kinalaman?\n{prompts['sentence2']}\nSagot:"


def doc_to_target_nli(doc):
    """Map label to index. A=entailment, B=contradiction, C=neutral."""
    label_map = {"A": 0, "B": 1, "C": 2}
    return label_map.get(doc["label"], 0)


def doc_to_choice_nli(doc):
    """Return Filipino labels."""
    return ["Totoo", "Hindi totoo", "Walang kinalaman"]


def doc_to_text_causal(doc):
    """Format causal reasoning prompt."""
    prompts = doc["prompts"][0]
    premise = prompts.get("premise", prompts.get("context", ""))
    question = prompts.get("question", "")
    choice1 = prompts.get("choice1", prompts.get("hypothesis1", ""))
    choice2 = prompts.get("choice2", prompts.get("hypothesis2", ""))
    return f"{premise}\n{question}\nA. {choice1}\nB. {choice2}\nSagot:"


def doc_to_target_causal(doc):
    """Map label to index."""
    label_map = {"A": 0, "B": 1}
    return label_map.get(doc["label"], 0)


def doc_to_choice_causal(doc):
    """Return choices from prompts."""
    prompts = doc["prompts"][0]
    choice1 = prompts.get("choice1", prompts.get("hypothesis1", "A"))
    choice2 = prompts.get("choice2", prompts.get("hypothesis2", "B"))
    return [choice1, choice2]


def doc_to_text_sentiment(doc):
    """Format sentiment prompt."""
    prompts = doc["prompts"][0]
    text = prompts.get("text", prompts.get("sentence", ""))
    return f"Teksto: {text}\nAng damdamin ng teksto ay positibo o negatibo?\nSagot:"


def doc_to_target_sentiment(doc):
    """Map label to index."""
    label_map = {"A": 0, "B": 1}  # A=positive, B=negative
    return label_map.get(doc["label"], 0)


def doc_to_choice_sentiment(doc):
    """Return Filipino sentiment labels."""
    return ["Positibo", "Negatibo"]
