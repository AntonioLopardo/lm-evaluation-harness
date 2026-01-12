# ITA-Bench: Italian Benchmarks for LLMs

## Overview

ITA-Bench is a comprehensive evaluation suite for Italian language models, developed by Sapienza NLP. It includes Italian translations of popular English benchmarks.

## Paper & Resources

- **GitHub**: https://github.com/SapienzaNLP/ita-bench
- **HuggingFace Collection**: https://huggingface.co/collections/sapienzanlp/ita-bench-italian-benchmarks-for-llms

## Tasks

| Task | Dataset | Split | Size | Description |
|------|---------|-------|------|-------------|
| `ita_bench_arc_challenge` | sapienzanlp/arc_italian | test | 1,172 | Science QA (Challenge) |
| `ita_bench_arc_easy` | sapienzanlp/arc_italian | test | 2,376 | Science QA (Easy) |
| `ita_bench_hellaswag` | sapienzanlp/hellaswag_italian | validation | 9,998 | Commonsense Inference |
| `ita_bench_mmlu` | sapienzanlp/mmlu_italian | test | 13,127 | World Knowledge (57 subjects) |
| `ita_bench_piqa` | sapienzanlp/piqa_italian | validation | 1,713 | Physical Commonsense |
| `ita_bench_winogrande` | sapienzanlp/winogrande_italian | validation | 1,176 | Coreference Resolution |

## Usage

```bash
# Run all ITA-Bench tasks
lm_eval --model hf --model_args pretrained=MODEL_NAME --tasks ita_bench

# Run individual tasks
lm_eval --model hf --model_args pretrained=MODEL_NAME --tasks ita_bench_mmlu
```

## Dataset Format

All datasets follow a consistent structure:
- `input` / `input_translation`: English / Italian question
- `choices` / `choices_translation`: English / Italian options
- `label`: Correct answer index (0-indexed)

The tasks use the Italian translations (`input_translation`, `choices_translation`).

## Metrics

- **acc**: Accuracy
- **acc_norm**: Length-normalized accuracy (for some tasks)

## Citation

Please cite SapienzaNLP when using these benchmarks.
