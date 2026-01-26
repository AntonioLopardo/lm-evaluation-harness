"""Utility functions for VMLU task."""


def doc_to_text(doc):
    """Format document to text, handling variable number of choices."""
    question = doc["question"]
    choices = doc.get("choices", [])
    
    # Build choices text dynamically
    choice_labels = ["A", "B", "C", "D", "E", "F"]
    choices_text = "\n".join(
        f"{choice_labels[i]}. {choice}" 
        for i, choice in enumerate(choices) 
        if i < len(choice_labels)
    )
    
    return f"Câu hỏi: {question}\n{choices_text}\nĐáp án:"


def doc_to_choice(doc):
    """Return list of choice labels based on number of choices."""
    choices = doc.get("choices", [])
    choice_labels = ["A", "B", "C", "D", "E", "F"]
    return choice_labels[:len(choices)]
