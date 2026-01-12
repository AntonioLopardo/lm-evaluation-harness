# Google Analogy Dataset

### Paper

Efficient Estimation of Word Representations in Vector Space (Word2Vec)
- Paper: https://arxiv.org/abs/1301.3781
- Original Dataset: https://code.google.com/archive/p/word2vec/

The Google Analogy dataset tests word relationship understanding through analogy tasks:
"A is to B as C is to ?" (e.g., "Athens is to Greece as Baghdad is to ?")

### Tasks

| Task | Description | Size |
|------|-------------|------|
| `analogy` | Full analogy dataset | 19,544 |

### Categories

- capital-common-countries
- capital-world
- currency
- city-in-state
- family
- gram1-adjective-to-adverb
- gram2-opposite
- gram3-comparative
- gram4-superlative
- gram5-present-participle
- gram6-nationality-adjective
- gram7-past-tense
- gram8-plural
- gram9-plural-verbs

### Usage

```bash
lm_eval --tasks analogy --model hf --model_args pretrained=gpt2
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/almogtavor/google-analogy-dataset

### Notes

- Tests both semantic and syntactic analogies
- 4-way analogy: Word1:Word2 :: Word3:Word4
- Model must predict Word4 given Word1, Word2, Word3
