# New Task Implementations

This document tracks new evaluation tasks being added to the lm-evaluation-harness.

---

## Task Backlog

| Task | Language | Status | Paper | Dataset | Priority |
|------|----------|--------|-------|---------|----------|
| VMLU | Vietnamese | ✅ Complete | - | [vilm/vmlu_val](https://huggingface.co/datasets/vilm/vmlu_val) | High |
| ViQuAD | Vietnamese | ✅ Complete | COLING 2020 | [taidng/UIT-ViQuAD2.0](https://huggingface.co/datasets/taidng/UIT-ViQuAD2.0) | High |
| Amharic QA | Amharic | ✅ Complete | [arXiv:2502.02047](https://arxiv.org/abs/2502.02047) | [israel/AmharicQA](https://huggingface.co/datasets/israel/AmharicQA) | High |
| IndicMMLU-Pro | Urdu + 8 Indic | ✅ Complete | - | [LinguaLift/IndicMMLU-Pro](https://huggingface.co/datasets/LinguaLift/IndicMMLU-Pro) | High |
| Thai Winograd | Thai | ✅ Complete | Winograd 1972 | [pakphum/winograd_th](https://huggingface.co/datasets/pakphum/winograd_th) | Medium |
| FLORES NLL | EN/TH/VI/AM/UR | ✅ Complete | [Goldfish](https://arxiv.org/abs/2408.10441) | [Muennighoff/flores200](https://huggingface.co/datasets/Muennighoff/flores200) | Low |

### Status Legend
- 🔍 Research - Investigating dataset availability and implementation approach
- 📝 Design - Designing task configuration
- 🚧 In Progress - Implementation underway
- ✅ Complete - Implemented and tested
- ❌ Blocked - Cannot proceed (see notes)

---

## Task Details

### 1. Vietnamese Language Understanding Tasks

#### 1a. VMLU (Vietnamese Multitask Language Understanding) ✅

**Status:** Implemented  
**Task Name:** `vmlu`  
**Dataset:** [vilm/vmlu_val](https://huggingface.co/datasets/vilm/vmlu_val)

**Description:**  
Vietnamese version of MMLU - multiple choice question answering across various subjects.

**Implementation:**
- Location: `lm_eval/tasks/vmlu/`
- Output type: `multiple_choice`
- Metrics: Accuracy, Normalized Accuracy
- Prompt language: Vietnamese

---

#### 1b. ViQuAD (Vietnamese Question Answering Dataset) ✅

**Status:** Implemented  
**Task Name:** `viquad`  
**Dataset:** [taidng/UIT-ViQuAD2.0](https://huggingface.co/datasets/taidng/UIT-ViQuAD2.0)

**Description:**  
Vietnamese SQuAD 2.0 style extractive QA with both answerable and unanswerable questions.

**Implementation:**
- Location: `lm_eval/tasks/viquad/`
- Output type: `generate_until`
- Metrics: Exact Match, F1
- Prompt language: Vietnamese
- Note: Test split has hidden labels, using validation for evaluation

---

### 2. Amharic QA ✅

**Status:** Implemented  
**Task Name:** `amharic_qa`  
**Paper:** [arXiv:2502.02047](https://arxiv.org/abs/2502.02047)  
**Dataset:** [israel/AmharicQA](https://huggingface.co/datasets/israel/AmharicQA)

**Description:**  
SQuAD-style extractive question answering dataset for Amharic, an Ethiopian Semitic language with ~57 million speakers.

**Implementation:**
- Location: `lm_eval/tasks/amharic_qa/`
- Output type: `generate_until`
- Metrics: Exact Match, F1
- Prompt language: Amharic (Ge'ez script)

**Splits:**
| Split      | Examples |
|------------|----------|
| Train      | 1,723    |
| Validation | 595      |
| Test       | 299      |

---

### 3. IndicMMLU-Pro ✅

**Status:** Implemented  
**Task Group:** `indicmmlu_pro`  
**Dataset:** [LinguaLift/IndicMMLU-Pro](https://huggingface.co/datasets/LinguaLift/IndicMMLU-Pro)

**Description:**  
MMLU-Pro style benchmark for 9 Indic languages with 10-option multiple choice questions and chain-of-thought reasoning.

**Languages:**
| Task Name | Language | Script |
|-----------|----------|--------|
| `indicmmlu_pro_urdu` | Urdu | Arabic |
| `indicmmlu_pro_hindi` | Hindi | Devanagari |
| `indicmmlu_pro_bengali` | Bengali | Bengali |
| `indicmmlu_pro_gujarati` | Gujarati | Gujarati |
| `indicmmlu_pro_kannada` | Kannada | Kannada |
| `indicmmlu_pro_marathi` | Marathi | Devanagari |
| `indicmmlu_pro_punjabi` | Punjabi | Gurmukhi |
| `indicmmlu_pro_tamil` | Tamil | Tamil |
| `indicmmlu_pro_telugu` | Telugu | Telugu |

**Implementation:**
- Location: `lm_eval/tasks/indicmmlu_pro/`
- Output type: `generate_until`
- Metrics: Exact Match
- 14 subject categories, 10 answer options (A-J)
- 5-shot chain-of-thought prompting

---

### 4. Thai Winograd Schema ✅

**Status:** Implemented  
**Task Name:** `winograd_th`  
**Dataset:** [pakphum/winograd_th](https://huggingface.co/datasets/pakphum/winograd_th)

**Description:**  
Thai version of the Winograd Schema Challenge - coreference resolution task testing commonsense reasoning. Given a sentence with a pronoun, the model must determine which of two entities the pronoun refers to.

**Implementation:**
- Location: `lm_eval/tasks/winograd_th/`
- Output type: `multiple_choice`
- Metrics: Accuracy
- 285 test examples
- Uses "multiple input" mode where the pronoun is replaced with each candidate

---

### 5. FLORES NLL (Negative Log Likelihood) ✅

**Status:** Implemented  
**Task Group:** `flores_nll`  
**Paper:** [Goldfish: Monolingual Language Models for Hundreds of Languages](https://arxiv.org/abs/2408.10441)  
**Dataset:** [Muennighoff/flores200](https://huggingface.co/datasets/Muennighoff/flores200)  
**Reference:** [goldfish/flores_eval_othermodels.py](https://github.com/tylerachang/goldfish/blob/main/eval_code/flores_eval_othermodels.py)

**Description:**  
Computes mean negative log likelihood (perplexity) on FLORES-200 sentences for multilingual language modeling evaluation. Based on evaluation methodology from Goldfish paper Appendix A3.

**Languages:**
| Task Name | Language | Script |
|-----------|----------|--------|
| `flores_nll_eng` | English | Latin |
| `flores_nll_tha` | Thai | Thai |
| `flores_nll_vie` | Vietnamese | Latin |
| `flores_nll_amh` | Amharic | Ethiopic |
| `flores_nll_urd` | Urdu | Arabic |

**Implementation:**
- Location: `lm_eval/tasks/flores_nll/`
- Output type: `loglikelihood_rolling`
- Metrics: mean_nll, word_perplexity, byte_perplexity, bits_per_byte
- 1,012 sentences per language (devtest split)

---

## Implementation Checklist

For each new task:

1. **Research Phase**
   - [ ] Locate dataset (HuggingFace preferred)
   - [ ] Verify license and usage rights
   - [ ] Understand data format and splits
   - [ ] Identify evaluation metrics used in paper

2. **Design Phase**
   - [ ] Choose task type (generate_until, loglikelihood, etc.)
   - [ ] Design prompt template (in target language)
   - [ ] Plan metric implementation

3. **Implementation Phase**
   - [ ] Create task directory under `lm_eval/tasks/`
   - [ ] Create common YAML config
   - [ ] Create language/subtask-specific configs
   - [ ] Add any custom utils.py functions
   - [ ] Add README.md with task documentation

4. **Testing Phase**
   - [ ] Test with small sample
   - [ ] Verify metrics match paper baselines
   - [ ] Test with different model types

---

## Future Tasks (To Be Added)

_Add new tasks here as they are identified:_

| Task | Language | Source | Notes |
|------|----------|--------|-------|
| | | | |

---

## Notes

- Reference existing implementations in `lm_eval/tasks/` for patterns
- xquad, xnli, and mgsm are good examples for multilingual tasks
- Keep prompts in the target language for authenticity
- Document any data preprocessing needed

---

*Last updated: 2026-01-23*

---

## Quick Reference: Running Tasks

```bash
# Vietnamese MMLU
lm_eval --model hf --model_args pretrained=MODEL --tasks vmlu --batch_size 8

# Vietnamese QA
lm_eval --model hf --model_args pretrained=MODEL --tasks viquad --batch_size 8

# Amharic QA
lm_eval --model hf --model_args pretrained=MODEL --tasks amharic_qa --batch_size 8

# IndicMMLU-Pro (Urdu)
lm_eval --model hf --model_args pretrained=MODEL --tasks indicmmlu_pro_urdu --batch_size 4

# IndicMMLU-Pro (all 9 Indic languages)
lm_eval --model hf --model_args pretrained=MODEL --tasks indicmmlu_pro --batch_size 4

# FLORES NLL (perplexity evaluation)
lm_eval --model hf --model_args pretrained=MODEL --tasks flores_nll --batch_size 8

# FLORES NLL (individual language)
lm_eval --model hf --model_args pretrained=MODEL --tasks flores_nll_eng --batch_size 8

# Thai Winograd
lm_eval --model hf --model_args pretrained=MODEL --tasks winograd_th --batch_size 8

# Run all new tasks
lm_eval --model hf --model_args pretrained=MODEL --tasks vmlu,viquad,amharic_qa,indicmmlu_pro_urdu,winograd_th,flores_nll --batch_size 4
```
