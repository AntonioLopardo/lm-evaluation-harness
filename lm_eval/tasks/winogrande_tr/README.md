# Winogrande-TR (Turkish Winogrande)

### Overview

Turkish translation of the Winogrande benchmark for commonsense reasoning and coreference resolution.

### Task

| Task | Test Size | Validation Size |
|------|-----------|-----------------|
| `winogrande_tr` | 1,766 | 1,266 |

### Usage

```bash
lm_eval --tasks winogrande_tr --model hf --model_args pretrained=Qwen/Qwen2-7B-Instruct
```

### Dataset

- **Current**: https://huggingface.co/datasets/malhajar/winogrande-tr-v0.2 (GPT-4 translations)
- Used by: [OpenLLMTurkishLeaderboard](https://huggingface.co/datasets/malhajar/winogrande-tr-v0.2)

### Format

Each example contains:
- `sentence`: A sentence with a blank (`_`) to fill
- `option1`, `option2`: Two possible completions
- `answer`: Correct option (1 or 2)

### Results

| Model | Accuracy | Notes |
|-------|----------|-------|
| TURKCELL/Turkcell-LLM-7b-v1 | **56.1%** | Turkish-specific model, best result |
| Qwen2-7B-Instruct | 52.8% | Multilingual model |
| English Winogrande (Qwen2-7B) | 66% | For comparison |

### Notes

- Turkish-specific models (like Turkcell-LLM-7b-v1) perform best on this task
- The task shows ~10% lower accuracy compared to English Winogrande with the same models
- Uses the official OpenLLMTurkishLeaderboard v0.2 dataset with GPT-4 translations

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
