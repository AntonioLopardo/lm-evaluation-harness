# ITA-Bench: Italian Benchmarks for LLM Evaluation

### Paper

**Title**: Towards a More Comprehensive Evaluation for Italian LLMs

**Authors**: Luca Moroni, Simone Conia, Federico Martelli, Roberto Navigli

**Affiliation**: Sapienza University of Rome

**Paper**: https://aclanthology.org/2024.clicit-1.67/

**Repository**: https://github.com/SapienzaNLP/ita-bench

### Description

ITA-Bench is a comprehensive benchmark suite for evaluating Large Language Models on Italian language tasks. It includes:

1. **🌐 Translations**: Italian translations of popular English benchmarks
2. **🔨 Adaptations**: Native Italian datasets adapted for LLM evaluation
3. **🤗 Leaderboard**: Italian versions of HuggingFace leaderboard tasks

### Task Groups

| Group | Description | # Tasks |
|-------|-------------|---------|
| `itabench_trans_it-it` | Italian translations of English benchmarks | 14 |
| `itabench_adapt_mc` | Native Italian adaptations (multiple choice) | 8 |
| `itabench_adapt_cloze` | Native Italian adaptations (cloze) | 8 |
| `itabench_leaderboard_it` | Italian HF leaderboard tasks | 6 |

### Translation Tasks (itabench_trans_it-it)

| Task | Description |
|------|-------------|
| `itabench_arc_challenge_it-it` | ARC Challenge in Italian |
| `itabench_arc_easy_it-it` | ARC Easy in Italian |
| `itabench_boolq_it-it` | BoolQ in Italian |
| `itabench_gsm8k_multichoice_it-it` | GSM8K (math) in Italian |
| `itabench_hellaswag_it-it` | HellaSwag in Italian |
| `itabench_mmlu_multichoice_it-it` | MMLU in Italian |
| `itabench_piqa_it-it` | PIQA in Italian |
| `itabench_sciq_it-it` | SciQ in Italian |
| `itabench_truthful_qa_mc1_it-it` | TruthfulQA MC1 in Italian |
| `itabench_truthful_qa_mc2_it-it` | TruthfulQA MC2 in Italian |
| `itabench_winogrande_it-it` | WinoGrande in Italian |

### Native Italian Adaptations

| Task | Description | Type |
|------|-------------|------|
| `itabench_ami_mc` | Misogyny detection | 🔨 Adaptation |
| `itabench_discotex_mc` | Commonsense & world knowledge | 🔨 Adaptation |
| `itabench_ghigliottinai_mc` | Guess missing concept (word game) | 🔨 Adaptation |
| `itabench_nermud_mc` | Named entity recognition | 🔨 Adaptation |
| `itabench_prelearn_mc` | Concept relationships | 🔨 Adaptation |
| `itabench_pretens_mc` | Concept relationships | 🔨 Adaptation |
| `itabench_quandho_mc` | Italian history QA | 🔨 Adaptation |
| `itabench_wic_mc` | Word-in-context | 🔨 Adaptation |

### Italian Leaderboard Tasks

| Task | Description |
|------|-------------|
| `itabench_leaderboard_bbh_it` | BIG-Bench Hard in Italian (22 tasks) |
| `itabench_leaderboard_gpqa_it` | GPQA in Italian |
| `itabench_leaderboard_math_hard_it` | MATH-Hard in Italian |
| `itabench_leaderboard_mmlu_pro_it` | MMLU-Pro in Italian |
| `itabench_leaderboard_musr_it` | MuSR in Italian |
| `itabench_leaderboard_ifeval_it` | IFEval in Italian |

### Results (Qwen2-1.5B-Instruct, 0-shot)

| Task | acc_norm | Notes |
|------|----------|-------|
| `itabench_arc_challenge_it-it` | **32%** | ~42% in English |
| `itabench_hellaswag_it-it` | **49%** | ~60% in English |
| `itabench_piqa_it-it` | **59%** | ~72% in English |
| `itabench_ami_mc` | **41%** | Native Italian |
| `itabench_ghigliottinai_mc` | **34%** | Italian word game |

### Usage

```bash
# Run all Italian translation tasks
lm_eval --model hf --model_args pretrained=meta-llama/Llama-3.1-8B-Instruct \
    --tasks itabench_trans_it-it

# Run Italian adaptations
lm_eval --model hf --model_args pretrained=meta-llama/Llama-3.1-8B-Instruct \
    --tasks itabench_adapt_mc

# Run Italian leaderboard
lm_eval --model hf --model_args pretrained=meta-llama/Llama-3.1-8B-Instruct \
    --tasks itabench_leaderboard_it
```

### Citation

```bibtex
@inproceedings{moroni-etal-2024-towards,
    title = "Towards a More Comprehensive Evaluation for {I}talian {LLM}s",
    author = "Moroni, Luca and Conia, Simone and Martelli, Federico and Navigli, Roberto",
    booktitle = "Proceedings of the 10th Italian Conference on Computational Linguistics (CLiC-it 2024)",
    month = dec,
    year = "2024",
    address = "Pisa, Italy",
    publisher = "CEUR Workshop Proceedings",
    url = "https://aclanthology.org/2024.clicit-1.67/",
    pages = "584--599",
}
```
