"""
EWoK (Elements of World Knowledge) utils.

EWoK evaluates commonsense reasoning about the physical and social world.
Each example contains paired contexts and targets that test minimal contrast pairs.

The dataset structure has:
- Context1 + Target1: valid combination
- Context2 + Target2: valid combination

We transform each row into two evaluation instances, one for each context.
"""

from datasets import Dataset


def process_docs(dataset):
    """Process EWoK dataset into individual evaluation instances.
    
    Each row becomes two instances:
    1. Context1 -> correct=Target1, incorrect=Target2
    2. Context2 -> correct=Target2, incorrect=Target1
    """
    processed = {
        "domain": [],
        "context": [],
        "target_correct": [],
        "target_incorrect": [],
        "concept_a": [],
        "concept_b": [],
        "context_type": [],
    }
    
    for doc in dataset:
        # Instance 1: Context1 should prefer Target1
        processed["domain"].append(doc["Domain"])
        processed["context"].append(doc["Context1"])
        processed["target_correct"].append(doc["Target1"])
        processed["target_incorrect"].append(doc["Target2"])
        processed["concept_a"].append(doc["ConceptA"])
        processed["concept_b"].append(doc["ConceptB"])
        processed["context_type"].append(doc["ContextType"])
        
        # Instance 2: Context2 should prefer Target2
        processed["domain"].append(doc["Domain"])
        processed["context"].append(doc["Context2"])
        processed["target_correct"].append(doc["Target2"])
        processed["target_incorrect"].append(doc["Target1"])
        processed["concept_a"].append(doc["ConceptA"])
        processed["concept_b"].append(doc["ConceptB"])
        processed["context_type"].append(doc["ContextType"])
    
    return Dataset.from_dict(processed)


def doc_to_text(doc):
    """Format the context as input."""
    return doc["context"] + " "


def doc_to_target(doc):
    """The correct target is always index 0."""
    return 0


def doc_to_choice(doc):
    """Return choices with correct target first."""
    return [doc["target_correct"], doc["target_incorrect"]]
