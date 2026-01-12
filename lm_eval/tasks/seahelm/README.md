# SEA-HELM Tasks

SEA-HELM (Southeast Asian Holistic Evaluation of Language Models) is a comprehensive benchmark designed to assess LLM performance in Southeast Asian languages and cultural contexts.

### Paper

Title: SEA-HELM: Southeast Asian Holistic Evaluation of Language Models

Homepage: https://sea-lion.ai/

GitHub: https://github.com/aisingapore/SEA-HELM

### Citation

```bibtex
@article{seahelm2025,
    title = "{SEA-HELM}: Southeast Asian Holistic Evaluation of Language Models",
    author = "AI Singapore",
    year = "2025",
    url = "https://arxiv.org/abs/2502.14301",
}
```

### Available Tasks

#### NLI (Natural Language Inference)
| Task | Language | Test Size |
|------|----------|-----------|
| `seahelm_nli_id` | Indonesian | 1,000 |
| `seahelm_nli_th` | Thai | 1,000 |
| `seahelm_nli_vi` | Vietnamese | 1,000 |
| `seahelm_nli_tl` | Tagalog | 1,000 |
| `seahelm_nli_ta` | Tamil | 1,000 |

#### Sentiment Analysis
| Task | Language | Test Size |
|------|----------|-----------|
| `seahelm_sentiment_id` | Indonesian | 400 |
| `seahelm_sentiment_th` | Thai | 400 |
| `seahelm_sentiment_vi` | Vietnamese | 400 |
| `seahelm_sentiment_tl` | Tagalog | 400 |

#### Causal Reasoning (COPA-style)
| Task | Language | Test Size |
|------|----------|-----------|
| `seahelm_causal_id` | Indonesian | 500 |
| `seahelm_causal_th` | Thai | 500 |
| `seahelm_causal_vi` | Vietnamese | 500 |
| `seahelm_causal_tl` | Tagalog | 500 |

#### Question Answering
| Task | Language | Test Size |
|------|----------|-----------|
| `seahelm_qa_id` | Indonesian | 100 |
| `seahelm_qa_th` | Thai | 100 |
| `seahelm_qa_vi` | Vietnamese | 100 |

### Task Groups

- `seahelm`: All SEA-HELM tasks
- `seahelm_nli`: All NLI tasks
- `seahelm_sentiment`: All sentiment tasks
- `seahelm_causal`: All causal reasoning tasks

### Languages Covered

- Indonesian (id)
- Thai (th)
- Vietnamese (vi)
- Tagalog/Filipino (tl)
- Tamil (ta)
- Malay (ms)
- Burmese (my)
