"""
MultiLoKo: Multilingual Local Knowledge benchmark utils.

Dataset: https://huggingface.co/datasets/facebook/multiloko
Paper: https://arxiv.org/abs/2504.10356

MultiLoKo tests local knowledge across 31 languages with extractive QA.
"""

import re
import string
import unicodedata


def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)
    
    def white_space_fix(text):
        return ' '.join(text.split())
    
    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)
    
    def lower(text):
        return text.lower()
    
    return white_space_fix(remove_articles(remove_punc(lower(s))))


def exact_match(prediction, targets):
    """Check if prediction matches any target (normalized)."""
    pred_normalized = normalize_answer(prediction)
    for target in targets:
        if normalize_answer(target) == pred_normalized:
            return 1.0
    return 0.0


def process_results(doc, results):
    """Process results for exact match evaluation."""
    prediction = results[0].strip()
    targets = doc["targets"]
    
    return {
        "exact_match": exact_match(prediction, targets),
    }
