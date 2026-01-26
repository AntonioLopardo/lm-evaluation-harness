# Amharic QA

## Description

Amharic Question Answering dataset - a SQuAD-style extractive QA benchmark for Amharic, an Ethiopian Semitic language with approximately 57 million speakers.

## Dataset

- **Source:** [israel/AmharicQA](https://huggingface.co/datasets/israel/AmharicQA)
- **Paper:** [arXiv:2502.02047](https://arxiv.org/abs/2502.02047)
- **Language:** Amharic (am)

## Task Format

The task is extractive question answering where the model must generate an answer span given a context paragraph and question.

**Prompt Template (Amharic):**
```
አውድ: {context}

ጥያቄ: {question}

መልስ:
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
| Train      | 1,723    |
| Validation | 595      |
| Test       | 299      |

## Usage

```bash
lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-2-7b \
    --tasks amharic_qa \
    --batch_size 8
```

## Citation

```bibtex
@article{amharic-squad-2025,
  title={Amharic Question Answering},
  author={...},
  journal={arXiv preprint arXiv:2502.02047},
  year={2025}
}
```
