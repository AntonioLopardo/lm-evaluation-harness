# IndicGLUE

### Paper

IndicGLUE: A Natural Language Understanding Benchmark for Indian Languages
- Paper: https://aclanthology.org/2020.findings-emnlp.445/
- Repository: https://github.com/AI4Bharat/IndicGLUE

IndicGLUE is a benchmark for evaluating natural language understanding for Indian languages, containing multiple tasks from AI4Bharat.

### Tasks

#### WNLI (Winograd NLI)
- Languages: Hindi (hi), Gujarati (gu), Marathi (mr)
- Task type: Natural Language Inference (binary)
- Metrics: Accuracy

#### COPA (Choice of Plausible Alternatives)
- Languages: Hindi (hi), Gujarati (gu), Marathi (mr)
- Task type: Commonsense Reasoning
- Metrics: Accuracy

### Groups

| Group | Tasks |
|-------|-------|
| `indicglue` | All IndicGLUE tasks |
| `indicglue_wnli` | WNLI tasks (hi, gu, mr) |
| `indicglue_copa` | COPA tasks (hi, gu, mr) |

### Usage

```bash
# Run all IndicGLUE tasks
lm_eval --tasks indicglue --model hf --model_args pretrained=ai4bharat/indic-bert

# Run specific task
lm_eval --tasks indicglue_wnli_hi --model hf --model_args pretrained=ai4bharat/indic-bert

# Run COPA group
lm_eval --tasks indicglue_copa --model hf --model_args pretrained=ai4bharat/indic-bert
```

### Dataset

- HuggingFace: https://huggingface.co/datasets/ai4bharat/indic_glue

### Citation

```bibtex
@inproceedings{kakwani-etal-2020-indicnlpsuite,
    title = "{I}ndic{NLPS}uite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for {I}ndian Languages",
    author = "Kakwani, Divyanshu  and
      Kunchukuttan, Anoop  and
      Golla, Satish  and
      Gokul, N.C.  and
      Bhattacharyya, Avik  and
      Khapra, Mitesh M.  and
      Kumar, Pratyush",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2020",
    year = "2020",
    publisher = "Association for Computational Linguistics",
    pages = "4948--4961",
}
```
