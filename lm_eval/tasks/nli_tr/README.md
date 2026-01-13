# NLI-TR (Turkish Natural Language Inference)

### Paper

Title: NLI-TR: A Turkish Natural Language Inference Dataset
- Paper: https://aclanthology.org/2020.emnlp-main.662/
- Repository: https://github.com/boun-tabi/NLI-TR

NLI-TR provides Turkish translations of SNLI and MultiNLI datasets for natural language inference.

### Tasks

| Task | Config | Test Size |
|------|--------|-----------|
| `nli_tr_snli` | snli_tr | 10,000 |
| `nli_tr_multinli` | multinli_tr | 10,000 |

### Groups

| Group | Tasks |
|-------|-------|
| `nli_tr` | Both SNLI-TR and MultiNLI-TR |

### Usage

```bash
# Run all NLI-TR tasks
lm_eval --tasks nli_tr --model hf --model_args pretrained=dbmdz/bert-base-turkish-cased

# Run specific task
lm_eval --tasks nli_tr_snli --model hf --model_args pretrained=dbmdz/bert-base-turkish-cased
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/boun-tabi/nli_tr
- Requires `trust_remote_code=True`

### Labels

- 0: Entailment (Doğru)
- 1: Neutral (Belirsiz)
- 2: Contradiction (Yanlış)

### Citation

```bibtex
@inproceedings{budur-etal-2020-data,
    title = "Data and Representation for {T}urkish Natural Language Inference",
    author = "Budur, Emrah and others",
    booktitle = "Proceedings of EMNLP 2020",
    year = "2020",
}
```
