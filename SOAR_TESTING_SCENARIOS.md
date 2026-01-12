# SOAR Benchmarks Testing Scenarios

This document outlines testing scenarios for reproducing baseline results from the source papers.

---

## Quick Reference: Recommended Models by Language

| Language | Encoder Models | Decoder/Generative Models |
|----------|----------------|---------------------------|
| **English** | `bert-base-uncased`, `roberta-base` | `gpt2`, `gpt2-medium`, `meta-llama/Llama-3.1-8B` |
| **French** | `camembert-base`, `flaubert/flaubert_base_cased` | `bigscience/bloom-560m` |
| **German** | `bert-base-german-cased`, `dbmdz/bert-base-german-uncased` | `bigscience/bloom-560m` |
| **Chinese** | `bert-base-chinese`, `hfl/chinese-bert-wwm` | `Qwen/Qwen2.5-7B` |
| **Italian** | `dbmdz/bert-base-italian-cased` | `iGeniusAI/Italia-9B-Instruct-v0.1` |
| **Dutch** | `GroNLP/bert-base-dutch-cased` | `bigscience/bloom-560m` |
| **Hindi/Indic** | `ai4bharat/indic-bert` | `ai4bharat/Airavata` |
| **Indonesian** | `indolem/indobert-base-uncased` | `SEACrowd/LLM-indonesian` |
| **Multilingual** | `xlm-roberta-base`, `bert-base-multilingual-cased` | `bigscience/bloom-7b1` |
| **SEA Languages** | `xlm-roberta-base` | `aisingapore/Llama-SEA-LION-v3-8B-IT` |

---

## 1. CLiMP (Chinese Grammaticality)

### Source Paper
- **Title**: CLiMP: Chinese Language Model Evaluation
- **Link**: https://aclanthology.org/2021.eacl-main.242/

### Baseline Results from Paper
| Model | Average Accuracy |
|-------|------------------|
| Chinese BERT | **81.8%** |
| LSTM | ~60% (above chance) |
| 5-gram | ~55% (above chance) |

### Recommended Test
```bash
# Using Chinese BERT (expect ~82% accuracy)
lm_eval --model hf \
  --model_args pretrained=bert-base-chinese \
  --tasks climp \
  --batch_size 16

# Using Qwen for comparison
lm_eval --model hf \
  --model_args pretrained=Qwen/Qwen2.5-7B \
  --tasks climp \
  --batch_size 8
```

### Expected Results
- **Chinese BERT**: ~80-82% average accuracy
- **Best phenomena**: classifier-noun agreement, verb complements
- **Challenging phenomena**: binding, filler-gap dependencies

---

## 2. BLiMP-FR (French Grammaticality)

### Source Paper
- **Title**: BLiMP: Benchmark of Linguistic Minimal Pairs
- **Original**: https://aclanthology.org/2020.tacl-1.25/

### Expected Baselines (extrapolated from English BLiMP)
| Phenomenon | Expected Range |
|------------|----------------|
| Agreement phenomena | 80-95% |
| Binding | 60-75% |
| Complex syntax | 55-70% |

### Recommended Test
```bash
# Using CamemBERT
lm_eval --model hf \
  --model_args pretrained=camembert-base \
  --tasks blimp_fr \
  --batch_size 16

# Using FlauBERT
lm_eval --model hf \
  --model_args pretrained=flaubert/flaubert_base_cased \
  --tasks blimp_fr \
  --batch_size 16
```

### Expected Results
- **CamemBERT**: 70-85% average
- **FlauBERT**: 70-85% average
- Agreement tasks should score highest

---

## 3. COMPS / XCOMPS (Compositionality)

### Source Paper
- **Title**: COMPS: Conceptual Minimal Pair Sentences
- **Link**: https://aclanthology.org/2023.eacl-main.213/

### Baseline Results from Paper
| Model | COMPS Accuracy |
|-------|----------------|
| GPT-2 | ~65% |
| GPT-2 XL | ~70% |
| RoBERTa-large | ~72% |

### Recommended Tests
```bash
# English COMPS with GPT-2
lm_eval --model hf \
  --model_args pretrained=gpt2 \
  --tasks comps \
  --batch_size 16

# XCOMPS multilingual (French)
lm_eval --model hf \
  --model_args pretrained=camembert-base \
  --tasks xcomps_fr \
  --batch_size 16

# XCOMPS multilingual (Chinese)
lm_eval --model hf \
  --model_args pretrained=bert-base-chinese \
  --tasks xcomps_zh \
  --batch_size 16
```

### Expected Results
- **GPT-2 on COMPS**: ~65%
- **Larger models** should perform better
- Cross-lingual performance may lag behind English

---

## 4. Syntax Gym (English Grammaticality)

### Source Paper
- **Title**: SyntaxGym: An Online Platform for Targeted Evaluation
- **Link**: https://aclanthology.org/2020.acl-demos.10/

### Recommended Test
```bash
# Using GPT-2
lm_eval --model hf \
  --model_args pretrained=gpt2 \
  --tasks syntaxgym \
  --batch_size 16

# Using GPT-2 Medium
lm_eval --model hf \
  --model_args pretrained=gpt2-medium \
  --tasks syntaxgym \
  --batch_size 8
```

### Expected Results
- **GPT-2**: 60-70% depending on phenomenon
- Center embedding tasks tend to be harder

---

## 5. IndicGLUE (Hindi, Gujarati, Marathi)

### Source Paper
- **Title**: IndicNLPSuite: Monolingual Corpora and Pre-trained Models
- **Link**: https://aclanthology.org/2020.findings-emnlp.445/

### Baseline Results from Paper
| Task | IndicBERT |
|------|-----------|
| WNLI (Hindi) | ~56% |
| COPA (Hindi) | ~54% |

### Recommended Test
```bash
# Using IndicBERT
lm_eval --model hf \
  --model_args pretrained=ai4bharat/indic-bert \
  --tasks indicglue \
  --batch_size 16

# Using mBERT
lm_eval --model hf \
  --model_args pretrained=bert-base-multilingual-cased \
  --tasks indicglue \
  --batch_size 16
```

### Expected Results
- **IndicBERT**: ~55% on WNLI, ~54% on COPA
- These tasks are challenging (close to random baseline)

---

## 6. IndicMMLU-Pro (9 Indic Languages)

### Source Paper
- **Dataset**: https://huggingface.co/datasets/LinguaLift/IndicMMLU-Pro

### Recommended Test
```bash
# Using Airavata (Hindi-focused)
lm_eval --model hf \
  --model_args pretrained=ai4bharat/Airavata \
  --tasks indicmmlu_pro_hi \
  --batch_size 4 \
  --limit 500

# Using multilingual model
lm_eval --model hf \
  --model_args pretrained=bigscience/bloom-7b1 \
  --tasks indicmmlu_pro \
  --batch_size 4 \
  --limit 100
```

### Expected Results
- 10-way multiple choice (random = 10%)
- Strong multilingual models: 25-40%
- Language-specific models may perform better on their target language

---

## 7. WinoX (German, French, Russian Coreference)

### Source Paper
- **Title**: Wino-X: Multilingual Winograd Schemas
- **Link**: https://aclanthology.org/2021.emnlp-main.670/

### Baseline Results from Paper
| Model | German | French | Russian |
|-------|--------|--------|---------|
| XLM-R | ~54% | ~55% | ~52% |
| mBERT | ~51% | ~52% | ~50% |

### Recommended Test
```bash
# Using XLM-RoBERTa
lm_eval --model hf \
  --model_args pretrained=xlm-roberta-base \
  --tasks winox \
  --batch_size 16

# German only with German BERT
lm_eval --model hf \
  --model_args pretrained=bert-base-german-cased \
  --tasks winox_de \
  --batch_size 16
```

### Expected Results
- **XLM-R**: ~52-55% (challenging - close to random)
- Winograd schemas are notoriously difficult

---

## 8. FLUE (French NLI)

### Source Paper
- **Title**: FlauBERT: Unsupervised Language Model Pre-training for French
- **Link**: https://aclanthology.org/2020.lrec-1.667/

### Baseline Results from Paper
| Model | XNLI Accuracy |
|-------|---------------|
| FlauBERT-base | ~78% |
| CamemBERT | ~81% |
| mBERT | ~76% |

### Recommended Test
```bash
# Using CamemBERT (expect ~81%)
lm_eval --model hf \
  --model_args pretrained=camembert-base \
  --tasks flue_xnli \
  --batch_size 16

# Using FlauBERT (expect ~78%)
lm_eval --model hf \
  --model_args pretrained=flaubert/flaubert_base_cased \
  --tasks flue_xnli \
  --batch_size 16
```

### Expected Results
- **CamemBERT**: ~80-82%
- **FlauBERT**: ~77-79%

---

## 9. DUMB (Dutch)

### Source Paper
- **Title**: DUMB: A Benchmark for Smart Evaluation of Dutch Models
- **Link**: https://openreview.net/pdf?id=ZSHcpMXWxX
- **Leaderboard**: https://dumbench.nl/

### Baseline Results from Paper
| Task | BERTje | RobBERT |
|------|--------|---------|
| CoLA | ~75% | ~78% |
| SICK-NL | ~82% | ~84% |
| DBRD | ~93% | ~94% |

### Recommended Test
```bash
# Using RobBERT (Dutch RoBERTa)
lm_eval --model hf \
  --model_args pretrained=pdelobelle/robbert-v2-dutch-base \
  --tasks dumb \
  --batch_size 16

# Using BERTje
lm_eval --model hf \
  --model_args pretrained=GroNLP/bert-base-dutch-cased \
  --tasks dumb \
  --batch_size 16
```

### Expected Results
- **CoLA**: 75-80%
- **SICK-NL**: 80-85%
- **DBRD**: 90-95%

---

## 10. SEA-HELM (Southeast Asian Languages)

### Source Paper
- **Title**: SEA-HELM: Southeast Asian Holistic Evaluation
- **Link**: https://arxiv.org/abs/2502.14301

### Recommended Test
```bash
# Using SEA-LION
lm_eval --model hf \
  --model_args pretrained=aisingapore/Llama-SEA-LION-v3-8B-IT \
  --tasks seahelm \
  --batch_size 4 \
  --limit 200

# Using XLM-RoBERTa (baseline)
lm_eval --model hf \
  --model_args pretrained=xlm-roberta-base \
  --tasks seahelm_nli \
  --batch_size 16
```

### Expected Results
- **SEA-LION** should outperform generic multilingual models
- NLI: 50-70% depending on language
- Sentiment: 60-80%

---

## 11. BATAYAN (Filipino/Tagalog)

### Source Paper
- **Title**: BATAYAN: A Filipino NLP Benchmark
- **Link**: https://aclanthology.org/2025.acl-long.1509/

### Recommended Test
```bash
# Using SEA-LION (native Filipino support)
lm_eval --model hf \
  --model_args pretrained=aisingapore/Llama-SEA-LION-v3-8B-IT \
  --tasks batayan \
  --batch_size 4

# Using XLM-RoBERTa
lm_eval --model hf \
  --model_args pretrained=xlm-roberta-large \
  --tasks batayan \
  --batch_size 8
```

### Expected Results
- SEA-specific models should perform better
- NLI: 45-60%
- Sentiment: 60-75%

---

## 12. CLUE (Chinese)

### Recommended Test
```bash
# Using Chinese BERT
lm_eval --model hf \
  --model_args pretrained=bert-base-chinese \
  --tasks clue \
  --batch_size 16

# Using Qwen
lm_eval --model hf \
  --model_args pretrained=Qwen/Qwen2.5-7B \
  --tasks clue \
  --batch_size 4
```

---

## 13. EWoK (English World Knowledge)

### Source Paper
- **Title**: EWoK: Elements of World Knowledge
- **Link**: https://arxiv.org/abs/2405.09605

### Baseline Results from Paper
| Model | Accuracy |
|-------|----------|
| GPT-4 | ~82% |
| Claude-3 | ~80% |
| LLaMA-2 70B | ~72% |
| GPT-2 XL | ~55% |

### Recommended Test
```bash
# Using GPT-2 (lower bound)
lm_eval --model hf \
  --model_args pretrained=gpt2-xl \
  --tasks ewok \
  --batch_size 8

# Using LLaMA
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-3.1-8B \
  --tasks ewok \
  --batch_size 4
```

### Expected Results
- **GPT-2 XL**: ~55%
- **LLaMA-8B**: ~65-70%
- Larger models should approach 80%+

---

## 14. ITALIC (Italian)

### Source Paper
- **Title**: ITALIC: Italian Language and Culture Benchmark
- **Link**: https://aclanthology.org/2024.lrec-main.648/

### Recommended Test
```bash
# Using Italian-specific model
lm_eval --model hf \
  --model_args pretrained=iGeniusAI/Italia-9B-Instruct-v0.1 \
  --tasks italic \
  --batch_size 4 \
  --limit 500

# Using mBERT
lm_eval --model hf \
  --model_args pretrained=bert-base-multilingual-cased \
  --tasks italic \
  --batch_size 16 \
  --limit 500
```

---

## 15. ITA-Bench (Italian Translations)

### Recommended Test
```bash
# Full suite with Italian model
lm_eval --model hf \
  --model_args pretrained=iGeniusAI/Italia-9B-Instruct-v0.1 \
  --tasks ita_bench \
  --batch_size 4

# Compare with English equivalents
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-3.1-8B \
  --tasks ita_bench \
  --batch_size 4
```

### Expected Results
Compare to English benchmarks - Italian should be somewhat lower due to translation effects.

---

## 16. MultiLoKo (31 Languages)

### Source Paper
- **Link**: https://arxiv.org/abs/2504.10356

### Recommended Test
```bash
# Test subset of languages
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-3.1-8B \
  --tasks multiloko \
  --batch_size 4 \
  --limit 100
```

---

## Quick Smoke Tests

For quick validation that tasks load correctly, use the dummy model:

```bash
# Test all SOAR benchmarks with dummy model (no GPU needed)
for task in climp blimp_fr comps xcomps syntaxgym indicglue indicmmlu_pro winox flue dumb seahelm batayan clue ewok italic ita_bench multiloko; do
  echo "Testing $task..."
  lm_eval --model dummy --tasks $task --limit 5 2>/dev/null && echo "✓ $task OK" || echo "✗ $task FAILED"
done
```

---

## Full Evaluation Script

```bash
#!/bin/bash
# full_soar_eval.sh - Run all SOAR benchmarks

MODEL="meta-llama/Llama-3.1-8B"
OUTPUT_DIR="./results/soar_eval_$(date +%Y%m%d)"
BATCH_SIZE=4
LIMIT=500  # Set to null for full eval

mkdir -p $OUTPUT_DIR

# Grammaticality benchmarks
lm_eval --model hf --model_args pretrained=$MODEL \
  --tasks climp,blimp_fr,syntaxgym \
  --batch_size $BATCH_SIZE --limit $LIMIT \
  --output_path $OUTPUT_DIR/grammaticality.json

# Compositionality benchmarks
lm_eval --model hf --model_args pretrained=$MODEL \
  --tasks comps,xcomps \
  --batch_size $BATCH_SIZE --limit $LIMIT \
  --output_path $OUTPUT_DIR/compositionality.json

# NLI benchmarks
lm_eval --model hf --model_args pretrained=$MODEL \
  --tasks flue_xnli,indicglue,seahelm_nli,batayan_nli \
  --batch_size $BATCH_SIZE --limit $LIMIT \
  --output_path $OUTPUT_DIR/nli.json

# World Knowledge
lm_eval --model hf --model_args pretrained=$MODEL \
  --tasks ewok,indicmmlu_pro,italic,ita_bench,multiloko \
  --batch_size $BATCH_SIZE --limit $LIMIT \
  --output_path $OUTPUT_DIR/knowledge.json

echo "Results saved to $OUTPUT_DIR"
```

---

## Notes on Reproducibility

1. **Random Seeds**: Use `--seed 42` for reproducible results
2. **Few-shot**: Some tasks may benefit from `--num_fewshot 5`
3. **Batch Size**: Adjust based on GPU memory
4. **Limit**: Remove `--limit` for full evaluation

## Hardware Requirements

| Task Size | Recommended GPU |
|-----------|-----------------|
| Small (<1K examples) | Any GPU / CPU |
| Medium (1K-10K) | 16GB+ GPU |
| Large (10K+) | 24GB+ GPU or use `--limit` |

For large models (7B+), use:
- `--batch_size 1` or `2`
- `device_map=auto` in model_args
- Consider using vLLM backend: `--model vllm`
