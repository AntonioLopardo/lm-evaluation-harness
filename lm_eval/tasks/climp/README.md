# CLiMP: Chinese Linguistic Minimal Pairs

## Overview

CLiMP is a Chinese grammaticality benchmark in the style of BLiMP (Benchmark of Linguistic Minimal Pairs). It evaluates whether language models can distinguish grammatical from ungrammatical Chinese sentences.

## Dataset

- **Source**: https://huggingface.co/datasets/suchirsalhan/CLiMP
- **Language**: Chinese (Simplified)
- **Task Type**: Multiple-choice (forced choice between grammatical/ungrammatical)
- **Size**: ~15,000 pairs (15 phenomena × 1,000 pairs each)

## Linguistic Phenomena

1. **anaphor_agreement_gender** - Anaphor gender agreement
2. **binding_gender** - Binding constraints with gender
3. **classifier** - Classifier selection
4. **classifier_adj** - Classifier with adjectives
5. **classifier_clause** - Classifier in clauses
6. **coverb_instrument** - Coverb instrument constructions
7. **coverb_with** - Coverb "with" constructions
8. **filler_gap_dependency** - Filler-gap dependencies
9. **head_final_clause** - Head-final clause structures
10. **passive_formal** - Formal passive constructions
11. **verb_complement_direction** - Directional verb complements
12. **verb_complement_duration** - Duration verb complements
13. **verb_complement_frequency** - Frequency verb complements
14. **verb_complement_res_adj** - Resultative adjective complements
15. **verb_complement_res_verb** - Resultative verb complements

**Note**: The `ba_construction` subset is skipped due to a broken CSV format in the source dataset.

## Usage

```bash
# Run CLiMP evaluation
lm_eval --model hf --model_args pretrained=MODEL_NAME --tasks climp --limit 100
```

## Example

**Grammatical**: 李思彤治疗过她自己 (Li Sitong treated herself)
**Ungrammatical**: 李思彤治疗过它自己 (Li Sitong treated itself)

The model should assign higher probability to the grammatical sentence.

## Metrics

- **Accuracy**: Proportion of pairs where the model assigns higher probability to the grammatical sentence.
