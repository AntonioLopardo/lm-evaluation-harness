#!/usr/bin/env python3
"""validate_native_cache2.py — is the native-cache loop *numerically* right? For each repo and dtype, run the loop
capturing the per-step next-token logits, then teacher-force the produced sequence through one plain full forward
(no cache, the reference the uncached generate() path also computes) and compare the logits at the same positions:
max |diff|, and how many steps' argmax agree. Token-level disagreement between cached and uncached decoding in bf16
is expected near ties; a correct cache shows ~1e-3 (bf16) / ~1e-5 (fp32) logit differences and full argmax agreement
in fp32.    usage: validate_native_cache2.py <cuda:N> [repo ...]"""
import sys, torch
from lm_eval.api.registry import get_model
dev = sys.argv[1]
repos = sys.argv[2:] or ["bpe_merge_3_32768", "unigram_greedy_7_32768", "pathpiecer_none_18_32768", "wordpiece_5_40960"]
PROMPTS = ["The capital of France is", "Question: How many letters are in the word 'strawberry'?\nAnswer:",
    "Spell the word \"banana\" with hyphens between letters: b-a-n-a-n-a. Spell the word \"reproduction\" with hyphens between letters:",
    "Once upon a time, in a village by the sea, there lived a fisherman who", "Q: Not ( ( not not True ) ) is\nA: Let's think step by step.",
    "1, 2, 3, 4, 5,", "def fibonacci(n):\n    \"\"\"Return the n-th Fibonacci number.\"\"\"\n",
    "In this task you are given a sentence and must count the number of unique characters.\nSentence: the quick brown fox jumps over the lazy dog\nCount:"]
N_NEW = 32
for repo in repos:
    cls = "pathpiece_hf" if any(k in repo for k in ("pathpiece", "sage", "unigram_greedy")) else "mpt_hf"
    for dtype in ("bfloat16", "float32"):
        args = dict(pretrained=f"luisfrentzen/{repo}", trust_remote_code=True, device=dev, batch_size=8, dtype=dtype)
        if repo.startswith("pathpiecer"): args["random_tiebreaker"] = False
        m = get_model(cls)(**args)
        ctx, mask = m.tok_batch_encode(PROMPTS, padding_side="left"); ctx, mask = ctx.to(m.device), mask.to(m.device)
        m._capture_logits = []
        out = m._model_generate(ctx.clone(), ctx.shape[1] + N_NEW, [], attention_mask=mask.clone())
        cap = torch.stack(m._capture_logits, dim=1)                      # (b, steps, V)
        steps = cap.shape[1]
        full_mask = torch.cat([mask, torch.ones(out.shape[0], out.shape[1] - ctx.shape[1], dtype=mask.dtype, device=mask.device)], 1)
        with torch.no_grad():
            ref = m.model(input_ids=out, attention_mask=full_mask.bool(), use_cache=False, return_dict=True).logits
        ref = ref[:, ctx.shape[1] - 1: ctx.shape[1] - 1 + steps, :].float().cpu()
        diff = (cap - ref).abs()
        agree = (cap.argmax(-1) == ref.argmax(-1))
        # steps after a sequence finished (eos) are padded and irrelevant; count agreement up to the first eos per row
        eos = m.model.generation_config.eos_token_id; eos = [] if eos is None else ([eos] if isinstance(eos, int) else list(eos))
        gen = out[:, ctx.shape[1]:].cpu()
        valid = torch.ones_like(agree)
        for i in range(gen.shape[0]):
            hits = [j for j in range(min(steps, gen.shape[1])) if gen[i, j].item() in eos]
            if hits: valid[i, hits[0] + 1:] = False
        print(f"{repo:42s} {cls:12s} {dtype:9s} steps={steps:3d} max|dlogit|={diff[valid].max():.2e} mean={diff[valid].mean():.2e} "
              f"argmax agree {int(agree[valid].sum())}/{int(valid.sum())}  ref-top-margin@disagree="
              f"{[round(float(torch.topk(ref[i,j],2).values.diff().abs()),4) for i,j in (~agree & valid).nonzero().tolist()][:6]}", flush=True)
        del m; torch.cuda.empty_cache()
