# SOAR Benchmark Tracker v2

Cross-reference of benchmarks from "SOAR Tokenizer Group Main Doc (1).pdf" with lm-evaluation-harness.

---

## English

| Benchmark | Task | Status | Source |
|-----------|------|--------|--------|
| GLUE | `glue` | ✅ Already in harness | - |
| SuperGLUE | `superglue` | ✅ Already in harness | - |
| Winogrande | `winogrande` | ✅ Already in harness | - |
| MultiBLiMP | `multiblimp` | ✅ Already in harness | - |
| BLiMP | `blimp` | ✅ Already in harness | - |
| **COMPS** | `comps` | ✅ **Added** | [kanishka/comps](https://huggingface.co/datasets/kanishka/comps) |
| **ANALOGICAL** | `analogical` | ✅ **Added** | [relbert/analogy_questions](https://huggingface.co/datasets/relbert/analogy_questions) |
| **EWoK** | `ewok` | ✅ **Added** | [ewok-core/ewok-core-1.0](https://huggingface.co/datasets/ewok-core/ewok-core-1.0) |
| PIQA | `piqa` | ✅ Already in harness | - |
| Global PIQA | `global_piqa` | ✅ Already in harness | - |
| HellaSwag | `hellaswag` | ✅ Already in harness | - |
| PROST | `prost` | ✅ Already in harness | - |
| Belebele | `belebele` | ✅ Already in harness | - |
| MMLU | `mmlu` | ✅ Already in harness | - |
| MMLU-ProX | `mmlu_prox` | ✅ Already in harness | - |
| Global MMLU | `global_mmlu` | ✅ Already in harness | - |
| BBH (zero shot) | `bbh` | ✅ Already in harness | - |
| XQuAD | `xquad` | ✅ Already in harness | - |

---

## Turkish

| Benchmark | Task | Status | Source |
|-----------|------|--------|--------|
| **winogrande-tr** | `winogrande_tr` | ✅ **Added** | [malhajar/winogrande-tr](https://huggingface.co/datasets/malhajar/winogrande-tr) |
| **nli-tr** | `nli_tr` | ✅ **Added** | [boun-tabi/nli_tr](https://huggingface.co/datasets/boun-tabi/nli_tr) |
| MultiBLiMP | `multiblimp` | ✅ Already in harness | - |
| TurBLiMP | `turblimp` | ✅ Already in harness | - |
| **XCOMPS** | `xcomps_tr` | ✅ **Added** | [fpadovani/xcomps-dataset](https://huggingface.co/datasets/fpadovani/xcomps-dataset) |
| XCOPA | `xcopa` | ✅ Already in harness | - |
| Global PIQA | `global_piqa` | ✅ Already in harness | - |
| Belebele | `belebele` | ✅ Already in harness | - |
| Global MMLU | `global_mmlu` | ✅ Already in harness | - |
| **MultiLoKo** | `multiloko_turkish` | ✅ **Added** | [facebook/multiloko](https://huggingface.co/datasets/facebook/multiloko) |
| INCLUDE | `include` | ✅ Already in harness | - |
| XQuAD | `xquad` | ✅ Already in harness | - |

---

## Chinese

| Benchmark | Task | Status | Source |
|-----------|------|--------|--------|
| **CLUE** | `clue` | ✅ **Added** | [clue/clue](https://huggingface.co/datasets/clue/clue) |
| ZhoBLiMP | `zhoblimp` | ✅ Already in harness | - |
| XWinograd | `xwinograd_zh` | ✅ Already in harness | - |
| Mandarinograd | `xwinograd_zh` | ✅ Covered by XWinograd (504 examples) | [Paper](https://aclanthology.org/2020.lrec-1.3.pdf) |
| **XCOMPS** | `xcomps_zh` | ✅ **Added** | [fpadovani/xcomps-dataset](https://huggingface.co/datasets/fpadovani/xcomps-dataset) |
| XCOPA | `xcopa` | ✅ Already in harness | - |
| XStoryCloze | `xstorycloze` | ✅ Already in harness | - |
| XQuAD | `xquad` | ✅ Already in harness | - |
| m_hellaswag | `mhellaswag` | ✅ Already in harness | - |
| Global PIQA | `global_piqa` | ✅ Already in harness | - |
| Belebele | `belebele` | ✅ Already in harness | - |
| Global MMLU | `global_mmlu` | ✅ Already in harness | - |
| CMMLU | `cmmlu` | ✅ Already in harness | - |
| **MultiLoKo** | `multiloko_simplified_mandarin`, `multiloko_traditional_mandarin`, `multiloko_cantonese` | ✅ **Added** | [facebook/multiloko](https://huggingface.co/datasets/facebook/multiloko) |
| INCLUDE | `include` | ✅ Already in harness | - |
| MMLU-ProX | `mmlu_prox` | ✅ Already in harness | - |

---

## Farsi/Persian

| Benchmark | Task | Status | Source |
|-----------|------|--------|--------|
| MultiBLiMP | `multiblimp` | ✅ Already in harness | - |
| **XCOMPS** | `xcomps_fa` | ✅ **Added** | [fpadovani/xcomps-dataset](https://huggingface.co/datasets/fpadovani/xcomps-dataset) |
| **FarsTail** | `farstail` | ✅ **Added** | [ParsiAI/FarsTail](https://huggingface.co/datasets/ParsiAI/FarsTail) |
| **MultiLoKo** | `multiloko_farsi` | ✅ **Added** | [facebook/multiloko](https://huggingface.co/datasets/facebook/multiloko) |
| INCLUDE | `include` | ✅ Already in harness | - |
| Global MMLU | `global_mmlu` | ✅ Already in harness | - |
| FarsEval-PKBETS | - | ⚠️ Gated (requires access) | [MatinaAI/pkbets](https://huggingface.co/datasets/MatinaAI/pkbets) |
| Syntran-fa | - | ⏭️ Skipped (QA fluency only) | [SLPL/syntran-fa](https://huggingface.co/datasets/SLPL/syntran-fa) |
| **persianQA** | `persian_qa` | ✅ **Added** | [SajjadAyoubi/persian_qa](https://huggingface.co/datasets/SajjadAyoubi/persian_qa) |
| PerCQA | - | ❌ Cannot load (Pdf type error) | [NaghmehAI/PerCQA](https://huggingface.co/datasets/NaghmehAI/PerCQA) |

---

## Summary of New Tasks Added (soar-benchmarks-v2)

| Task Group | Languages | # Tasks | Dataset |
|------------|-----------|---------|---------|
| `nli_tr` | Turkish | 2 | boun-tabi/nli_tr |
| `winogrande_tr` | Turkish | 1 | malhajar/winogrande-tr |
| `farstail` | Farsi | 1 | ParsiAI/FarsTail |
| `persian_qa` | Farsi | 1 | SajjadAyoubi/persian_qa |
| `xcomps` | 17 languages | 17 | fpadovani/xcomps-dataset |
| `multiloko` | 31 languages | 31 | facebook/multiloko |
| `clue` | Chinese | 3 | clue/clue |
| `comps` | English | 3 | kanishka/comps |
| `ewok` | English | 1 | ewok-core/ewok-core-1.0 |
| `analogical` | English | 6 | relbert/analogy_questions |

**Total: 66 new tasks**

---

## Unavailable Benchmarks

| Benchmark | Reason | Alternative |
|-----------|--------|-------------|
| Mandarinograd | GitLab only (not on HF) | ✅ Use `xwinograd_zh` (504 examples, includes CLUE-WSC) |
| FarsEval-PKBETS | Gated (requires access request) | Request access at HF |
| Syntran-fa | QA fluency dataset, not evaluation | persian_qa covers Farsi QA |
| PerCQA | Not a proper HF dataset (only PDF+RAR files) | Use `persian_qa` for Farsi QA |

---

## Quick Test Command

```bash
# Test all new benchmarks
lm_eval --model dummy --tasks nli_tr,winogrande_tr,farstail,persian_qa,xcomps_tr,xcomps_fa,xcomps_zh,multiloko_turkish,multiloko_farsi,clue,comps,ewok --limit 5
```
