# FarsTail (Persian/Farsi NLI)

### Paper

Title: FarsTail: A Persian Natural Language Inference Dataset
- Paper: https://arxiv.org/abs/2009.08820
- Repository: https://github.com/dml-qom/FarsTail

FarsTail is the first Persian (Farsi) natural language inference dataset.

### Task

| Task | Test Size | Validation Size |
|------|-----------|-----------------|
| `farstail` | 1,564 | 1,537 |

### Usage

```bash
lm_eval --tasks farstail --model hf --model_args pretrained=HooshvareLab/bert-fa-zwnj-base
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/ParsiAI/FarsTail

### Labels

- `e`: Entailment (درست)
- `n`: Neutral (نامشخص)
- `c`: Contradiction (نادرست)

### Citation

```bibtex
@article{amirkhani2020farstail,
    title={FarsTail: A Persian Natural Language Inference Dataset},
    author={Amirkhani, Hossein and others},
    journal={arXiv preprint arXiv:2009.08820},
    year={2020}
}
```
