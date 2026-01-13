# SynTran-FA (Farsi QA with Fluent Responses)

### Paper

Title: SynTran-fa: Generating Comprehensive Answers for Farsi QA Pairs via Syntactic Transformation
- Paper: https://doi.org/10.20944/preprints202410.1684.v1
- Repository: https://huggingface.co/datasets/SLPL/syntran-fa

SynTran-fa is a Farsi question-answering dataset that provides both short answers and fluent (complete sentence) answers.

### Task

| Task | Size | Description |
|------|------|-------------|
| `syntran_fa` | 48,106 | Farsi QA generation |

### Usage

```bash
lm_eval --tasks syntran_fa --model hf --model_args pretrained=HooshvareLab/bert-fa-zwnj-base --limit 100
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/SLPL/syntran-fa
- Source: Sharif University Speech and Language Processing Lab

### Format

Each example contains:
- `question`: The question in Farsi
- `short_answer`: Short answer (up to ~4 words)
- `fluent_answer`: Complete sentence answer
- `bert_loss`: Quality metric (lower = more fluent)

### Note

The dataset only has a `train` split. For proper evaluation, consider using `--limit` or splitting manually.

### Citation

```bibtex
@article{farsi2024syntran,
  title={SynTran-fa: Generating Comprehensive Answers for Farsi QA Pairs via Syntactic Transformation},
  author={Farsi, Farhan and Sabouri, Sadra and others},
  year={2024},
  doi={10.20944/preprints202410.1684.v1}
}
```
