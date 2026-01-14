# LMentry: Elementary Language Tasks

### Paper

**Title**: LMentry: A Language Model Benchmark of Elementary Language Tasks

**Authors**: Avia Efrat, Or Honovich, Omer Levy

**Affiliations**: Tel Aviv University, Meta AI

**Paper**: https://arxiv.org/abs/2211.02069

### Description

LMentry is a benchmark that avoids the "arms race" of increasingly complex tasks by focusing on a compact set of tasks that are **trivial to humans** but surprisingly challenging for LLMs.

The benchmark is designed to:
- Provide quick and interpretable insights into model capabilities
- Measure both accuracy and robustness to input perturbations
- Serve as a "unit test" for LLMs without requiring large benchmark suites

**Key Finding**: While humans achieve 100% on LMentry, even TextDavinci002 (175B) only scored 66.1%!

### Tasks

The benchmark includes 25 tasks across multiple categories:

#### Multiple-Choice Tasks (MC)
| Task | Description | Example |
|------|-------------|---------|
| `lmentry_bigger_number` | Compare two numbers | "Which is bigger, 147 or 246?" |
| `lmentry_smaller_number` | Compare two numbers | "Which is smaller, 278 or 802?" |
| `lmentry_more_letters` | Compare word lengths | "Which has more letters, 'city' or 'drink'?" |
| `lmentry_less_letters` | Compare word lengths | "Which has fewer letters, 'day' or 'computer'?" |
| `lmentry_first_alphabetically` | Alphabetical order | "Which comes first, 'book' or 'water'?" |
| `lmentry_rhyming_word` | Identify rhymes | "Which rhymes with 'try': 'food' or 'cry'?" |
| `lmentry_homophones` | Sound similarity | "Which sounds like 'ate': 'eight' or 'mouth'?" |
| `lmentry_most_associated` | Word association | "Which is most associated with 'animals'?" |
| `lmentry_least_associated` | Word association | "Which is least associated with 'fruit'?" |
| `lmentry_word_after` | Sentence analysis | "In 'The door was pushed open', what comes after 'was'?" |
| `lmentry_word_before` | Sentence analysis | "What comes before 'any' in the sentence?" |
| `lmentry_first_word` | Extract first word | "What is the first word of the sentence?" |
| `lmentry_last_word` | Extract last word | "What is the last word of the sentence?" |
| `lmentry_first_letter` | Extract first letter | "What is the first letter of 'hello'?" |
| `lmentry_last_letter` | Extract last letter | "What is the last letter of 'world'?" |
| `lmentry_any_words_category` | Category check (any) | "Are any of these words vehicles?" |
| `lmentry_all_words_category` | Category check (all) | "Are all of these words furniture?" |

#### Generative Tasks (Gen)
| Task | Description | Evaluation |
|------|-------------|------------|
| `lmentry_sentence_containing` | Write sentence with word | Check if word appears |
| `lmentry_sentence_not_containing` | Write sentence without word | Check word absent |
| `lmentry_word_containing` | Write word with letter | Check if letter appears |
| `lmentry_word_not_containing` | Write word without letter | Check letter absent |
| `lmentry_starts_with_letter` | Write word starting with letter | Check first letter |
| `lmentry_ends_with_letter` | Write word ending with letter | Check last letter |
| `lmentry_starts_with_word` | Write sentence starting with word | Check first word |
| `lmentry_ends_with_word` | Write sentence ending with word | Check last word |

### Results

| Task | Qwen2-1.5B-Instruct | Paper (TextDavinci002) | Notes |
|------|---------------------|------------------------|-------|
| `lmentry_bigger_number` | **96%** | 93% | Numbers are easy |
| `lmentry_smaller_number` | **82%** | — | Slightly harder |
| `lmentry_more_letters` | **62%** | 55% | Character counting is hard |
| `lmentry_first_alphabetically` | **49%** | 87% | Alphabetical order |
| `lmentry_rhyming_word` | 6% | 77% | Very hard for small models |
| `lmentry_homophones` | 7% | 66% | Sound similarity |
| `lmentry_sentence_containing` | **83%** | 97% | Generative task |
| `lmentry_starts_with_letter` | **96%** | 98% | Easy generative |

### Key Findings

1. **Instruction tuning helps accuracy** but not robustness
2. **Scaling helps** but doesn't solve fundamental issues
3. **Character-level tasks remain hard**: counting letters, rhyming, homophones
4. **Generative tasks easier** than discriminative for some categories

### Usage

```bash
# Run all MC tasks
lm_eval --model hf --model_args pretrained=Qwen/Qwen2-7B-Instruct \
    --tasks lmentry_bigger_number,lmentry_more_letters,lmentry_first_alphabetically \
    --batch_size 16

# Run generative tasks
lm_eval --model hf --model_args pretrained=Qwen/Qwen2-7B-Instruct \
    --tasks lmentry_sentence_containing,lmentry_starts_with_letter \
    --batch_size 16
```

### Dataset

HuggingFace: https://huggingface.co/datasets/clembench-playpen/lmentry

Each task has 3000 test samples with multiple prompt templates.

### Citation

```bibtex
@inproceedings{efrat2022lmentry,
  title={LMentry: A Language Model Benchmark of Elementary Language Tasks},
  author={Efrat, Avia and Honovich, Or and Levy, Omer},
  booktitle={Findings of EMNLP},
  year={2022}
}
```
