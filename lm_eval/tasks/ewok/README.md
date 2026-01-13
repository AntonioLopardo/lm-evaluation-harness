# EWoK (Elements of World Knowledge)

### Paper

Title: EWoK: A Benchmark for Elements of World Knowledge
- Paper: https://arxiv.org/abs/2405.09605
- Repository: https://github.com/ewok-core/ewok-core

EWoK tests language models on elements of world knowledge through minimal pairs. Each example provides two contexts and two targets, where Context1 makes Target1 more plausible and Context2 makes Target2 more plausible.

### Task

| Task | Size |
|------|------|
| `ewok` | 8,748 (4,374 × 2) |

### Usage

```bash
lm_eval --tasks ewok --model hf --model_args pretrained=gpt2
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/ewok-core/ewok-core-1.0

### Format

Original format:
- `Context1`, `Context2`: Two different contexts
- `Target1`, `Target2`: Two possible completions
- `Domain`: Knowledge domain (e.g., physics, social)

Processed format (2 examples per original):
1. Context1 → [Target1, Target2], correct=0
2. Context2 → [Target1, Target2], correct=1

### Citation

```bibtex
@article{ivanova2024ewok,
    title={Elements of World Knowledge (EWoK): A cognition-inspired framework for evaluating basic world knowledge in language models},
    author={Ivanova, Anna and others},
    journal={arXiv preprint arXiv:2405.09605},
    year={2024}
}
```
