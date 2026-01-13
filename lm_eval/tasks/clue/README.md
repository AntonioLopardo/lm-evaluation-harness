# CLUE (Chinese Language Understanding Evaluation)

### Paper

Title: CLUE: A Chinese Language Understanding Evaluation Benchmark
- Paper: https://aclanthology.org/2020.coling-main.419/
- Repository: https://github.com/CLUEbenchmark/CLUE

CLUE is a comprehensive Chinese language understanding benchmark.

### Tasks

| Task | Description | Validation Size |
|------|-------------|-----------------|
| `clue_cmnli` | Chinese Multi-Genre NLI | 12,241 |
| `clue_ocnli` | Original Chinese NLI | 2,950 |
| `clue_cluewsc` | Chinese Winograd Schema Challenge | 304 |

### Usage

```bash
# Run all CLUE tasks
lm_eval --tasks clue --model hf --model_args pretrained=bert-base-chinese

# Run specific task
lm_eval --tasks clue_cmnli --model hf --model_args pretrained=bert-base-chinese
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/clue/clue
- Requires `trust_remote_code=True`

### Labels

**NLI (cmnli, ocnli):**
- 0: Entailment (正确)
- 1: Neutral (不确定)
- 2: Contradiction (错误)

**WSC (cluewsc):**
- 0: Not coreferent (否)
- 1: Coreferent (是)

### Citation

```bibtex
@inproceedings{xu-etal-2020-clue,
    title = "{CLUE}: A {C}hinese Language Understanding Evaluation Benchmark",
    author = "Xu, Liang and others",
    booktitle = "Proceedings of COLING 2020",
    year = "2020",
}
```
