# ViQuAD - Vietnamese Question Answering Dataset

## Description

UIT-ViQuAD 2.0 is a Vietnamese reading comprehension dataset in the style of SQuAD 2.0, containing both answerable and unanswerable questions.

## Dataset

- **Source:** [taidng/UIT-ViQuAD2.0](https://huggingface.co/datasets/taidng/UIT-ViQuAD2.0)
- **Language:** Vietnamese (vi)
- **Task Type:** Extractive Question Answering

## Task Format

The task is extractive question answering where the model must generate an answer span given a context paragraph and question in Vietnamese.

**Prompt Template (Vietnamese):**
```
Bối cảnh: {context}

Câu hỏi: {question}

Trả lời:
```

**Translation:**
```
Context: {context}

Question: {question}

Answer:
```

## Metrics

- **Exact Match (EM):** Percentage of predictions that exactly match the ground truth
- **F1 Score:** Token-level F1 score between prediction and ground truth

## Splits

| Split      | Examples |
|------------|----------|
| Train      | 28,454   |
| Validation | 3,814    |
| Test       | 7,301    |

## Features

- Contains both answerable and unanswerable questions (like SQuAD 2.0)
- `is_impossible` field indicates unanswerable questions
- By default, only answerable questions are evaluated

## Usage

```bash
lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-2-7b \
    --tasks viquad \
    --batch_size 8
```

## Citation

```bibtex
@inproceedings{nguyen2020vietnamese,
  title={A Vietnamese Dataset for Evaluating Machine Reading Comprehension},
  author={Nguyen, Kiet Van and Nguyen, Duc-Vu and Nguyen, Anh Gia-Tuan and Nguyen, Ngan Luu-Thuy},
  booktitle={Proceedings of COLING},
  year={2020}
}
```
