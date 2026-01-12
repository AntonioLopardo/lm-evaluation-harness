# SEACrowd Tasks

SEACrowd is a collaborative initiative focused on advancing AI tools and resources for Southeast Asian languages and cultures.

### Paper

Title: SEACrowd: A Multilingual Multimodal Data Hub and Benchmark Suite for Southeast Asian Languages

Abstract: SEACrowd consolidates 498 datasheets covering diverse tasks across Southeast Asian languages, providing standardized dataloaders for 399 datasets.

Homepage: https://seacrowd.org/

### Citation

```bibtex
@inproceedings{lovenia2024seacrowd,
    title = "{SEACrowd}: A Multilingual Multimodal Data Hub and Benchmark Suite for Southeast Asian Languages",
    author = "Lovenia, Holy and others",
    booktitle = "Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing",
    year = "2024",
    url = "https://aclanthology.org/2024.emnlp-main.296",
}
```

### Requirements

**Important**: SEACrowd datasets require the `datasets` library version < 3.0.0 due to their use of loading scripts:

```bash
pip install 'datasets>=2.0.0,<3.0.0'
```

### Available Tasks

| Task | Dataset | Language | Description |
|------|---------|----------|-------------|
| `seacrowd_indonli` | SEACrowd/indonli | Indonesian | Natural Language Inference |
| `seacrowd_wrete` | SEACrowd/wrete | Indonesian | Word Relation Textual Entailment |
| `seacrowd_indolem_sentiment` | SEACrowd/indolem_sentiment | Indonesian | Sentiment Analysis |
| `seacrowd_facqa` | SEACrowd/facqa | Indonesian | Factoid Question Answering |

### Task Group

Run all SEACrowd tasks:
```bash
lm_eval --tasks seacrowd --model hf --model_args pretrained=<model>
```

### Languages

- Indonesian (id)
- More languages available in individual SEACrowd datasets
