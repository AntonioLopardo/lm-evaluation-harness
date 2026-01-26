# VMLU - Vietnamese Multitask Language Understanding

## Description

VMLU (Vietnamese Multitask Language Understanding) is a Vietnamese benchmark inspired by MMLU, designed to evaluate language models on various subjects and domains in Vietnamese.

## Dataset

- **Source:** [vilm/vmlu_val](https://huggingface.co/datasets/vilm/vmlu_val)
- **Language:** Vietnamese (vi)
- **Task Type:** Multiple Choice Question Answering

## Task Format

The task is multiple choice question answering where the model must select the correct answer from 4 options.

**Prompt Template (Vietnamese):**
```
Câu hỏi: {question}
A. {choice_a}
B. {choice_b}
C. {choice_c}
D. {choice_d}
Đáp án:
```

**Translation:**
```
Question: {question}
A. {choice_a}
B. {choice_b}
C. {choice_c}
D. {choice_d}
Answer:
```

## Metrics

- **Accuracy (acc):** Percentage of correctly answered questions
- **Normalized Accuracy (acc_norm):** Length-normalized accuracy

## Splits

| Split      | Examples |
|------------|----------|
| Validation | 744      |

## Subjects

The dataset covers various subjects including:
- Economics and Business
- Science and Technology
- History and Geography
- Law and Regulations
- And more...

## Usage

```bash
lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-2-7b \
    --tasks vmlu \
    --batch_size 8
```

## Related Benchmarks

- MMLU (English)
- CMMLU (Chinese)
- KMMLU (Korean)

## Citation

```bibtex
@misc{vmlu,
  title={VMLU: Vietnamese Multitask Language Understanding Benchmark},
  author={Vietnamese LM Community},
  year={2024}
}
```
