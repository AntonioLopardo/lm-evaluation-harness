"""Utility functions for LMentry tasks."""

import re


def process_results_mc(doc, results):
    """Check if prediction matches the target answer for MC tasks.
    
    Normalizes by stripping whitespace, lowercasing, and removing punctuation.
    """
    pred = results[0].strip().lower()
    # Remove common punctuation that might be included
    pred = re.sub(r'[.,!?;:\'"]+', '', pred).strip()
    
    target = str(doc["answer"]).strip().lower()
    target = re.sub(r'[.,!?;:\'"]+', '', target).strip()
    
    # Exact match
    exact_match = 1.0 if pred == target else 0.0
    
    return {"exact_match": exact_match}


def process_results_sentence_containing(doc, results):
    """Check if generated sentence contains the required word."""
    pred = results[0].strip().lower()
    word = doc["word"].strip().lower()
    
    # Check if word appears in the sentence (as whole word)
    pattern = r'\b' + re.escape(word) + r'\b'
    contains = 1.0 if re.search(pattern, pred) else 0.0
    
    return {"exact_match": contains}


def process_results_sentence_not_containing(doc, results):
    """Check if generated sentence does NOT contain the forbidden word."""
    pred = results[0].strip().lower()
    word = doc["word"].strip().lower()
    
    # Check if word does NOT appear in the sentence
    pattern = r'\b' + re.escape(word) + r'\b'
    not_contains = 1.0 if not re.search(pattern, pred) else 0.0
    
    return {"exact_match": not_contains}


def process_results_word_containing(doc, results):
    """Check if generated word contains the required letter."""
    pred = results[0].strip().lower()
    # Get first word only
    words = pred.split()
    if not words:
        return {"exact_match": 0.0}
    first_word = words[0]
    # Clean punctuation
    first_word = re.sub(r'[^\w]', '', first_word)
    
    letter = doc["letter"].strip().lower()
    
    contains = 1.0 if letter in first_word else 0.0
    
    return {"exact_match": contains}


def process_results_word_not_containing(doc, results):
    """Check if generated word does NOT contain the forbidden letter."""
    pred = results[0].strip().lower()
    # Get first word only
    words = pred.split()
    if not words:
        return {"exact_match": 0.0}
    first_word = words[0]
    # Clean punctuation
    first_word = re.sub(r'[^\w]', '', first_word)
    
    letter = doc["letter"].strip().lower()
    
    not_contains = 1.0 if letter not in first_word else 0.0
    
    return {"exact_match": not_contains}


def process_results_starts_with_letter(doc, results):
    """Check if generated word starts with the required letter."""
    pred = results[0].strip().lower()
    words = pred.split()
    if not words:
        return {"exact_match": 0.0}
    first_word = re.sub(r'[^\w]', '', words[0])
    
    letter = doc["letter"].strip().lower()
    
    starts = 1.0 if first_word and first_word[0] == letter else 0.0
    
    return {"exact_match": starts}


def process_results_ends_with_letter(doc, results):
    """Check if generated word ends with the required letter."""
    pred = results[0].strip().lower()
    words = pred.split()
    if not words:
        return {"exact_match": 0.0}
    first_word = re.sub(r'[^\w]', '', words[0])
    
    letter = doc["letter"].strip().lower()
    
    ends = 1.0 if first_word and first_word[-1] == letter else 0.0
    
    return {"exact_match": ends}


def process_results_starts_with_word(doc, results):
    """Check if generated sentence starts with the required word."""
    pred = results[0].strip().lower()
    word = doc["word"].strip().lower()
    
    # Check if sentence starts with word
    pattern = r'^' + re.escape(word) + r'\b'
    starts = 1.0 if re.match(pattern, pred) else 0.0
    
    return {"exact_match": starts}


def process_results_ends_with_word(doc, results):
    """Check if generated sentence ends with the required word."""
    pred = results[0].strip().lower()
    # Remove trailing punctuation
    pred = re.sub(r'[.,!?;:]+$', '', pred).strip()
    word = doc["word"].strip().lower()
    
    # Check if sentence ends with word
    pattern = r'\b' + re.escape(word) + r'$'
    ends = 1.0 if re.search(pattern, pred) else 0.0
    
    return {"exact_match": ends}


def doc_to_target_any_words_category(doc):
    """Compute target for any_words_from_category task.
    
    Returns 'yes' if any words are in the category, 'no' otherwise.
    """
    category_words = doc.get("category_words", [])
    return "yes" if len(category_words) > 0 else "no"


def doc_to_target_all_words_category(doc):
    """Compute target for all_words_from_category task.
    
    Returns 'yes' if all words are in the category (no distractors), 'no' otherwise.
    """
    distractors = doc.get("distractors", [])
    return "yes" if len(distractors) == 0 else "no"


def process_results_yes_no(doc, results):
    """Check if prediction matches yes/no answer for category tasks."""
    pred = results[0].strip().lower()
    # Remove common punctuation
    pred = re.sub(r'[.,!?;:\'"]+', '', pred).strip()
    
    # Get the target from the doc_to_target function result
    # The target is computed dynamically, so we check which task this is
    category_words = doc.get("category_words", [])
    distractors = doc.get("distractors", [])
    
    # Determine expected answer based on task type
    # For any_words_category: yes if any category_words exist
    # For all_words_category: yes if no distractors
    # We can distinguish by checking num_words vs len(category_words)
    if "num_distractors" in doc:
        # This is likely all_words_category
        target = "yes" if len(distractors) == 0 else "no"
    else:
        target = "yes" if len(category_words) > 0 else "no"
    
    # Exact match
    exact_match = 1.0 if pred == target else 0.0
    
    return {"exact_match": exact_match}
