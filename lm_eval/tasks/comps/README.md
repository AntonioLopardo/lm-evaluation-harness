# COMPS (Compositional Semantics)

### Paper

COMPS: Conceptual Minimal Pair Sentences for testing Property Knowledge in Pre-trained Language Models
- Paper: https://aclanthology.org/2023.eacl-main.213/
- Repository: https://github.com/kanishkamisra/comps

COMPS tests whether language models can distinguish between concepts that do and don't have a property (e.g., "a sock absorbs sweat" vs "a stocking absorbs sweat").

### Tasks

| Task | Description | Size |
|------|-------------|------|
| `comps_base` | Base COMPS (real words) | 49,340 |
| `comps_wugs` | COMPS with novel words | varies |
| `comps_wugs_dist` | COMPS with distractor words | varies |

### Groups

| Group | Tasks |
|-------|-------|
| `comps` | All COMPS tasks |

### Usage

```bash
# Run all COMPS tasks
lm_eval --tasks comps --model hf --model_args pretrained=gpt2

# Run just base COMPS
lm_eval --tasks comps_base --model hf --model_args pretrained=gpt2
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/kanishka/comps

### Notes

- Each example has an acceptable sentence (property true of concept) and unacceptable sentence (property false of concept)
- Model should assign higher probability to the acceptable sentence
- Related to XCOMPS (cross-lingual version)
