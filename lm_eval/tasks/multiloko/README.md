# MultiLoKo - Multilingual Local Knowledge

### Paper

Title: MultiLoKo: A Multilingual Local Knowledge Benchmark
- Paper: https://arxiv.org/abs/2504.10356
- Repository: https://github.com/facebookresearch/multiloko

MultiLoKo is a multilingual local knowledge benchmark designed to evaluate LLMs across 31 languages. It tests knowledge that is locally relevant to specific language communities.

### Available Languages (31)

| Task | Language | Examples |
|------|----------|----------|
| `multiloko_arabic` | Arabic | 250 |
| `multiloko_bengali` | Bengali | 250 |
| `multiloko_cantonese` | Cantonese | 250 |
| `multiloko_czech` | Czech | 250 |
| `multiloko_dutch` | Dutch | 250 |
| `multiloko_english` | English | 250 |
| `multiloko_farsi` | Farsi/Persian | 250 |
| `multiloko_french` | French | 250 |
| `multiloko_german` | German | 250 |
| `multiloko_hebrew` | Hebrew | 250 |
| `multiloko_hindi` | Hindi | 250 |
| `multiloko_indonesian` | Indonesian | 250 |
| `multiloko_italian` | Italian | 250 |
| `multiloko_japanese` | Japanese | 250 |
| `multiloko_khmer` | Khmer | 250 |
| `multiloko_korean` | Korean | 250 |
| `multiloko_malay` | Malay | 250 |
| `multiloko_marathi` | Marathi | 250 |
| `multiloko_polish` | Polish | 250 |
| `multiloko_portuguese` | Portuguese | 250 |
| `multiloko_romanian` | Romanian | 250 |
| `multiloko_russian` | Russian | 250 |
| `multiloko_simplified_mandarin` | Simplified Mandarin | 250 |
| `multiloko_spanish` | Spanish | 250 |
| `multiloko_swedish` | Swedish | 250 |
| `multiloko_tagalog` | Tagalog | 250 |
| `multiloko_thai` | Thai | 250 |
| `multiloko_traditional_mandarin` | Traditional Mandarin | 250 |
| `multiloko_turkish` | Turkish | 250 |
| `multiloko_urdu` | Urdu | 250 |
| `multiloko_vietnamese` | Vietnamese | 250 |

### Usage

```bash
# Run all MultiLoKo tasks
lm_eval --tasks multiloko --model hf --model_args pretrained=meta-llama/Llama-3.1-8B

# Run specific language
lm_eval --tasks multiloko_turkish --model hf --model_args pretrained=meta-llama/Llama-3.1-8B
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/facebook/multiloko

### Task Format

- **Type**: Extractive QA (generation)
- **Input**: Context passage + question
- **Output**: Short answer extracted from context
- **Metric**: Exact match (normalized, matches any valid target)

### Citation

```bibtex
@article{multiloko2025,
    title={MultiLoKo: A Multilingual Local Knowledge Benchmark},
    author={Facebook Research},
    year={2025},
    url={https://arxiv.org/abs/2504.10356}
}
```
