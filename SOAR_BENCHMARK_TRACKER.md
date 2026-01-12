# SOAR Tokenizer Group - Benchmark Tracker

This document tracks which benchmarks from the SOAR Tokenizer Group are available in lm-evaluation-harness and which need to be added.

---

## ✅ Already in Harness

| Benchmark | Harness Task | Languages | Category |
|-----------|--------------|-----------|----------|
| GLUE | `glue` | EN | NLI/Coreference |
| SuperGLUE | `super_glue` | EN | NLI/Coreference (includes COPA) |
| AfriXNLI | `afrixnli` | Hausa, etc. | NLI |
| XNLI | `xnli` | 15 langs | NLI |
| Xwinograd | `xwinograd` | Multi | Coreference |
| winogrande | `winogrande` | EN | Coreference |
| BLiMP | `blimp` | EN | Grammaticality |
| MultiBLiMP | `multiblimp` | 100+ langs (FR, HI, IT incl.) | Grammaticality |
| BLiMP-NL | `blimp_nl` | NL | Grammaticality |
| TurBLiMP | `turblimp` | TR | Grammaticality |
| ZhoBLiMP | `zhoblimp` | ZH | Grammaticality |
| PIQA | `piqa` | EN | Commonsense Reasoning |
| GlobalPIQA | `global_piqa` | Multi | Commonsense Reasoning |
| HellaSWag | `hellaswag` | EN | Commonsense Reasoning |
| mHellaSwag | `okapi/hellaswag_multilingual` | 30+ langs | Commonsense Reasoning |
| XStoryCloze | `xstorycloze` | 11 langs | Commonsense Reasoning |
| Prost | `prost` | EN | Commonsense Reasoning |
| COPA | `super_glue/copa` | EN | Commonsense Reasoning |
| XCOPA | `xcopa` | 11 langs (ID, IT, TR, VI, ZH incl.) | Commonsense Reasoning |
| COPAL-ID | `copal_id` | ID | Commonsense Reasoning |
| Belebele | `belebele` | 122 langs | Reading Comprehension |
| MMLU | `mmlu` | EN | World Knowledge |
| GlobalMMLU | `global_mmlu` | Multi | World Knowledge |
| MMLU-ProX | `mmlu_prox` | Multi | World Knowledge |
| AfriMMLU | `afrimmlu` | Hausa, etc. | World Knowledge |
| INCLUDE | `include` | 44 langs (TL, FR, HI, ID, TR, NL, ZH, IT) | World Knowledge |
| IndoNLI | `indonli` | ID | NLI |
| SEACrowd | `seacrowd` | ID | Various (NLI, Sentiment) |
| SEA-HELM | `seahelm` | ID, TH, VI, TL, TA | NLI, Causal, Sentiment |
| XCOMPS | `xcomps` | FR, NL, TR, ZH, DE, VI, ES | Compositionality |
| IndicGLUE | `indicglue` | HI, GU, MR | NLI (WNLI), COPA |

---

## ⚠️ Known Issues & Notes

### SEACrowd Dependency

**SEACrowd tasks require `datasets<3.0.0`** due to their use of HuggingFace loading scripts (deprecated in datasets 3.0+).

```bash
pip install 'datasets>=2.0.0,<3.0.0'
```

This may conflict with other packages (e.g., `tokenizer-analysis` requires `datasets>=4.0.0`). For most evaluation use cases, this is not an issue.

**SEACrowd Tasks Available:**
| Task | Dataset | Test Size | Description |
|------|---------|-----------|-------------|
| `seacrowd_indonli` | SEACrowd/indonli | 5,183 | Indonesian NLI (3-way) |
| `seacrowd_wrete` | SEACrowd/wrete | 100 | Word Relation Textual Entailment |
| `seacrowd_indolem_sentiment` | SEACrowd/indolem_sentiment | 1,011 | Indonesian Sentiment (binary) |

---

## ❌ To Be Added

### Priority 1 - Explicitly Mentioned in Doc

| Benchmark | Languages | Category | Dataset Source | Status |
|-----------|-----------|----------|----------------|--------|
| IndoNLI | ID | NLI | [HuggingFace](https://huggingface.co/datasets/karuniaperjuangan/indonli_benchmark) | ✅ Added |
| SEACrowd | Multi (SEA) | Various | [GitHub](https://github.com/SEACrowd) | ✅ Added (3 tasks) |
| SEA-HELM | Multi (SEA) | Various | [GitHub](https://github.com/aisingapore/SEA-HELM) | ✅ Added (13 tasks) |

### Priority 2 - NLI / Coreference

| Benchmark | Languages | Category | Dataset Source | Status |
|-----------|-----------|----------|----------------|--------|
| BATAYA | TL (Tagalog) | NLI | TBD | ⬜ Not started |
| COLE/FLUE | FR | NLI | TBD | ⬜ Not started |
| IndicGLUE | HI, GU, MR | NLI + COPA | [HuggingFace](https://huggingface.co/datasets/ai4bharat/indic_glue) | ✅ Added (6 tasks) |
| winoX | Multi | Coreference | TBD | ⬜ Not started |

### Priority 3 - Grammaticality / Linguistic

| Benchmark | Languages | Category | Dataset Source | Status |
|-----------|-----------|----------|----------------|--------|
| QFrBLiMP | FR | Grammaticality | TBD | ⬜ Not started |
| Syntax Gym | EN | Grammaticality | TBD | ⬜ Not started |
| Babies | IT | Grammaticality | TBD | ⬜ Not started |
| LINDSEA | ID | Grammaticality | TBD | ⬜ Not started |
| CLIMP | ZH | Grammaticality | TBD | ⬜ Not started |
| XCOMPS | FR, TR, NL, ZH, DE, VI, ES | Compositionality | [HuggingFace](https://huggingface.co/datasets/fpadovani/xcomps-dataset) | ✅ Added (7 tasks) |
| COMPS | EN | Compositionality | TBD | ⬜ Not started |

### Priority 4 - Commonsense Reasoning

| Benchmark | Languages | Category | Dataset Source | Status |
|-----------|-----------|----------|----------------|--------|
| EWoK | EN | Commonsense | TBD | ⬜ Not started |
| Analogy | EN | Commonsense | TBD | ⬜ Not started |
| ITALIC | IT | Commonsense | TBD | ⬜ Not started |
| COPA-NL | NL | Commonsense | TBD | ⬜ Not started |

### Priority 5 - World Knowledge / MMLU variants

| Benchmark | Languages | Category | Dataset Source | Status |
|-----------|-----------|----------|----------------|--------|
| FilBench | TL (Tagalog) | World Knowledge | TBD | ⬜ Not started |
| MultiLoKg | Multi | World Knowledge | TBD | ⬜ Not started |
| IndicMMLU-Pro | HI | World Knowledge | TBD | ⬜ Not started |
| ITT-Bench | HI, IT | World Knowledge | TBD | ⬜ Not started |
| CLUE | ZH | Various | TBD | ⬜ Not started |
| DUMB | NL | Various | TBD | ⬜ Not started |

---

## Language Coverage Summary

| Language | Code | In Harness | To Add |
|----------|------|------------|--------|
| Tagalog | TL | INCLUDE, Belebele, SEA-HELM | BATAYA, FilBench |
| Thai | TH | XCOPA, mHellaSwag, Belebele, SEA-HELM | - |
| Vietnamese | VI | XCOPA, XStoryCloze, XNLI, Belebele, SEA-HELM | - |
| Tamil | TA | INCLUDE, Belebele, SEA-HELM | - |
| French | FR | MultiBLiMP, mHellaSwag, XNLI, INCLUDE, Belebele | COLE/FLUE, QFrBLiMP, XCOMPS |
| Hausa | HA | AfriXNLI, AfriMMLU, Belebele | - |
| Hindi | HI | MultiBLiMP, XStoryCloze, XNLI, INCLUDE, Belebele | IndicGLUE, IndicMMLU-Pro, ITT-Bench |
| English | EN | GLUE, SuperGLUE, BLiMP, PIQA, HellaSWag, MMLU, etc. | Syntax Gym, COMPS, EWoK, Analogy |
| Italian | IT | MultiBLiMP (ita), XCOPA, INCLUDE, Belebele | Babies, ITALIC, ITT-Bench |
| Indonesian | ID | COPAL-ID, mHellaSwag, XStoryCloze, XCOPA, INCLUDE, Belebele, IndoNLI, SEACrowd, SEA-HELM | LINDSEA |
| Turkish | TR | TurBLiMP, XCOPA, INCLUDE, Belebele | XCOMPS |
| Dutch | NL | BLiMP-NL, mHellaSwag, INCLUDE, Belebele | DUMB, COPA-NL, XCOMPS |
| Chinese | ZH | ZhoBLiMP, mHellaSwag, XStoryCloze, XCOPA, XNLI, INCLUDE, Belebele | CLIMP, CLUE, XCOMPS |

---

## Adding a New Benchmark - Checklist

1. [ ] Find dataset source (HuggingFace preferred)
2. [ ] Understand task format (multiple choice, generation, etc.)
3. [ ] Create task folder in `lm_eval/tasks/`
4. [ ] Write YAML config file
5. [ ] Add any preprocessing utils if needed
6. [ ] Test locally
7. [ ] Update this tracker

---

## Progress Log

| Date | Benchmark | Action | Notes |
|------|-----------|--------|-------|
| 2026-01-12 | - | Initial tracker created | - |
| 2026-01-12 | IndoNLI | ✅ Added | Task: `indonli`, Dataset: `karuniaperjuangan/indonli_benchmark`, 2,201 test examples |
| 2026-01-12 | SEACrowd | ✅ Added | Group: `seacrowd` with 3 tasks. **Requires `datasets<3.0.0`** (see notes above) |
| 2026-01-12 | SEA-HELM | ✅ Added | Group: `seahelm` with 13 tasks across 5 languages. No special dependencies |
| 2026-01-12 | XCOMPS | ✅ Added | Group: `xcomps` with 7 tasks (FR, NL, TR, ZH, DE, VI, ES). Compositionality benchmark |
| 2026-01-12 | IndicGLUE | ✅ Added | Group: `indicglue` with 6 tasks (WNLI + COPA for HI, GU, MR) |

### Benchmarks Added This Session

1. **IndoNLI** (`indonli`)
   - Indonesian Natural Language Inference
   - 3-way classification: Berhubungan (entailment), Netral, Kontradiktif
   - 2,201 test examples
   - No special dependencies

2. **SEACrowd** (`seacrowd` group)
   - `seacrowd_indonli`: Indonesian NLI from SEACrowd (5,183 test)
   - `seacrowd_wrete`: Word Relation Textual Entailment (100 test)
   - `seacrowd_indolem_sentiment`: Sentiment Analysis (1,011 test)
   - ⚠️ Requires `datasets<3.0.0`

3. **SEA-HELM** (`seahelm` group) - 13 tasks
   - NLI: `seahelm_nli_{id,th,vi,tl,ta}` (1,000 test each)
   - Causal Reasoning: `seahelm_causal_{id,th,vi,tl}` (500 test each)
   - Sentiment: `seahelm_sentiment_{id,th,vi,tl}` (400 test each)
   - Languages: Indonesian, Thai, Vietnamese, Tagalog, Tamil
   - No special dependencies ✓

4. **XCOMPS** (`xcomps` group) - 7 tasks
   - Tasks: `xcomps_{fr,nl,tr,zh,de,vi,es}`
   - Cross-lingual compositionality benchmark
   - Dataset: `fpadovani/xcomps-dataset`
   - Acceptable vs. unacceptable sentence pairs
   - No special dependencies ✓

5. **IndicGLUE** (`indicglue` group) - 6 tasks
   - COPA: `indicglue_copa_{hi,gu,mr}` (commonsense reasoning)
   - WNLI: `indicglue_wnli_{hi,gu,mr}` (natural language inference)
   - Languages: Hindi, Gujarati, Marathi
   - Dataset: `ai4bharat/indic_glue`
   - No special dependencies ✓

