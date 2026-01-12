# BLiMP-FR (French Benchmark of Linguistic Minimal Pairs)

### Paper

BLiMP-FR: A French adaptation of BLiMP for grammaticality judgment
- Original BLiMP Paper: https://aclanthology.org/2020.tacl-1.25/

BLiMP-FR tests French grammaticality using minimal pairs - sentences that differ minimally with one being grammatical and one ungrammatical.

### Tasks

Each phenomenon is evaluated separately:

| Task | Phenomenon | Size |
|------|------------|------|
| `blimp_fr_anaphor_agreement` | Anaphor Agreement | 1,000 |
| `blimp_fr_adjective_noun_agreement` | Adjective-Noun Agreement | 1,000 |
| `blimp_fr_determiner_noun_agreement` | Determiner-Noun Agreement | 1,000 |
| `blimp_fr_binding` | Binding | 1,000 |
| `blimp_fr_clitic_placement` | Clitic Placement | 1,000 |
| `blimp_fr_auxiliary_agreement` | Auxiliary Agreement | 1,000 |
| `blimp_fr_negation` | Negation | 1,000 |
| `blimp_fr_subjunctive` | Subjunctive | 1,000 |

### Groups

| Group | Tasks |
|-------|-------|
| `blimp_fr` | All BLiMP-FR tasks |

### Usage

```bash
# Run all BLiMP-FR tasks
lm_eval --tasks blimp_fr --model hf --model_args pretrained=flaubert/flaubert_base_cased

# Run specific phenomenon
lm_eval --tasks blimp_fr_anaphor_agreement --model hf --model_args pretrained=flaubert/flaubert_base_cased
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/elliepreed/BLiMP-fr

### Citation

```bibtex
@article{warstadt2020blimp,
    title={BLiMP: The benchmark of linguistic minimal pairs for English},
    author={Warstadt, Alex and Parrish, Alicia and Liu, Haokun and Mohananey, Anhad and Peng, Wei and Wang, Sheng-Fu and Bowman, Samuel R},
    journal={Transactions of the Association for Computational Linguistics},
    volume={8},
    pages={377--392},
    year={2020}
}
```
