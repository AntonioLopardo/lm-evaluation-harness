# Winogrande-TR (Turkish Winogrande)

### Overview

Turkish translation of the Winogrande benchmark for commonsense reasoning and coreference resolution.

### Task

| Task | Test Size | Validation Size |
|------|-----------|-----------------|
| `winogrande_tr` | 1,766 | 1,266 |

### Usage

```bash
lm_eval --tasks winogrande_tr --model hf --model_args pretrained=dbmdz/bert-base-turkish-cased
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/malhajar/winogrande-tr

### Format

Each example contains:
- `sentence`: A sentence with a blank (`_`) to fill
- `option1`, `option2`: Two possible completions
- `answer`: Correct option (1 or 2)

### ⚠️ Known Data Quality Issue

**Warning**: This dataset has translation quality issues that affect evaluation results.

Approximately **42% of samples** have mismatches between option text and sentence text:
- Example: Sentence contains "Sarah" but `option1` contains "Sara"
- This breaks perplexity-based evaluation since the options don't match the sentence context

As a result, all models (including large multilingual models like Qwen2-7B and mGPT) score ~50% (random chance) on this task, compared to ~68% on the English Winogrande with the same models.

The task implementation is correct (matching the English Winogrande format), but the dataset needs correction.

### Citation

Based on the original Winogrande:
```bibtex
@article{sakaguchi2020winogrande,
    title={Winogrande: An adversarial winograd schema challenge at scale},
    author={Sakaguchi, Keisuke and others},
    journal={Communications of the ACM},
    year={2021}
}
```
