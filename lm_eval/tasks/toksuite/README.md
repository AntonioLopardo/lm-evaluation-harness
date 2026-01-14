# TokSuite: Tokenizer Robustness Benchmark

### Paper

**Title**: TokSuite: Measuring the Impact of Tokenizer Choice on Language Model Behavior

**Authors**: Gül Sena Altıntaş, Malikeh Ehghaghi, Brian Lester, Fengyuan Liu, Wanru Zhao, Marco Ciccone, Colin Raffel

**Affiliations**: University of Toronto, Vector Institute, Google DeepMind, McGill University, Mila, University of Cambridge, Hugging Face

**Paper**: https://arxiv.org/abs/2512.20757

**HuggingFace**: https://huggingface.co/collections/toksuite/toksuite-benchmarks

### Description

TokSuite is a comprehensive benchmark for measuring tokenizer robustness. It tests how model performance degrades when text is subjected to real-world perturbations that affect tokenization.

The benchmark includes:
- **5 languages**: English (EN), Turkish (TR), Italian (IT), Farsi (FA), Mandarin Chinese (ZH)
- **~5,000 samples** across multiple perturbation types
- **14 text-matched models** trained with identical architectures but different tokenizers

### Perturbation Types

| Category | Examples |
|----------|----------|
| **Input** | Non-native keyboard, romanization |
| **Diacritics** | Optional diacritics (Farsi, Turkish) |
| **Orthographic Errors** | Spelling mistakes, typos |
| **Morphological** | Derivations, inflections, contractions |
| **Noise** | Homoglyphs, OCR errors, spacing |
| **LaTeX** | Math notation formatting |
| **STEM** | Scientific diagrams and notations |
| **Unicode** | Unicode styling characters |

### Tasks

#### Canonical (Clean) Baselines
| Task | Lang | Samples | Description |
|------|------|---------|-------------|
| `toksuite_english_canonical` | EN | 40 | Clean English baseline |
| `toksuite_turkish_canonical` | TR | 40 | Clean Turkish baseline |
| `toksuite_farsi_canonical` | FA | 40 | Clean Farsi baseline |
| `toksuite_chinese_canonical` | ZH | 40 | Clean Chinese baseline |
| `toksuite_italian_canonical` | IT | 40 | Clean Italian baseline |
| `toksuite_stem_canonical` | EN | — | STEM domain baseline |
| `toksuite_math_canonical` | EN | — | Math domain baseline |
| `toksuite_general_canonical` | EN | — | General domain baseline |

#### Perturbation Variants (English)
| Task | Perturbation Type |
|------|-------------------|
| `toksuite_english_ocr_errors` | OCR recognition errors |
| `toksuite_english_keyboard_errors` | Keyboard proximity typos |
| `toksuite_english_homoglyphs` | Unicode lookalike characters |

### Results

| Task | Qwen2-1.5B (acc) | Qwen2-1.5B (acc_norm) | Notes |
|------|------------------|----------------------|-------|
| `toksuite_english_canonical` | **95%** | **100%** | Clean baseline |
| `toksuite_english_ocr_errors` | 83% | 93% | -12% from OCR |
| `toksuite_english_keyboard_errors` | 93% | 95% | -2% from typos |
| `toksuite_english_homoglyphs` | 87.5% | 97.5% | -7.5% from homoglyphs |
| `toksuite_turkish_canonical` | 55% | 55% | Lower on Turkish |
| `toksuite_farsi_canonical` | 52.5% | 60% | Arabic script challenge |
| `toksuite_chinese_canonical` | 85% | 85% | Good on Chinese |

### Key Findings from Paper

1. **Tokenizer choice significantly impacts robustness**: Different tokenizers show up to 20% performance differences on perturbations
2. **Byte-level tokenizers (ByT5) are more robust**: Better handling of OCR errors and Unicode
3. **Multilingual tokenizers vary widely**: Some struggle with non-Latin scripts
4. **Trade-offs exist**: Efficiency vs. robustness, vocabulary size vs. coverage

### Usage

```bash
# Run all canonical baselines
lm_eval --model hf --model_args pretrained=Qwen/Qwen2-7B-Instruct \
    --tasks toksuite --batch_size 8

# Test English with perturbations
lm_eval --model hf --model_args pretrained=Qwen/Qwen2-7B-Instruct \
    --tasks toksuite_english_canonical,toksuite_english_ocr_errors,toksuite_english_homoglyphs \
    --batch_size 8

# Compare robustness: canonical vs perturbation
# Robustness = (acc_canonical - acc_perturbed) / acc_canonical
```

### Extending to More Perturbations

Each language has multiple perturbation configs available. You can create additional tasks by copying the YAML pattern:

```yaml
include: _toksuite_template.yaml
task: toksuite_english_<perturbation>
dataset_path: toksuite/tokenizer_robustness_completion_english
dataset_name: tokenizer_robustness_completion_english_<perturbation>
```

Available perturbations for English (30 total):
- `abbreviations`, `capitalization`, `character_deletion`, `character_substitution`
- `colloquial`, `compounds`, `contractions`, `date_formats`
- `emoji_substitution`, `grammatical_errors`, `historical_spelling`
- `homoglyphs`, `hyphenated_spelling`, `inflections`, `keyboard_proximity_errors`
- `letter_repetition_for_emphasis`, `lowercase`, `macron_diacritic`, `ocr_errors`
- `orthographic_errors`, `scripted_text`, `similar_words`, `space_removal`
- `spaced_styling`, `spelled_out`, `superscript_subscript_styling`
- `web_search_query`, `word_reordering`

### Citation

```bibtex
@article{altintas2024toksuite,
  title={TokSuite: Measuring the Impact of Tokenizer Choice on Language Model Behavior},
  author={Altıntaş, Gül Sena and Ehghaghi, Malikeh and Lester, Brian and Liu, Fengyuan and Zhao, Wanru and Ciccone, Marco and Raffel, Colin},
  journal={arXiv preprint arXiv:2512.20757},
  year={2024}
}
```
