import re
import string

import transformers.data.metrics.squad_metrics as squad_metrics


def filter_answerable(doc, *args):
    """Filter to only include answerable questions (not impossible)."""
    return not doc.get("is_impossible", False)


def process_results_viquad(doc, results):
    """Process results for ViQuAD task.

    Uses the same metrics as SQuAD: Exact Match and F1.
    """
    pred = results[0].strip()

    # ViQuAD has answers in SQuAD format: {"text": [...], "answer_start": [...]}
    answers = doc["answers"]

    if not answers["text"]:
        # Unanswerable question
        # If model predicts empty, it's correct
        is_correct = len(pred) == 0 or pred.lower() in ["", "không có câu trả lời", "không thể trả lời"]
        return {"exact_match": int(is_correct), "f1": float(is_correct)}

    # For answerable questions, compute against all valid answers
    gold_answers = answers["text"]

    # Compute max score against all gold answers
    exact_match = max(squad_metrics.compute_exact(gold, pred) for gold in gold_answers)
    f1 = max(squad_metrics.compute_f1(gold, pred) for gold in gold_answers)

    return {"exact_match": exact_match, "f1": f1}
