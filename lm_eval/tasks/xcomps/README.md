# XCOMPS - Cross-lingual COMPositional Semantics

XCOMPS is a multilingual benchmark for evaluating semantic plausibility understanding in language models. It uses minimal pairs of acceptable and unacceptable sentences based on compositional semantics.

### Paper

Title: COMPS: Conceptual Minimal Pair Sentences for testing Property Knowledge and Inheritance in Pre-trained Language Models

### Citation

```bibtex
@inproceedings{misra-etal-2023-comps,
    title = "{COMPS}: Conceptual Minimal Pair Sentences for testing Property Knowledge and Inheritance in Pre-trained Language Models",
    author = "Misra, Kanishka and others",
    booktitle = "Proceedings of EACL 2023",
    year = "2023",
}
```

### Task Description

Each item consists of a minimal pair:
- **Acceptable sentence**: A semantically plausible statement (e.g., "Socks absorb sweat")
- **Unacceptable sentence**: A semantically implausible statement (e.g., "Stockings absorb sweat")

The model should assign higher probability to the acceptable sentence.

### Available Languages

| Task | Language | Code | Size |
|------|----------|------|------|
| `xcomps_fr` | French | fr | ~10k |
| `xcomps_nl` | Dutch | nl | ~10k |
| `xcomps_tr` | Turkish | tr | ~10k |
| `xcomps_zh` | Chinese | zh | ~10k |
| `xcomps_de` | German | de | ~14k |
| `xcomps_es` | Spanish | es | ~10k |
| `xcomps_vi` | Vietnamese | vi | ~10k |
| ... | (17 languages total) | | |

### Groups

- `xcomps`: All XCOMPS language tasks

### Dataset

- HuggingFace: https://huggingface.co/datasets/fpadovani/xcomps-dataset
