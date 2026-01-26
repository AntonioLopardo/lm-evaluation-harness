# IndicMMLU-Pro

## Description

IndicMMLU-Pro is a multilingual extension of MMLU-Pro for 9 Indic languages. It evaluates language models on multiple-choice questions across 14 subject categories with 10 answer options per question.

## Dataset

- **Source:** [LinguaLift/IndicMMLU-Pro](https://huggingface.co/datasets/LinguaLift/IndicMMLU-Pro)
- **Task Type:** Multiple Choice with Chain-of-Thought

## Languages

| Task Name | Language | Script |
|-----------|----------|--------|
| `indicmmlu_pro_urdu` | Urdu | Arabic |
| `indicmmlu_pro_hindi` | Hindi | Devanagari |
| `indicmmlu_pro_bengali` | Bengali | Bengali |
| `indicmmlu_pro_gujarati` | Gujarati | Gujarati |
| `indicmmlu_pro_kannada` | Kannada | Kannada |
| `indicmmlu_pro_marathi` | Marathi | Devanagari |
| `indicmmlu_pro_punjabi` | Punjabi | Gurmukhi |
| `indicmmlu_pro_tamil` | Tamil | Tamil |
| `indicmmlu_pro_telugu` | Telugu | Telugu |

## Categories

The dataset covers 14 subject categories:
- Biology
- Business
- Chemistry
- Computer Science
- Economics
- Engineering
- Health
- History
- Law
- Math
- Other
- Philosophy
- Physics
- Psychology

## Metrics

- **Exact Match:** Accuracy of extracted answers (A-J)

## Features

- 10 answer options per question (A-J)
- Chain-of-thought reasoning included
- 5-shot prompting by default

## Usage

```bash
# Run Urdu only
lm_eval --model hf --model_args pretrained=MODEL --tasks indicmmlu_pro_urdu --batch_size 4

# Run all Indic languages
lm_eval --model hf --model_args pretrained=MODEL --tasks indicmmlu_pro --batch_size 4

# Run specific language
lm_eval --model hf --model_args pretrained=MODEL --tasks indicmmlu_pro_hindi --batch_size 4
```

## Citation

```bibtex
@misc{indicmmlupro,
  title={IndicMMLU-Pro: A Multilingual MMLU-Pro for Indic Languages},
  author={LinguaLift},
  year={2025},
  url={https://huggingface.co/datasets/LinguaLift/IndicMMLU-Pro}
}
```
