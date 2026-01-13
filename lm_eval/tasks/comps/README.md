# COMPS (Compositional Semantics)

### Paper

Title: COMPS: Conceptual Minimal Pair Sentences for testing Property Knowledge in Pre-trained Language Models
- Paper: https://aclanthology.org/2023.eacl-main.213/
- Repository: https://github.com/kanishkamisra/comps

COMPS tests whether language models can distinguish between concepts that do and don't have a property (e.g., "a sock absorbs sweat" vs "a stocking absorbs sweat").

### Tasks

| Task | Config | Size |
|------|--------|------|
| `comps_base` | base | 49,340 |
| `comps_wugs` | wugs | ~10,000 |
| `comps_wugs_dist` | wugs_dist | ~10,000 |

### Usage

```bash
# Run all COMPS tasks
lm_eval --tasks comps --model hf --model_args pretrained=gpt2

# Run just base
lm_eval --tasks comps_base --model hf --model_args pretrained=gpt2
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/kanishka/comps

### Task Format

Each example contains:
- `prefix_acceptable`: Semantically acceptable phrase (e.g., "a sock")
- `prefix_unacceptable`: Semantically unacceptable phrase (e.g., "a stocking")
- `property_phrase`: Property to test (e.g., "absorbs sweat.")

The model should assign higher probability to the acceptable sentence.

### Citation

```bibtex
@inproceedings{misra-etal-2023-comps,
    title = "{COMPS}: Conceptual Minimal Pair Sentences for testing Property Knowledge and Inheritance in Pre-trained Language Models",
    author = "Misra, Kanishka and others",
    booktitle = "Proceedings of EACL 2023",
    year = "2023",
}
```
