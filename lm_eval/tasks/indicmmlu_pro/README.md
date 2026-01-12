# IndicMMLU-Pro

### Paper

IndicMMLU-Pro: A Multilingual MMLU-Pro Benchmark for Indic Languages
- Repository: https://huggingface.co/datasets/LinguaLift/IndicMMLU-Pro

IndicMMLU-Pro is a challenging, reasoning-focused benchmark based on MMLU-Pro, translated and adapted for Indic languages.

### Tasks

| Task | Language | Test Size |
|------|----------|-----------|
| `indicmmlu_pro_hi` | Hindi | 12,032 |
| `indicmmlu_pro_bn` | Bengali | 12,032 |
| `indicmmlu_pro_gu` | Gujarati | 12,032 |
| `indicmmlu_pro_kn` | Kannada | 12,032 |
| `indicmmlu_pro_mr` | Marathi | 12,032 |
| `indicmmlu_pro_pa` | Punjabi | 12,032 |
| `indicmmlu_pro_ta` | Tamil | 12,032 |
| `indicmmlu_pro_te` | Telugu | 12,032 |
| `indicmmlu_pro_ur` | Urdu | 12,032 |

### Groups

| Group | Tasks |
|-------|-------|
| `indicmmlu_pro` | All 9 Indic language tasks |

### Usage

```bash
# Run all IndicMMLU-Pro tasks
lm_eval --tasks indicmmlu_pro --model hf --model_args pretrained=ai4bharat/indic-bert

# Run just Hindi
lm_eval --tasks indicmmlu_pro_hi --model hf --model_args pretrained=ai4bharat/indic-bert
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/LinguaLift/IndicMMLU-Pro

### Notes

- 10-way multiple choice (A-J options)
- CoT prompting recommended for best results
- Based on MMLU-Pro structure
