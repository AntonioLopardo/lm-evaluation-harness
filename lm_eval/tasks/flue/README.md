# FLUE (French Language Understanding Evaluation)

### Paper

FLUE: French Language Understanding Evaluation
- Paper: https://aclanthology.org/2020.lrec-1.667/
- Repository: https://github.com/getalp/Flaubert

FLUE is a benchmark for evaluating French language understanding models.

### Tasks

| Task | Description | Size |
|------|-------------|------|
| `flue_xnli` | French NLI (3-way classification) | 5,010 test |
| `flue_cls` | Text Classification | varies |
| `flue_pawsx` | Paraphrase Detection | varies |

### Groups

| Group | Tasks |
|-------|-------|
| `flue` | All FLUE tasks |

### Usage

```bash
# Run all FLUE tasks
lm_eval --tasks flue --model hf --model_args pretrained=flaubert/flaubert_base_cased

# Run just XNLI
lm_eval --tasks flue_xnli --model hf --model_args pretrained=flaubert/flaubert_base_cased
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/GETALP/flue

⚠️ **Note**: Requires `trust_remote_code=True` (handled automatically by task config).

### Citation

```bibtex
@inproceedings{le-etal-2020-flaubert,
    title = "{F}lau{BERT}: Unsupervised Language Model Pre-training for {F}rench",
    author = "Le, Hang  and
      Vial, Lo{\"\i}c  and
      Frej, Jibril  and
      Segonne, Vincent  and
      Coavoux, Maximin  and
      Lecouteux, Benjamin  and
      Allauzen, Alexandre  and
      Crabb{\'e}, Beno{\^\i}t  and
      Besacier, Laurent  and
      Schwab, Didier",
    booktitle = "Proceedings of the Twelfth Language Resources and Evaluation Conference",
    year = "2020",
    publisher = "European Language Resources Association",
    pages = "2479--2490",
}
```
