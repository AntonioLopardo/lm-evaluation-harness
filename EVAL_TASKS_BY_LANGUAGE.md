# Evaluation Tasks by Language

This document lists lm-eval-harness tasks organized by language for the monolingual training evaluation plan.

**Target Languages:** English, Thai, Vietnamese, Amharic, Urdu

---

## Quick Summary Table

| Benchmark | English | Vietnamese | Thai | Amharic | Urdu | Status |
|-----------|:-------:|:----------:|:----:|:-------:|:----:|--------|
| FLORES NLL | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ Implemented |
| Global MMLU | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ In harness |
| GLUE/SuperGLUE | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ In harness (EN only) |
| VMLU | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ Implemented |
| ViQuAD | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ Implemented |
| Amharic QA | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ Implemented |
| MultiLoko | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ In harness |
| INCLUDE | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ In harness |
| Global PIQA | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ In harness |
| Belebele (mc_full) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ In harness |
| MultiBLiMP | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ In harness |
| BLiMP | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ In harness (EN only) |
| UrBLiMP | ❌ | ❌ | ❌ | ❌ | ❓ | ❌ Not available yet |
| IndicMMLU-Pro | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ Implemented |
| AfriMMLU | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ In harness |
| Winogrande | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ In harness |
| Thai Winograd | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ Implemented |
| XWinograd | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ In harness |
| XCOMPS | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ In harness (no EN) |
| Afri-MCQA | ❌ | ❌ | ❌ | ❓ | ❌ | ❌ Multimodal only |
| XQUAD | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ In harness |
| XCOPA | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ In harness |
| HellaSwag | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ In harness |
| ARC | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ In harness |

---

## Tasks by Language

### 🇺🇸 English

| Task | lm-eval Task Name | Status |
|------|-------------------|--------|
| FLORES NLL | `flores_nll_eng` | ✅ Implemented |
| Global MMLU | `global_mmlu_full_en` | ✅ In harness |
| GLUE | `glue` | ✅ In harness |
| SuperGLUE | `super_glue` | ✅ In harness |
| MultiLoko | `multiloko_english` | ✅ In harness |
| Global PIQA | `global_piqa_eng_latn` | ✅ In harness |
| Belebele | `belebele_mc_full_eng_Latn` | ✅ In harness |
| MultiBLiMP | `multiblimp_eng` | ✅ In harness |
| BLiMP | `blimp` | ✅ In harness |
| Winogrande | `winogrande` | ✅ In harness |
| XWinograd | `xwinograd_en` | ✅ In harness |
| COMPS | `comps` | ✅ In harness |
| XQUAD | `xquad_en` | ✅ In harness |
| COPA | `super_glue` (includes COPA) | ✅ In harness |
| HellaSwag | `hellaswag` | ✅ In harness |
| ARC | `arc_easy`, `arc_challenge` | ✅ In harness |

---

### 🇻🇳 Vietnamese

| Task | lm-eval Task Name | Status |
|------|-------------------|--------|
| FLORES NLL | `flores_nll_vie` | ✅ Implemented |
| Global MMLU | `global_mmlu_full_vi` | ✅ In harness |
| VMLU | `vmlu` | ✅ Implemented |
| ViQuAD | `viquad` | ✅ Implemented |
| MultiLoko | `multiloko_vietnamese` | ✅ In harness |
| INCLUDE | `include_base_44_vietnamese` | ✅ In harness |
| Global PIQA | `global_piqa_vie_latn` | ✅ In harness |
| Belebele | `belebele_mc_full_vie_Latn` | ✅ In harness |
| XCOMPS | `xcomps_vi` | ✅ In harness |
| XQUAD | `xquad_vi` | ✅ In harness |
| XCOPA | `xcopa_vi` | ✅ In harness |
| HellaSwag | `hellaswag_vi` (Okapi) | ✅ In harness |
| ARC | `arc_vi` (Okapi) | ✅ In harness |
| XNLI | `xnli_vi` | ✅ In harness |

---

### 🇹🇭 Thai

| Task | lm-eval Task Name | Status |
|------|-------------------|--------|
| FLORES NLL | `flores_nll_tha` | ✅ Implemented |
| MultiLoko | `multiloko_thai` | ✅ In harness |
| Global PIQA | `global_piqa_tha_thai` | ✅ In harness |
| Belebele | `belebele_mc_full_tha_Thai` | ✅ In harness |
| XQUAD | `xquad_th` | ✅ In harness |
| XCOPA | `xcopa_th` | ✅ In harness |
| Thai Winograd | `winograd_th` | ✅ Implemented |
| Global MMLU | ❌ | ❌ Not available for Thai |
| MultiBLiMP | ❌ | ❌ Not available for Thai |

**Note for Thai:**
- No MMLU-style benchmark available in Global MMLU

---

### 🇪🇹 Amharic

| Task | lm-eval Task Name | Status |
|------|-------------------|--------|
| FLORES NLL | `flores_nll_amh` | ✅ Implemented |
| Global MMLU | `global_mmlu_full_am` | ✅ In harness |
| Amharic QA | `amharic_qa` | ✅ Implemented |
| AfriMMLU | `afrimmlu_direct_amh_prompt_1` | ✅ In harness |
| Global PIQA | `global_piqa_amh_ethi` | ✅ In harness |
| Belebele | `belebele_mc_full_amh_Ethi` | ✅ In harness |
| MultiBLiMP | `multiblimp_amh` | ✅ In harness |
| Afri-MCQA | ❌ | ❌ **Multimodal only** |

**Note:** Afri-MCQA is a VQA (visual question answering) dataset requiring images - cannot be used as text-only.

---

### 🇵🇰 Urdu

| Task | lm-eval Task Name | Status |
|------|-------------------|--------|
| FLORES NLL | `flores_nll_urd` | ✅ Implemented |
| IndicMMLU-Pro | `indicmmlu_pro_urdu` | ✅ Implemented |
| MultiLoko | `multiloko_urdu` | ✅ In harness |
| INCLUDE | `include_base_44_urdu` | ✅ In harness |
| Global PIQA | `global_piqa_urd_arab` | ✅ In harness |
| Belebele | `belebele_mc_full_urd_Arab` | ✅ In harness |
| MultiBLiMP | `multiblimp_urd` | ✅ In harness |
| UrBLiMP | ❌ | ❌ **Not available yet** (arxiv:2508.01006 - future paper) |
| Global MMLU | ❌ | ❌ Not available for Urdu |

---

## Missing Tasks Summary

### Needs Implementation

| Task | Language | Dataset | Priority | Notes |
|------|----------|---------|----------|-------|
| UrBLiMP | Urdu | arxiv:2508.01006 | Low | Paper not yet published |

### Cannot Implement (Blocked)

| Task | Reason |
|------|--------|
| Afri-MCQA (Amharic) | Multimodal VQA - requires images |
| Global MMLU (Thai/Urdu) | Dataset doesn't include these languages |
| VLUE | Original dataset not on HuggingFace |

---

## Running All Tasks

### By Language

```bash
# English
lm_eval --model hf --model_args pretrained=MODEL --tasks \
  flores_nll_eng,global_mmlu_full_en,glue,super_glue,belebele_mc_full_eng_Latn,\
  global_piqa_eng_latn,multiloko_english,multiblimp_eng,blimp,comps,hellaswag,\
  arc_easy,arc_challenge,xquad_en,winogrande,xwinograd_en --batch_size 8

# Vietnamese  
lm_eval --model hf --model_args pretrained=MODEL --tasks \
  flores_nll_vie,global_mmlu_full_vi,vmlu,viquad,belebele_mc_full_vie_Latn,\
  global_piqa_vie_latn,multiloko_vietnamese,include_base_44_vietnamese,\
  xquad_vi,xcopa_vi,xcomps_vi,xnli_vi,hellaswag_vi,arc_vi --batch_size 8

# Thai
lm_eval --model hf --model_args pretrained=MODEL --tasks \
  flores_nll_tha,belebele_mc_full_tha_Thai,global_piqa_tha_thai,multiloko_thai,\
  xquad_th,xcopa_th,winograd_th --batch_size 8

# Amharic
lm_eval --model hf --model_args pretrained=MODEL --tasks \
  flores_nll_amh,amharic_qa,belebele_mc_full_amh_Ethi,global_piqa_amh_ethi,\
  global_mmlu_full_am,afrimmlu_direct_amh_prompt_1,multiblimp_amh --batch_size 8

# Urdu
lm_eval --model hf --model_args pretrained=MODEL --tasks \
  flores_nll_urd,indicmmlu_pro_urdu,belebele_mc_full_urd_Arab,global_piqa_urd_arab,\
  multiloko_urdu,include_base_44_urdu,multiblimp_urd --batch_size 8
```

### All New Implemented Tasks

```bash
lm_eval --model hf --model_args pretrained=MODEL --tasks \
  vmlu,viquad,amharic_qa,indicmmlu_pro_urdu,flores_nll --batch_size 4
```

---

## Task Categories

### Language Modeling / Perplexity
- `flores_nll_*` - Mean NLL on FLORES sentences

### Knowledge / MMLU-style
- `global_mmlu_full_*` - Multilingual MMLU
- `vmlu` - Vietnamese MMLU
- `indicmmlu_pro_urdu` - Urdu MMLU-Pro
- `afrimmlu_direct_*` - African MMLU

### Reading Comprehension / QA
- `belebele_mc_full_*` - Multilingual reading comprehension (full answer scoring)
- `xquad_*` - Extractive QA
- `viquad` - Vietnamese QA
- `amharic_qa` - Amharic QA

### Commonsense Reasoning
- `global_piqa_*` - Physical intuition
- `xcopa_*` - Causal reasoning
- `hellaswag*` - Sentence completion
- `arc_*` - Science QA
- `winogrande` - Coreference

### Linguistic Acceptability
- `blimp` - English grammaticality
- `multiblimp_*` - Multilingual minimal pairs

### NLI / Semantic
- `xnli_*` - Natural language inference
- `xcomps_*` - Compositional semantics

---

*Last updated: 2026-01-23*
