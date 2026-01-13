# ANALOGICAL - Analogy Evaluation Benchmark

### Paper

Title: ANALOGICAL - A Novel Benchmark for Long Text Analogy Evaluation in Large Language Models
- Paper: https://arxiv.org/abs/2305.05050
- Authors: Wijesiriwardene et al. (University of South Carolina, Amazon AI, Stanford)

ANALOGICAL evaluates LLMs' ability to identify analogical relationships across six levels of complexity.

### Tasks

| Task | Config | Test Size | Description |
|------|--------|-----------|-------------|
| `analogical_bats` | bats | 1,799 | BATS 3.0 word analogies |
| `analogical_google` | google | 500 | Google word analogy dataset |
| `analogical_sat` | sat | varies | SAT-style analogies |
| `analogical_u2` | u2 | varies | U2 analogies |
| `analogical_u4` | u4 | varies | U4 analogies |
| `analogical_scan` | scan | varies | SCAN analogies |

### Usage

```bash
# Run all ANALOGICAL tasks
lm_eval --tasks analogical --model hf --model_args pretrained=bert-base-uncased

# Run specific task
lm_eval --tasks analogical_bats --model hf --model_args pretrained=bert-base-uncased
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/relbert/analogy_questions

### Task Format

Each example contains:
- `stem`: The base analogy pair (e.g., ["strong", "stronger"])
- `choice`: Four possible answer pairs
- `answer`: Index of the correct answer (0-3)

Example: "strong is to stronger as tall is to taller"

### Citation

```bibtex
@article{wijesiriwardene2023analogical,
    title={ANALOGICAL - A Novel Benchmark for Long Text Analogy Evaluation in Large Language Models},
    author={Wijesiriwardene, Thilini and others},
    journal={arXiv preprint arXiv:2305.05050},
    year={2023}
}
```
