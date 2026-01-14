# CUTE: Character-level Understanding of Tokens Evaluation

### Paper

**Title**: CUTE: Measuring LLMs' Understanding of Their Tokens

**Authors**: Lukas Edman, Helmut Schmid, Alexander Fraser (LMU Munich, TU Munich)

**Paper**: https://arxiv.org/abs/2409.15452

**Repository**: https://github.com/Leukas/CUTE

### Description

CUTE is a benchmark designed to test the orthographic knowledge of Large Language Models (LLMs). Since most LLMs process text as multi-character tokens without direct access to individual characters, CUTE evaluates whether models can understand and manipulate the character composition of their tokens.

### Tasks

The benchmark consists of 14 tasks across 3 categories:

#### Composition Tasks
| Task | Description | Example |
|------|-------------|---------|
| `cute_spell` | Spell out a word with spaces | "the" → "t h e" |
| `cute_spell_inverse` | Write the word from spelled letters | "t h e" → "the" |
| `cute_contains_char` | Check if a character is in a word | Is "a" in "the"? → "No" |
| `cute_contains_word` | Check if a word is in a sentence | Is "the" in "A cat sat"? → "No" |

#### Similarity Tasks
| Task | Description |
|------|-------------|
| `cute_orth` | Select the word closer in Levenshtein distance |
| `cute_sem` | Select the word more semantically related |

#### Manipulation Tasks
| Task | Description | Example |
|------|-------------|---------|
| `cute_ins_char` | Insert a letter after every instance of another | Add "e" after "t" in "the" → "thme" |
| `cute_ins_word` | Insert a word after every instance of another |
| `cute_del_char` | Delete every instance of a letter | Delete "t" in "the" → "he" |
| `cute_del_word` | Delete every instance of a word |
| `cute_sub_char` | Substitute one letter with another |
| `cute_sub_word` | Substitute one word with another |
| `cute_swap_char` | Swap positions of two letters | Swap "t" and "e" in "the" → "eht" |
| `cute_swap_word` | Swap positions of two words |

### Usage

```bash
# Run all CUTE tasks
lm_eval --model hf --model_args pretrained=meta-llama/Llama-3.1-8B-Instruct --tasks cute --batch_size 8

# Run specific task categories
lm_eval --model hf --model_args pretrained=meta-llama/Llama-3.1-8B-Instruct --tasks cute_spell,cute_spell_inverse --batch_size 8

# Run with limit for quick testing
lm_eval --model hf --model_args pretrained=meta-llama/Llama-3.1-8B-Instruct --tasks cute --batch_size 8 --limit 100
```

### Results

Tested with Qwen2 Instruct models:

| Task | Qwen2-1.5B | Qwen2-7B | Random |
|------|------------|----------|--------|
| `cute_spell` | 78% | 97% | ~0% |
| `cute_spell_inverse` | 97% | 100% | ~0% |
| `cute_contains_char` | 67% | - | 50% |
| `cute_del_char` | 38% | 58% | ~0% |
| `cute_swap_char` | 1% | 2% | ~0% |

Based on the [paper](https://arxiv.org/abs/2409.15452):
- **Composition**: Models know the spelling of their tokens (~80-90% on spell/inverse tasks)
- **Similarity**: Better at semantic similarity than orthographic similarity
- **Manipulation**: LLMs struggle to manipulate text at character level (<50% on most tasks)
- **Scaling**: Larger models perform better, especially on composition tasks

Character-level tasks are generally harder than word-level equivalents.

### Citation

```bibtex
@article{edman2024cute,
  title={CUTE: Measuring LLMs' Understanding of Their Tokens},
  author={Edman, Lukas and Schmid, Helmut and Fraser, Alexander},
  journal={arXiv preprint arXiv:2409.15452},
  year={2024}
}
```
