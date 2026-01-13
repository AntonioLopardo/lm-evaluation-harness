import datasets


def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    """Transform EWoK dataset into minimal pairs format.
    
    EWoK has Context1, Context2, Target1, Target2.
    Context1 is designed to make Target1 more likely.
    Context2 is designed to make Target2 more likely.
    
    We create two examples per original row:
    1. Context1 with choices [Target1, Target2], answer=0
    2. Context2 with choices [Target1, Target2], answer=1
    """
    processed = []
    
    for doc in dataset:
        # Example 1: Context1 -> Target1 is correct
        processed.append({
            "context": doc["Context1"],
            "target_correct": doc["Target1"],
            "target_incorrect": doc["Target2"],
            "domain": doc["Domain"],
            "label": 0,  # Target1 is at index 0
        })
        
        # Example 2: Context2 -> Target2 is correct
        processed.append({
            "context": doc["Context2"],
            "target_correct": doc["Target2"],
            "target_incorrect": doc["Target1"],
            "domain": doc["Domain"],
            "label": 0,  # target_correct is always at index 0
        })
    
    return datasets.Dataset.from_list(processed)
