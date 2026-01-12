# EWoK: Elements of World Knowledge

## Overview

EWoK (Elements of World Knowledge) is a benchmark for evaluating commonsense reasoning about the physical and social world.

## Paper

- **Title**: EWoK: A Benchmark for Elements of World Knowledge
- **Link**: https://arxiv.org/abs/2405.09605

## Dataset

- **Source**: https://huggingface.co/datasets/ewok-core/ewok-core-1.0
- **Language**: English
- **Task Type**: Multiple-choice (forced choice)
- **Split**: test (4,374 examples → 8,748 evaluation instances)

## Domains

EWoK covers 11 knowledge domains:

1. **agent-properties** - Mental states and agent capabilities
2. **material-dynamics** - How materials change and behave
3. **material-properties** - Physical properties of materials
4. **physical-dynamics** - Motion and physical processes
5. **physical-interactions** - Object interactions
6. **physical-relations** - Physical relationships between objects
7. **quantitative-properties** - Numerical and quantity reasoning
8. **social-interactions** - Human social behaviors
9. **social-properties** - Social characteristics
10. **social-relations** - Relationships between people
11. **spatial-relations** - Spatial reasoning

## Task Format

Each original example contains a minimal contrast pair:
- Context1 + Target1 (correct pairing)
- Context2 + Target2 (correct pairing)

We evaluate both pairings separately, testing whether the model assigns higher probability to the correct continuation.

## Example

**Context1**: Ali is in the bakery. Ali sees the candle inside.
**Target1**: Ali believes that the candle is in the bakery. ✓
**Target2**: Ali doubts that the candle is in the bakery. ✗

**Context2**: Ali is in the bakery. Ali sees the candle outside.
**Target1**: Ali believes that the candle is in the bakery. ✗
**Target2**: Ali doubts that the candle is in the bakery. ✓

## Usage

```bash
# Run EWoK evaluation
lm_eval --model hf --model_args pretrained=gpt2 --tasks ewok --limit 100
```

## Metrics

- **Accuracy**: Proportion of examples where the model assigns higher probability to the correct target continuation.
