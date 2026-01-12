# BATAYAN (Filipino NLP Benchmark)

### Paper

BATAYAN: A Filipino NLP benchmark for evaluating Large Language Models
- Paper: https://aclanthology.org/2025.acl-long.1509/
- Authors: AI Singapore & Ateneo de Manila University

BATAYAN is a holistic Filipino benchmark that systematically evaluates LLMs across three key NLP competencies: understanding, reasoning, and generation. It covers both Tagalog and code-switched Taglish utterances.

### Tasks

| Task | Category | Size | Description |
|------|----------|------|-------------|
| `batayan_nli` | NLI | 600 | Natural Language Inference (3-way) |
| `batayan_causal` | Reasoning | 400 | Causal Reasoning |
| `batayan_sentiment` | Understanding | 600 | Sentiment Analysis |

### Groups

| Group | Tasks |
|-------|-------|
| `batayan` | All BATAYAN tasks |

### Usage

```bash
# Run all BATAYAN tasks
lm_eval --tasks batayan --model hf --model_args pretrained=aisingapore/Llama-SEA-LION-v3-8B-IT

# Run specific task
lm_eval --tasks batayan_nli --model hf --model_args pretrained=aisingapore/Llama-SEA-LION-v3-8B-IT
```

### Dataset

- NLI: https://huggingface.co/datasets/aisingapore/NLR-NLI
- Causal: https://huggingface.co/datasets/aisingapore/NLR-Causal-Reasoning
- Sentiment: https://huggingface.co/datasets/aisingapore/NLU-Sentiment-Analysis

### Notes

- Native-speaker validated dataset (not machine translated)
- Part of SEA benchmark suite from AI Singapore
- Filipino language code: `tl` (Tagalog)
