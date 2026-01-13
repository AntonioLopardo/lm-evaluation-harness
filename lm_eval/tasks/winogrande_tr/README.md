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
