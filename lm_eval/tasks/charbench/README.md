# CharBench: Evaluating Character-Level Understanding

### Paper

**Title**: CharBench: Evaluating the Role of Tokenization in Character-Level Tasks

**Authors**: Omri Uzan, Yuval Pinter (Ben-Gurion University of the Negev)

**Paper**: https://arxiv.org/abs/2508.02591

**Dataset**: https://huggingface.co/datasets/omriuz/CharBench

### Description

CharBench is a comprehensive benchmark for assessing LLMs' ability to perform character-level reasoning tasks. The benchmark includes 175,000 samples across 4 tasks testing counting and positional understanding.

### Tasks

| Task | Description | Paper Avg | Our Results |
|------|-------------|-----------|-------------|
| `charbench_count_char_freq` | Count occurrences of a character in a word | ~50% | 39% (Qwen2-1.5B) |
| `charbench_count_unique` | Count unique characters in a word | ~43% | 31% (Qwen2-1.5B) |
| `charbench_find_first` | Find index of first occurrence | ~43% | 20% (Qwen2-1.5B) |
| `charbench_find_last` | Find index of last occurrence | ~32% | 11% (Qwen2-1.5B) |

### Key Findings from the Paper

1. **Positional understanding is harder than counting**: Tasks requiring finding character positions have lower accuracy (32-43%) than counting tasks (~50%)

2. **Token length matters for position tasks**: Accuracy declines as the token containing the target character gets longer

3. **Word length affects all tasks**: Consistent linear decline in performance as word length increases

4. **Tokenization role varies by task**:
   - For counting tasks: actual character count matters more than tokenization
   - For position tasks: token length is the most correlated feature

### Example Prompts

**Counting (count_character_frequency)**:
```
How many times does the character 'r' appear in the string 'strawberry'?
Answer: 3
```

**Position (find_first_occurrence)**:
```
What is the index of the first occurrence of the character 'r' in the string 'strawberry'?
Start counting from 0.
Answer: 2
```

### Usage

```bash
# Run all CharBench tasks
lm_eval --model hf --model_args pretrained=Qwen/Qwen2-7B-Instruct \
    --tasks charbench --batch_size 8 --limit 1000

# Run only counting tasks
lm_eval --model hf --model_args pretrained=Qwen/Qwen2-7B-Instruct \
    --tasks charbench_count_char_freq,charbench_count_unique \
    --batch_size 8
```

### Citation

```bibtex
@article{uzan2025charbench,
  title={CharBench: Evaluating the Role of Tokenization in Character-Level Tasks},
  author={Uzan, Omri and Pinter, Yuval},
  journal={arXiv preprint arXiv:2508.02591},
  year={2025}
}
```
