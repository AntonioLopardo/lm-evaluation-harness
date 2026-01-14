# NLI-TR (Turkish Natural Language Inference)

### Paper

Title: NLI-TR: A Turkish Natural Language Inference Dataset
- Paper: https://aclanthology.org/2020.emnlp-main.662/
- Repository: https://github.com/boun-tabi/NLI-TR

NLI-TR provides Turkish translations of SNLI and MultiNLI datasets for natural language inference.

### Tasks

| Task | Config | Eval Split | Size |
|------|--------|------------|------|
| `nli_tr_snli` | snli_tr | test | 10,000 |
| `nli_tr_multinli` | multinli_tr | validation_matched | 10,000 |

**Note**: MultiNLI-TR uses `validation_matched` as the eval split since the dataset doesn't have a `test` split.

### Results

| Task | Model | Few-shot | Accuracy |
|------|-------|----------|----------|
| `nli_tr_snli` | Qwen2-1.5B-Instruct | 5-shot | 43% |
| `nli_tr_multinli` | TURKCELL/Turkcell-LLM-7b-v1 | 5-shot | **58.5%** |

The random baseline for 3-way NLI is 33%.

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
