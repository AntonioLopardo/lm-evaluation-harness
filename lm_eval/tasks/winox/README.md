# WinoX

### Paper

WinoX: Wino-X: Multilingual Winograd Schemas for Commonsense Reasoning and Coreference Resolution
- Paper: https://aclanthology.org/2021.emnlp-main.670/
- Repository: https://github.com/demelin/Wino-X

WinoX is a multilingual collection of Winograd Schemas for cross-lingual coreference resolution.

### Tasks

The benchmark provides two settings:
- **LM (Language Model)**: Test coreference in target language only
- **MT (Machine Translation)**: Cross-lingual evaluation

We implement the LM setting for the target languages.

| Task | Languages | Description |
|------|-----------|-------------|
| `winox_de` | German | Winograd schemas in German |
| `winox_fr` | French | Winograd schemas in French |
| `winox_ru` | Russian | Winograd schemas in Russian |

### Groups

| Group | Tasks |
|-------|-------|
| `winox` | All WinoX tasks (de, fr, ru) |

### Usage

```bash
# Run all WinoX tasks
lm_eval --tasks winox --model hf --model_args pretrained=xlm-roberta-base

# Run specific language
lm_eval --tasks winox_de --model hf --model_args pretrained=xlm-roberta-base
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/demelin/wino_x

### Citation

```bibtex
@inproceedings{emelin-sennrich-2021-wino,
    title = "Wino-{X}: Multilingual {W}inograd Schemas for Commonsense Reasoning and Coreference Resolution",
    author = "Emelin, Denis  and
      Sennrich, Rico",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing",
    year = "2021",
    publisher = "Association for Computational Linguistics",
    pages = "8517--8533",
}
```
