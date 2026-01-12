# SyntaxGym

### Paper

SyntaxGym: An Online Platform for Targeted Evaluation of Language Models
- Paper: https://aclanthology.org/2020.acl-demos.10/
- Website: https://syntaxgym.org/

SyntaxGym provides targeted syntactic evaluations of language models using carefully controlled test suites.

### Tasks

We implement the 2-way grammaticality judgment tasks (plausible vs implausible):

| Task | Description | Size |
|------|-------------|------|
| `syntaxgym_all` | Combined suite (all-2020) | 799 |
| `syntaxgym_center_embed` | Center embedding | 28 |
| `syntaxgym_center_embed_mod` | Center embedding (modified) | 28 |

### Groups

| Group | Tasks |
|-------|-------|
| `syntaxgym` | All SyntaxGym tasks |

### Usage

```bash
# Run all SyntaxGym tasks
lm_eval --tasks syntaxgym --model hf --model_args pretrained=gpt2

# Run just the main suite
lm_eval --tasks syntaxgym_all --model hf --model_args pretrained=gpt2
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/cpllab/syntaxgym

### Notes

- The dataset contains multiple condition types, but we focus on the 2-way plausible/implausible judgments
- The `all-2020` config combines multiple phenomena
- Other configs with 4+ conditions (e.g., cleft, fgd_*) require more complex evaluation not yet implemented
