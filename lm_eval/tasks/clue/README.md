# CLUE (Chinese Language Understanding Evaluation)

### Paper

CLUE: A Chinese Language Understanding Evaluation Benchmark
- Paper: https://aclanthology.org/2020.coling-main.419/
- Website: https://www.cluebenchmarks.com/

CLUE is a comprehensive Chinese NLU benchmark covering various tasks.

### Tasks

| Task | Description | Val Size |
|------|-------------|----------|
| `clue_cmnli` | Chinese MNLI (3-way NLI) | 12,241 |
| `clue_ocnli` | Original Chinese NLI | 2,950 |
| `clue_cluewsc` | Chinese WSC (coreference) | 304 |
| `clue_afqmc` | Ant Financial QA Matching | 4,316 |
| `clue_tnews` | Toutiao News Classification | 10,000 |

### Groups

| Group | Tasks |
|-------|-------|
| `clue` | All CLUE tasks |
| `clue_nli` | NLI tasks only (cmnli, ocnli) |

### Usage

```bash
# Run all CLUE tasks
lm_eval --tasks clue --model hf --model_args pretrained=THUDM/chatglm-6b

# Run just NLI tasks
lm_eval --tasks clue_nli --model hf --model_args pretrained=THUDM/chatglm-6b
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/clue/clue

### Notes

- Test labels are hidden; we use validation split for evaluation
- 0=neutral, 1=entailment, 2=contradiction for NLI tasks
