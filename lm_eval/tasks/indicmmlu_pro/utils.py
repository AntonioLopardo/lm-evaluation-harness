from functools import partial


choices = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


def format_cot_example(example, including_answer=True):
    """Format example for chain-of-thought prompting."""
    prompt = "Question:\n"
    question = example["question"]
    options = example["options"]
    prompt += question + "\n"
    prompt += "Options:\n"

    for i, opt in enumerate(options):
        if i >= len(choices):
            break
        prompt += "{}. {}\n".format(choices[i], opt)

    if including_answer:
        cot_content = example.get("cot_content", "")
        if cot_content:
            # Handle various CoT formats
            cot_content = cot_content.replace(
                "A: Let's think step by step.", "Answer: Let's think step by step."
            )
            prompt += cot_content + "\n\n"
        else:
            prompt += f"Answer: {example['answer']}\n\n"
    else:
        prompt += "Answer: Let's think step by step."

    return prompt


doc_to_text = partial(format_cot_example, including_answer=False)
fewshot_to_text = partial(format_cot_example, including_answer=True)
