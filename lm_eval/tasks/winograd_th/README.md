# Thai Winograd Schema

## Overview

Thai Winograd Schema is a coreference resolution benchmark for Thai language, based on the classic Winograd Schema Challenge. The task tests a model's ability to resolve pronouns to their correct referents using world knowledge and commonsense reasoning.

## Dataset

- **Source:** [pakphum/winograd_th](https://huggingface.co/datasets/pakphum/winograd_th)
- **Size:** 285 test examples
- **Format:** Multiple choice (binary)

## Task Format

Given a sentence containing a pronoun (e.g., "พวกเขา" - "they"), the model must determine which of two candidate noun phrases the pronoun refers to.

### Example

**Sentence:** สมาชิกสภาเทศบาลเมืองปฏิเสธใบอนุญาตผู้ชุมนุมเพราะพวกเขากลัวความรุนแรง

**Pronoun:** พวกเขา (they)

**Options:**
- A: สมาชิกสภาเทศบาลเมือง (city council members)
- B: ผู้ชุมนุม (protesters)

**Answer:** A (The council members feared violence)

## Metrics

- **Accuracy:** Percentage of correctly resolved coreferences

## Usage

```bash
lm_eval --model hf \
    --model_args pretrained=MODEL_NAME \
    --tasks winograd_th \
    --batch_size 8
```

## References

- Original Winograd Schema: Winograd, T. (1972). Understanding natural language.
- Thai adaptation: [pakphum/winograd_th](https://huggingface.co/datasets/pakphum/winograd_th)
