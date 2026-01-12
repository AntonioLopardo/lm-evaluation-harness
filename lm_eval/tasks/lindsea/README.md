# LINDSEA (Linguistic Diagnostics for Southeast Asian Languages)

### Paper

LINDSEA: Linguistic Diagnostics for Southeast Asian Languages
- Paper: https://aclanthology.org/2024.lrec-main.213/
- Repository: https://github.com/juletx/lindsea

LINDSEA is a grammaticality judgment benchmark for Indonesian, testing syntactic knowledge through minimal pairs.

### Tasks

| Task | Phenomenon | Size |
|------|------------|------|
| `lindsea_argument_structure` | Argument Structure | 160 |
| `lindsea_npis_and_negation` | NPIs and Negation | 20 |
| `lindsea_filler_gap` | Filler-Gap Dependencies | 60 |
| `lindsea_morphology` | Morphology | 140 |

### Groups

| Group | Tasks |
|-------|-------|
| `lindsea` | All LINDSEA tasks (4 phenomena) |

### Usage

```bash
# Run all LINDSEA tasks
lm_eval --tasks lindsea --model hf --model_args pretrained=indolem/indobert-base-uncased

# Run specific phenomenon
lm_eval --tasks lindsea_argument_structure --model hf --model_args pretrained=indolem/indobert-base-uncased
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/juletxara/lindsea-blimp

### Notes

- Indonesian grammaticality using minimal pairs (good vs bad sentences)
- Based on BLiMP methodology
- Model should assign higher probability to grammatical sentence
