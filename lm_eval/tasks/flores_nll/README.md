# FLORES NLL (Negative Log Likelihood)

## Description

Computes mean negative log likelihood (perplexity) on FLORES-200 sentences for multilingual language modeling evaluation.

Based on the evaluation methodology from the Goldfish paper (Appendix A3).

## Dataset

- **Source:** [Muennighoff/flores200](https://huggingface.co/datasets/Muennighoff/flores200)
- **Paper:** [Goldfish: Monolingual Language Models for Hundreds of Languages](https://arxiv.org/abs/2408.10441)
- **Reference Implementation:** [tylerachang/goldfish](https://github.com/tylerachang/goldfish/blob/main/eval_code/flores_eval_othermodels.py)

## Target Languages

| Task Name | Language | Script | FLORES Code |
|-----------|----------|--------|-------------|
| `flores_nll_eng` | English | Latin | eng_Latn |
| `flores_nll_tha` | Thai | Thai | tha_Thai |
| `flores_nll_vie` | Vietnamese | Latin | vie_Latn |
| `flores_nll_amh` | Amharic | Ethiopic | amh_Ethi |
| `flores_nll_urd` | Urdu | Arabic | urd_Arab |

## Metrics

- **mean_nll:** Mean negative log likelihood per sentence
- **word_perplexity:** Perplexity normalized by word count
- **byte_perplexity:** Perplexity normalized by byte count
- **bits_per_byte:** Bits per byte (compression metric)

## Usage

```bash
# Run all 5 target languages
lm_eval --model hf --model_args pretrained=MODEL --tasks flores_nll --batch_size 8

# Run individual language
lm_eval --model hf --model_args pretrained=MODEL --tasks flores_nll_eng --batch_size 8
lm_eval --model hf --model_args pretrained=MODEL --tasks flores_nll_amh --batch_size 8
```

## Dataset Details

- **Split used:** devtest (1,012 sentences per language)
- **Task type:** loglikelihood_rolling (perplexity evaluation)

## Citation

```bibtex
@article{chang2024goldfish,
  title={Goldfish: Monolingual Language Models for Hundreds of Languages},
  author={Chang, Tyler A and Arnett, Catherine and Yao, Zhuowen and Balis, Mahir and Neubig, Graham},
  journal={arXiv preprint arXiv:2408.10441},
  year={2024}
}

@article{nllb2022,
  title={No Language Left Behind: Scaling Human-Centered Machine Translation},
  author={NLLB Team},
  year={2022}
}
```
