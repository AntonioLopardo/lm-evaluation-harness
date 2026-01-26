import re
import string
import unicodedata


def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""

    def remove_articles(text):
        # No articles to remove in Amharic, but keep for consistency
        return text

    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        # Add Amharic punctuation marks
        exclude.update(["።", "፣", "፤", "፥", "፦", "፧", "፨"])
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def compute_exact(a_gold, a_pred):
    return int(normalize_answer(a_gold) == normalize_answer(a_pred))


def compute_f1(a_gold, a_pred):
    gold_toks = normalize_answer(a_gold).split()
    pred_toks = normalize_answer(a_pred).split()

    if len(gold_toks) == 0 or len(pred_toks) == 0:
        # If either is empty, check exact match
        return int(gold_toks == pred_toks)

    common = set(gold_toks) & set(pred_toks)
    num_same = sum(min(gold_toks.count(w), pred_toks.count(w)) for w in common)

    if num_same == 0:
        return 0

    precision = 1.0 * num_same / len(pred_toks)
    recall = 1.0 * num_same / len(gold_toks)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1


def process_results_amharic_qa(doc, results):
    """Process results for Amharic QA task.

    The israel/AmharicQA dataset has 'answers' as a string (not a list).
    """
    pred = results[0].strip()
    # The dataset has answers as a single string
    gold = doc["answers"]

    exact_match = compute_exact(gold, pred)
    f1 = compute_f1(gold, pred)

    return {"exact_match": exact_match, "f1": f1}
