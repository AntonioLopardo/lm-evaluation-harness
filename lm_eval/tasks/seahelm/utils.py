"""Utility functions for SEA-HELM tasks."""

import datasets


def process_nli_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    """Process NLI dataset to extract fields from prompts."""
    def _process(example):
        prompts = example["prompts"][0]
        return {
            "sentence1": prompts["sentence1"],
            "sentence2": prompts["sentence2"],
            "label": example["label"],
            "text_label": example["text_label"],
        }
    return dataset.map(_process, remove_columns=dataset.column_names)


def process_causal_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    """Process causal reasoning dataset to extract fields from prompts."""
    def _process(example):
        prompts = example["prompts"][0]
        return {
            "premise": prompts["premise"],
            "choice1": prompts["choice1"],
            "choice2": prompts["choice2"],
            "question": prompts.get("question_translated", ""),
            "label": example["label"],
        }
    return dataset.map(_process, remove_columns=dataset.column_names)


def process_sentiment_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    """Process sentiment analysis dataset to extract fields from prompts."""
    def _process(example):
        prompts = example["prompts"][0]
        return {
            "text": prompts["text"],
            "label": example["label"],
        }
    return dataset.map(_process, remove_columns=dataset.column_names)


def nli_doc_to_target(doc):
    """Map NLI label to index."""
    # Labels are A, B, C for entailment, contradiction, neutral
    label_map = {"A": 0, "B": 1, "C": 2}
    return label_map.get(doc["label"], 0)


def causal_doc_to_target(doc):
    """Map causal reasoning label to index."""
    # Labels are A or B
    label_map = {"A": 0, "B": 1}
    return label_map.get(doc["label"], 0)


def sentiment_doc_to_target(doc):
    """Map sentiment label to index."""
    label = doc["label"]
    
    # Indonesian: Positif, Negatif, Netral
    # Thai: แง่บวก (positive), แง่ลบ (negative), เฉยๆ (neutral)
    # Vietnamese: Tích cực (positive), Tiêu cực (negative), Trung lập (neutral)
    # Tagalog: Positibo, Negatibo, Neutral
    
    positive_labels = {"Positif", "แง่บวก", "Tích cực", "Positibo", "Positive"}
    negative_labels = {"Negatif", "แง่ลบ", "Tiêu cực", "Negatibo", "Negative"}
    neutral_labels = {"Netral", "เฉยๆ", "Trung lập", "Neutral"}
    
    if label in positive_labels:
        return 0
    elif label in negative_labels:
        return 1
    elif label in neutral_labels:
        return 2
    return 0


def get_sentiment_choices(lang):
    """Get sentiment choices for a specific language."""
    choices = {
        "id": ["Positif", "Negatif", "Netral"],
        "th": ["แง่บวก", "แง่ลบ", "เฉยๆ"],
        "vi": ["Tích cực", "Tiêu cực", "Trung lập"],
        "tl": ["Positibo", "Negatibo", "Neutral"],
    }
    return choices.get(lang, ["Positive", "Negative", "Neutral"])
