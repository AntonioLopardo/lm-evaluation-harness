# ITALIC (Italian Language and Culture Benchmark)

### Paper

ITALIC: A Benchmark for Italian Language and Culture Understanding
- Paper: https://aclanthology.org/2024.lrec-main.648/
- Repository: https://github.com/Crisp-Unimib/ITALIC

ITALIC is a comprehensive benchmark for evaluating Italian language and cultural knowledge in LLMs.

### Tasks

| Task | Description | Size |
|------|-------------|------|
| `italic` | Full benchmark (all categories) | 10,000 |

### Categories

- **Language Capability**: orthography, morphology, syntax, lexicon, synonyms/antonyms
- **Culture & Commonsense**: history, art_history, literature, tourism, civic_education

### Usage

```bash
lm_eval --tasks italic --model hf --model_args pretrained=iGeniusAI/Italia-9B-Instruct-v0.1
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/Crisp-Unimib/ITALIC

### Notes

- 4-way multiple choice questions
- Covers both linguistic and cultural knowledge
- Only train split available (used as test)
