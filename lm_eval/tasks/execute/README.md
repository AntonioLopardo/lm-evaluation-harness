# EXECUTE: Multilingual Benchmark for LLM Token Understanding

### Paper

**Title**: EXECUTE: A Multilingual Benchmark for LLM Token Understanding

**Authors**: Lukas Edman, Helmut Schmid, Alexander Fraser (TU Munich, LMU Munich)

**Paper**: https://aclanthology.org/2025.findings-acl.95/

**Repository**: https://github.com/Leukas/EXECUTE

### Description

EXECUTE extends the [CUTE benchmark](../cute/) to multiple languages with diverse scripts and writing systems. It tests whether LLMs can understand and manipulate character sequences across different language types:

| Language | Script | Writing System | Tokenization |
|----------|--------|----------------|--------------|
| Amharic | Ge'ez | Abugida | Byte-level |
| Arabic | Arabic | Abjad | ~2.4 tokens/word |
| Chinese | Simp. Han | Logographic | ~1.25 tokens/word |
| English | Latin | Alphabet | ~1.32 tokens/word |
| German | Latin | Alphabet | Similar to English |
| Hindi | Devanagari | Abugida | ~2.8 tokens/word |
| Japanese | Japanese | Mixed | ~1.27 tokens/word |
| Korean | Hangul | Featural | ~2.7 tokens/word |
| Russian | Cyrillic | Alphabet | ~2.4 tokens/word |
| Spanish | Latin | Alphabet | Similar to English |

### Tasks

Same 12 tasks as CUTE, applied across all languages:

| Category | Tasks | Description |
|----------|-------|-------------|
| **Composition** | `spell`, `spell_inverse`, `contains_char`, `contains_word` | Understanding token composition |
| **Manipulation** | `ins_*`, `del_*`, `sub_*`, `swap_*` | Character/word manipulation |

### Available Task Configs

Tasks are named as `execute_{lang}_{task}` where:
- `lang`: ISO-3 code (eng, ara, zho, jpn, kor, rus, hin, deu, spa)
- `task`: Task name (spell, spell_inverse, contains_char, del_char, etc.)

### Usage

```bash
# Run a specific language/task
lm_eval --model hf --model_args pretrained=Qwen/Qwen2-7B-Instruct \
    --tasks execute_eng_spell,execute_zho_spell,execute_ara_spell \
    --batch_size 8

# Run all English tasks
lm_eval --model hf --model_args pretrained=Qwen/Qwen2-7B-Instruct \
    --tasks execute_eng_spell,execute_eng_spell_inverse,execute_eng_contains_char \
    --batch_size 8
```

### Results

Tested with Qwen2-1.5B-Instruct (limit=50):

| Language | Spell | Notes |
|----------|-------|-------|
| English | 90% | Strong performance |
| Chinese | 96% | Best - logographic (1-2 chars/word) |
| Korean | 28% | Hangul syllable blocks |
| Arabic | 12% | Abjad script, right-to-left |

### Key Findings from Paper

1. **Language-specific challenges**: Different scripts present different difficulties
2. **CWT correlation**: Results correlate with character-word-token statistics
3. **Inverse pattern**: Less language knowledge → better EXECUTE performance (fewer shortcuts)
4. **Sub-character tasks**: CJK languages have additional sub-character understanding tasks

### Prerequisites

Requires the EXECUTE dataset to be cloned:
```bash
git clone https://github.com/Leukas/EXECUTE.git /home/execute_benchmark
```

### Citation

```bibtex
@inproceedings{edman2025execute,
  title={EXECUTE: A Multilingual Benchmark for LLM Token Understanding},
  author={Edman, Lukas and Schmid, Helmut and Fraser, Alexander},
  booktitle={Findings of ACL},
  year={2025}
}
```
