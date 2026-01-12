# DUMB (Dutch Model Benchmark)

### Paper

DUMB: A Benchmark for Smart Evaluation of Dutch Models
- Paper: https://openreview.net/pdf?id=ZSHcpMXWxX
- Leaderboard: https://dumbench.nl/

DUMB is a comprehensive evaluation suite for Dutch language models covering grammaticality, NLI, sentiment, and QA.

### Tasks

| Task | Description | Test Size |
|------|-------------|-----------|
| `dumb_cola` | Dutch CoLA (grammaticality) | 2,400 |
| `dumb_sick` | Dutch SICK (NLI) | 4,906 |
| `dumb_dbrd` | Dutch Book Review (sentiment) | 2,224 |

### Groups

| Group | Tasks |
|-------|-------|
| `dumb` | All DUMB tasks |

### Usage

```bash
# Run all DUMB tasks
lm_eval --tasks dumb --model hf --model_args pretrained=GroNLP/bert-base-dutch-cased

# Run specific task
lm_eval --tasks dumb_cola --model hf --model_args pretrained=GroNLP/bert-base-dutch-cased
```

### Datasets

- Dutch CoLA: https://huggingface.co/datasets/GroNLP/dutch-cola
- SICK-NL: https://huggingface.co/datasets/maximedb/sick_nl
- DBRD: https://huggingface.co/datasets/benjaminvdb/dbrd

### Notes

- Dutch-only benchmark
- Tasks cover grammaticality, NLI, and sentiment analysis
- Part of the comprehensive DUMB evaluation suite
