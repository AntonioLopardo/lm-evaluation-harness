# Persian QA

### Overview

Persian Question Answering dataset based on Wikipedia articles. This is a reading comprehension task where the model must extract answers from the given context.

### Task

| Task | Validation Size | Train Size |
|------|-----------------|------------|
| `persian_qa` | 930 | 9,008 |

### Usage

```bash
lm_eval --tasks persian_qa --model hf --model_args pretrained=HooshvareLab/bert-fa-zwnj-base
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/SajjadAyoubi/persian_qa

### Format

Each example contains:
- `context`: Persian Wikipedia passage
- `question`: Question about the passage
- `answers`: Dictionary with `text` (list of answer strings) and `answer_start` (positions)

### Citation

```bibtex
@misc{persian_qa,
    title={Persian QA Dataset},
    author={Ayoubi, Sajjad},
    url={https://huggingface.co/datasets/SajjadAyoubi/persian_qa}
}
```
