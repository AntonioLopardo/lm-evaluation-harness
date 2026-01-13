# SOAR Testing Scenarios (v2)

Testing scenarios for benchmarks added in `soar-benchmarks-v2` branch. Each scenario includes recommended models and expected baseline performance from source papers.

---

## Quick Reference

| Benchmark | Language(s) | Task Type | Primary Model | Expected Acc. |
|-----------|-------------|-----------|---------------|---------------|
| NLI-TR | Turkish | NLI | BERTurk | ~82-84% |
| Winogrande-TR | Turkish | Coreference | BERTurk | ~65-70% |
| FarsTail | Farsi | NLI | ParsBERT | ~83% |
| Persian QA | Farsi | Extractive QA | ParsBERT | ~75% F1 |
| SynTran-FA | Farsi | Generative QA | ParsBERT | TBD |
| XCOMPS | 17 languages | Property Knowledge | XLM-R | ~70-80% |
| MultiLoKo | 31 languages | Local Knowledge QA | Llama-3.1-8B | ~40-60% EM |
| CLUE | Chinese | NLI + Coreference | BERT-Chinese | ~80% |
| COMPS | English | Property Knowledge | GPT-2 | ~60-70% |
| EWoK | English | World Knowledge | GPT-4 / Llama-3 | ~75-85% |
| ANALOGICAL | English | Analogy Reasoning | GPT-4 | ~70-80% |

---

## 1. NLI-TR (Turkish NLI)

**Paper**: [Data and Representation for Turkish Natural Language Inference](https://aclanthology.org/2020.emnlp-main.662/) (EMNLP 2020)

### Tasks
| Task | Config | Test Size |
|------|--------|-----------|
| `nli_tr_snli` | snli_tr | 10,000 |
| `nli_tr_multinli` | multinli_tr | 10,000 |

### Baseline Results (from paper)
| Model | SNLI-TR Acc | MultiNLI-TR Acc |
|-------|-------------|-----------------|
| BERTurk (cased) | 83.2% | 76.8% |
| mBERT | 79.5% | 72.4% |
| XLM-R-base | 81.1% | 74.3% |

### Recommended Testing

```bash
# Test with BERTurk (Turkish BERT)
lm_eval --tasks nli_tr --model hf --model_args pretrained=dbmdz/bert-base-turkish-cased --batch_size 16

# Test with mBERT
lm_eval --tasks nli_tr --model hf --model_args pretrained=bert-base-multilingual-cased --batch_size 16
```

**Expected Performance**: ~80-84% accuracy for fine-tuned models, ~55-65% for zero-shot LLMs.

---

## 2. Winogrande-TR (Turkish Winogrande)

**Paper**: Based on [Winogrande](https://arxiv.org/abs/1907.10641) (AAAI 2020)

### Task
| Task | Validation Size |
|------|-----------------|
| `winogrande_tr` | 1,266 |

### Baseline Estimates
| Model | Expected Acc |
|-------|--------------|
| BERTurk | ~65-70% |
| mBERT | ~60-65% |
| Random | 50% |

### Recommended Testing

```bash
# Test with BERTurk
lm_eval --tasks winogrande_tr --model hf --model_args pretrained=dbmdz/bert-base-turkish-cased

# Test with Llama-3.1 (multilingual)
lm_eval --tasks winogrande_tr --model hf --model_args pretrained=meta-llama/Llama-3.1-8B-Instruct --batch_size 4
```

**Expected Performance**: ~60-70% for multilingual models (vs. 50% random baseline).

---

## 3. FarsTail (Farsi NLI)

**Paper**: [FarsTail: A Persian Natural Language Inference Dataset](https://arxiv.org/abs/2009.08820)

### Task
| Task | Test Size |
|------|-----------|
| `farstail` | 1,564 |

### Baseline Results (from paper)
| Model | Test Accuracy |
|-------|---------------|
| ParsBERT | 83.1% |
| mBERT | 81.2% |
| XLM-R | 82.5% |
| DeepSentiPers | 79.4% |

### Recommended Testing

```bash
# Test with ParsBERT (Persian BERT)
lm_eval --tasks farstail --model hf --model_args pretrained=HooshvareLab/bert-fa-zwnj-base

# Test with multilingual BERT
lm_eval --tasks farstail --model hf --model_args pretrained=bert-base-multilingual-cased
```

**Expected Performance**: ~81-83% for fine-tuned Persian models, ~50-60% for zero-shot.

---

## 4. Persian QA

**Paper**: Community dataset based on Persian Wikipedia

### Task
| Task | Validation Size |
|------|-----------------|
| `persian_qa` | 930 |

### Baseline Estimates
| Model | Expected F1 | Expected EM |
|-------|-------------|-------------|
| ParsBERT | ~75-80% | ~65-70% |
| mBERT | ~70-75% | ~60-65% |

### Recommended Testing

```bash
# Test with ParsBERT
lm_eval --tasks persian_qa --model hf --model_args pretrained=HooshvareLab/bert-fa-zwnj-base --limit 200

# Test with multilingual model
lm_eval --tasks persian_qa --model hf --model_args pretrained=google/mt5-base --limit 200
```

**Expected Performance**: ~65-80% F1 for Persian-specialized models.

---

## 5. SynTran-FA (Farsi Fluent QA)

**Paper**: [SynTran-fa: Generating Comprehensive Answers for Farsi QA Pairs](https://doi.org/10.20944/preprints202410.1684.v1)

### Task
| Task | Size |
|------|------|
| `syntran_fa` | 48,106 |

### Baseline
No published LLM baselines. This is a newer dataset for generating fluent answers.

### Recommended Testing

```bash
# Test with ParsBERT (limited sample)
lm_eval --tasks syntran_fa --model hf --model_args pretrained=HooshvareLab/bert-fa-zwnj-base --limit 500

# Test with mT5
lm_eval --tasks syntran_fa --model hf --model_args pretrained=google/mt5-base --limit 500
```

**Expected Performance**: Evaluate using exact_match; expect ~20-40% for generative models.

---

## 6. XCOMPS (Cross-lingual Compositionality)

**Paper**: [COMPS: Conceptual Minimal Pair Sentences](https://aclanthology.org/2023.eacl-main.213/) (EACL 2023)

### Tasks (17 languages)
| Relevant Tasks | Language |
|----------------|----------|
| `xcomps_fa` | Farsi |
| `xcomps_tr` | Turkish |
| `xcomps_zh` | Chinese |
| `xcomps_ar` | Arabic |
| `xcomps` | All 17 |

### Baseline Results (from paper)
| Model | Average Acc (across langs) |
|-------|---------------------------|
| XLM-R-large | ~75% |
| mBERT | ~68% |
| GPT-3 (davinci) | ~72% |

### Recommended Testing

```bash
# Test specific languages
lm_eval --tasks xcomps_fa,xcomps_tr,xcomps_zh --model hf --model_args pretrained=xlm-roberta-base

# Test all languages
lm_eval --tasks xcomps --model hf --model_args pretrained=xlm-roberta-large --batch_size 8
```

**Expected Performance**: ~65-80% depending on language and model.

---

## 7. MultiLoKo (Multilingual Local Knowledge)

**Paper**: [MultiLoKo: A Multilingual Local Knowledge Benchmark](https://arxiv.org/abs/2504.10356)

### Tasks (31 languages)
| Relevant Tasks | Language |
|----------------|----------|
| `multiloko_farsi` | Farsi |
| `multiloko_turkish` | Turkish |
| `multiloko_simplified_mandarin` | Chinese (Simplified) |
| `multiloko_traditional_mandarin` | Chinese (Traditional) |
| `multiloko_english` | English |

### Baseline Results (from paper)
| Model | Avg EM (31 langs) |
|-------|-------------------|
| GPT-4 | ~55% |
| Llama-3.1-70B | ~48% |
| Llama-3.1-8B | ~38% |
| Mistral-7B | ~32% |

### Recommended Testing

```bash
# Test key SOAR languages
lm_eval --tasks multiloko_farsi,multiloko_turkish,multiloko_simplified_mandarin --model hf --model_args pretrained=meta-llama/Llama-3.1-8B-Instruct --batch_size 4

# Test with Qwen for Chinese
lm_eval --tasks multiloko_simplified_mandarin --model hf --model_args pretrained=Qwen/Qwen2-7B-Instruct --batch_size 4
```

**Expected Performance**: ~30-55% exact match depending on model and language.

---

## 8. CLUE (Chinese Language Understanding)

**Paper**: [CLUE: A Chinese Language Understanding Evaluation Benchmark](https://aclanthology.org/2020.coling-main.419/) (COLING 2020)

### Tasks
| Task | Type | Validation Size |
|------|------|-----------------|
| `clue_cmnli` | NLI | 12,241 |
| `clue_ocnli` | NLI | 2,950 |
| `clue_cluewsc` | Coreference | 304 |

### Baseline Results (from CLUE leaderboard)
| Model | CMNLI | OCNLI | CLUEWSC |
|-------|-------|-------|---------|
| BERT-base-Chinese | 79.7% | 73.5% | 70.4% |
| RoBERTa-wwm-ext | 83.4% | 76.0% | 74.0% |
| ERNIE 3.0 | 84.5% | 79.1% | 84.5% |
| Human | 90.3% | 90.3% | 98.0% |

### Recommended Testing

```bash
# Test with BERT-base-Chinese
lm_eval --tasks clue --model hf --model_args pretrained=bert-base-chinese

# Test with Chinese RoBERTa
lm_eval --tasks clue --model hf --model_args pretrained=hfl/chinese-roberta-wwm-ext

# Test with Qwen (Chinese LLM)
lm_eval --tasks clue --model hf --model_args pretrained=Qwen/Qwen2-7B-Instruct --batch_size 4
```

**Expected Performance**: ~75-85% for fine-tuned models, ~60-75% for zero-shot LLMs.

---

## 9. COMPS (English Compositionality)

**Paper**: [COMPS: Conceptual Minimal Pair Sentences](https://aclanthology.org/2023.eacl-main.213/) (EACL 2023)

### Tasks
| Task | Config | Size |
|------|--------|------|
| `comps_base` | base | 49,340 |
| `comps_wugs` | wugs | ~10,000 |
| `comps_wugs_dist` | wugs_dist | ~10,000 |

### Baseline Results (from paper)
| Model | Base Acc | Wugs Acc |
|-------|----------|----------|
| GPT-2 Large | 64.2% | 58.1% |
| GPT-3 (davinci) | 71.5% | 63.4% |
| RoBERTa-large | 68.3% | 60.2% |
| Human | 94.0% | 91.0% |

### Recommended Testing

```bash
# Test with GPT-2
lm_eval --tasks comps --model hf --model_args pretrained=gpt2-large

# Test with Llama
lm_eval --tasks comps --model hf --model_args pretrained=meta-llama/Llama-3.1-8B --batch_size 4
```

**Expected Performance**: ~60-75% for LLMs (vs. 94% human baseline).

---

## 10. EWoK (Elements of World Knowledge)

**Paper**: [Elements of World Knowledge (EWoK)](https://arxiv.org/abs/2405.09605)

### Task
| Task | Size |
|------|------|
| `ewok` | 8,748 |

### Baseline Results (from paper)
| Model | Accuracy |
|-------|----------|
| GPT-4 | ~85% |
| Claude-3-Opus | ~83% |
| Llama-3-70B | ~78% |
| Llama-3-8B | ~72% |
| GPT-2 | ~55% |
| Random | 50% |

### Recommended Testing

```bash
# Test with GPT-2
lm_eval --tasks ewok --model hf --model_args pretrained=gpt2-large

# Test with Llama-3
lm_eval --tasks ewok --model hf --model_args pretrained=meta-llama/Llama-3.1-8B --batch_size 4

# Test with Mistral
lm_eval --tasks ewok --model hf --model_args pretrained=mistralai/Mistral-7B-Instruct-v0.2 --batch_size 4
```

**Expected Performance**: ~55-85% depending on model size and capability.

---

## 11. ANALOGICAL (Analogy Reasoning)

**Paper**: [ANALOGICAL - A Novel Benchmark for Long Text Analogy Evaluation](https://arxiv.org/abs/2305.05050)

### Tasks
| Task | Config | Test Size |
|------|--------|-----------|
| `analogical_bats` | bats | 1,799 |
| `analogical_google` | google | 500 |
| `analogical_sat` | sat | varies |
| `analogical_u2` | u2 | varies |
| `analogical_u4` | u4 | varies |
| `analogical_scan` | scan | varies |

### Baseline Results (from paper)
| Model | BATS | Google | SAT |
|-------|------|--------|-----|
| GPT-4 | 78.3% | 82.1% | 76.5% |
| GPT-3.5 | 65.2% | 71.4% | 62.3% |
| Llama-2-70B | 58.4% | 63.2% | 55.1% |
| BERT-large | 42.1% | 48.5% | 38.2% |

### Recommended Testing

```bash
# Test with BERT
lm_eval --tasks analogical --model hf --model_args pretrained=bert-large-uncased

# Test with Llama
lm_eval --tasks analogical_bats,analogical_google --model hf --model_args pretrained=meta-llama/Llama-3.1-8B --batch_size 4
```

**Expected Performance**: ~40-80% depending on model capability.

---

## Comprehensive Test Commands

### Quick Validation (All New Tasks)

```bash
# Quick test with dummy model (verify task loading)
lm_eval --model dummy --tasks nli_tr,winogrande_tr,farstail,persian_qa,xcomps_fa,xcomps_tr,xcomps_zh,multiloko_turkish,multiloko_farsi,clue,comps,ewok,analogical_bats,syntran_fa --limit 5
```

### By Language Group

```bash
# Turkish benchmarks
lm_eval --tasks nli_tr,winogrande_tr,xcomps_tr,multiloko_turkish --model hf --model_args pretrained=dbmdz/bert-base-turkish-cased --limit 100

# Farsi benchmarks
lm_eval --tasks farstail,persian_qa,xcomps_fa,multiloko_farsi,syntran_fa --model hf --model_args pretrained=HooshvareLab/bert-fa-zwnj-base --limit 100

# Chinese benchmarks
lm_eval --tasks clue,xcomps_zh,multiloko_simplified_mandarin --model hf --model_args pretrained=bert-base-chinese --limit 100

# English benchmarks
lm_eval --tasks comps,ewok,analogical --model hf --model_args pretrained=gpt2-large --limit 100
```

### With State-of-the-Art Models

```bash
# Multilingual model (all languages)
lm_eval --tasks nli_tr,farstail,clue_cmnli,xcomps --model hf --model_args pretrained=xlm-roberta-large --batch_size 8

# Llama-3.1 (comprehensive test)
lm_eval --tasks ewok,comps,analogical_bats,multiloko_english --model hf --model_args pretrained=meta-llama/Llama-3.1-8B-Instruct --batch_size 4
```

---

## Notes

1. **Fine-tuned vs Zero-shot**: Reported baselines are often from fine-tuned models. Zero-shot LLM performance may be lower.
2. **Batch Size**: Adjust `--batch_size` based on GPU memory.
3. **Limit**: Use `--limit N` for quick validation before full runs.
4. **Trust Remote Code**: Some datasets require `--trust_remote_code` flag.
5. **Generation Tasks**: MultiLoKo, Persian QA, and SynTran-FA are generation tasks; use appropriate models.
