# XCOMPS - Cross-lingual Compositional Semantics

### Paper

Title: COMPS: Conceptual Minimal Pair Sentences for testing Property Knowledge in Pre-trained Language Models
- Paper: https://aclanthology.org/2023.eacl-main.213/
- Repository: https://github.com/kanishkamisra/comps

XCOMPS is the cross-lingual extension of COMPS, testing whether language models can distinguish between semantically acceptable and unacceptable sentences across 17 languages.

### Available Languages

| Task | Language | Code |
|------|----------|------|
| `xcomps_ar` | Arabic | ar |
| `xcomps_ca` | Catalan | ca |
| `xcomps_de` | German | de |
| `xcomps_el` | Greek | el |
| `xcomps_es` | Spanish | es |
| `xcomps_fa` | Farsi/Persian | fa |
| `xcomps_fr` | French | fr |
| `xcomps_he` | Hebrew | he |
| `xcomps_hu` | Hungarian | hu |
| `xcomps_ja` | Japanese | ja |
| `xcomps_ko` | Korean | ko |
| `xcomps_nl` | Dutch | nl |
| `xcomps_ru` | Russian | ru |
| `xcomps_tr` | Turkish | tr |
| `xcomps_uk` | Ukrainian | uk |
| `xcomps_vi` | Vietnamese | vi |
| `xcomps_zh` | Chinese | zh |

### Usage

```bash
# Run all XCOMPS tasks
lm_eval --tasks xcomps --model hf --model_args pretrained=xlm-roberta-base

# Run specific language
lm_eval --tasks xcomps_fa --model hf --model_args pretrained=HooshvareLab/bert-fa-zwnj-base
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/fpadovani/xcomps-dataset

### Task Format

Each example contains:
- `acceptable`: A semantically plausible sentence
- `unacceptable`: A semantically implausible sentence

The model should assign higher probability to the acceptable sentence.

### Citation

```bibtex
@inproceedings{misra-etal-2023-comps,
    title = "{COMPS}: Conceptual Minimal Pair Sentences for testing Property Knowledge and Inheritance in Pre-trained Language Models",
    author = "Misra, Kanishka and others",
    booktitle = "Proceedings of EACL 2023",
    year = "2023",
}
```
