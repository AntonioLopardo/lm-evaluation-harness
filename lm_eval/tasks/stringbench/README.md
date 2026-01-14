# StringBench: String Processing Capability Benchmark

### Paper

**Title**: StringLLM: Understanding the String Processing Capability of Large Language Models

**Authors**: Xilong Wang, Hao Fu, Jindong Wang, Neil Zhenqiang Gong (Duke University, Li Auto, William & Mary)

**Paper**: https://arxiv.org/abs/2410.01208 (ICLR 2025)

**GitHub**: https://github.com/wxl-lxw/StringLLM

### Description

StringBench is a comprehensive benchmark for evaluating LLMs' ability to perform string processing tasks. It includes 1,511 unique tasks spanning atomic operations (indexing, slicing, counting) and composite tasks (combinations of multiple operations).

The benchmark tests three types of strings:
- **Hash strings**: Hexadecimal outputs from hash functions (MD5, SHA, etc.)
- **Multilingual strings**: Natural language text in various languages
- **Random strings**: Randomly generated character sequences

### Tasks

| Task | Description | Samples |
|------|-------------|---------|
| `stringbench_hash` | String operations on hash outputs | 1,242 |
| `stringbench_multilingual` | Operations on multilingual text | 1,486 |
| `stringbench_random` | Operations on random strings | 1,437 |

### Task Types (Atomic Operations)

The benchmark covers 41+ string manipulation types including:
- **Indexing**: Access character at position (`a[x]`)
- **Slicing**: Extract substring (`a[x:y]`)
- **Length**: Count characters (`len(a)`)
- **Count**: Count occurrences (`a.count(x)`)
- **Contain**: Check substring presence (`x in a`)
- **Find**: Locate substring (`a.find(x)`)
- **Reverse**: Reverse string (`a[::-1]`)
- **Replace**: Substitute substrings
- **Case operations**: upper, lower, swapcase, etc.

Most test samples are **composite tasks** combining multiple operations.

### Key Findings from the Paper

1. **LLMs struggle with string processing**: Maximum ~48.89% accuracy with raw instructions
2. **Random strings are hardest**: Peak accuracy of 43.94%
3. **Program of Thought (PoT) helps**: >20% improvement over raw instructions
4. **Tokenization is a key factor**: LLMs lack character-level understanding
5. **Fine-tuning is effective**: 38.80%+ improvement with supervised fine-tuning

### Results

| Task | Qwen2-1.5B | Paper (GPT-4o) |
|------|------------|----------------|
| `stringbench_hash` | 1% | ~50% |
| `stringbench_multilingual` | 1% | ~48% |
| `stringbench_random` | 1% | ~44% |

**Note**: Low accuracy is expected! The paper shows even GPT-4o struggles. Small models like Qwen2-1.5B perform worse. The benchmark is intentionally challenging.

### Usage

```bash
# Run all StringBench tasks
lm_eval --model hf --model_args pretrained=Qwen/Qwen2-7B-Instruct \
    --tasks stringbench --batch_size 8

# Run specific string type
lm_eval --model hf --model_args pretrained=Qwen/Qwen2-7B-Instruct \
    --tasks stringbench_hash --batch_size 8
```

### Requirements

The StringBench data must be cloned locally:
```bash
git clone https://github.com/wxl-lxw/StringLLM.git /home/StringLLM
```

### Citation

```bibtex
@inproceedings{wang2025stringllm,
  title={StringLLM: Understanding the String Processing Capability of Large Language Models},
  author={Wang, Xilong and Fu, Hao and Wang, Jindong and Gong, Neil Zhenqiang},
  booktitle={International Conference on Learning Representations (ICLR)},
  year={2025}
}
```
