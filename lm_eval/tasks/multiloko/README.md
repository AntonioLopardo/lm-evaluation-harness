# MultiLoKo: Multilingual Local Knowledge

## Overview

MultiLoKo is a multilingual local knowledge benchmark designed to evaluate LLMs across 31 languages. It tests knowledge that is locally relevant to specific language communities.

## Paper & Resources

- **Paper**: https://arxiv.org/abs/2504.10356
- **Dataset**: https://huggingface.co/datasets/facebook/multiloko
- **GitHub**: https://github.com/facebookresearch/multiloko

## Languages (31)

Arabic, Bengali, Cantonese, Czech, Dutch, English, Farsi, French, German, Hebrew, Hindi, Indonesian, Italian, Japanese, Khmer, Korean, Malay, Marathi, Polish, Portuguese, Romanian, Russian, Simplified Mandarin, Spanish, Swedish, Tagalog, Thai, Traditional Mandarin, Turkish, Urdu, Vietnamese

## Task Format

- **Type**: Extractive QA (generation)
- **Input**: Context passage + question
- **Output**: Short answer extracted from context
- **Metric**: Exact match (normalized)

## Splits

- `dev`: 7,750 examples (250 per language)
- `dev_translated_human`: Human translations
- `dev_translated_machine`: Machine translations  
- `enloko`: English local knowledge

## Usage

```bash
# Run MultiLoKo evaluation
lm_eval --model hf --model_args pretrained=MODEL_NAME --tasks multiloko --limit 100
```

## Example

**Context**: [Arabic text about the Prophet Muhammad...]

**Question**: في أي مدينة شهد رسول الله صلي الله عليه وسلم حادثة انشقاق القمر؟

**Answer**: مكة

## Citation

```bibtex
@article{multiloko2025,
  title={MultiLoKo: A Multilingual Local Knowledge Benchmark},
  author={Facebook Research},
  year={2025}
}
```
