#!/usr/bin/env python3
"""validate_native_cache.py — token-exact check of MPTNativeCacheHFLM._native_greedy (mpt_hf / pathpiece_hf,
native_cache=true) against the uncached transformers generate() path (native_cache=false, generate_use_cache=false)
on batched, left-padded prompts of mixed length, with and without stop strings, for one repo of each modeling-code
vintage. Prints per-case agreement and timings.   usage: validate_native_cache.py <cuda:N> [repo ...]"""
import sys, time, torch
from lm_eval.api.registry import get_model
dev = sys.argv[1]
repos = sys.argv[2:] or ["bpe_merge_3_32768", "unigram_greedy_7_32768", "pathpiecer_none_18_32768", "wordpiece_5_40960"]
PROMPTS = [
    "The capital of France is",
    "Question: How many letters are in the word 'strawberry'?\nAnswer:",
    "Spell the word \"banana\" with hyphens between letters: b-a-n-a-n-a. Spell the word \"reproduction\" with hyphens between letters:",
    "Once upon a time, in a village by the sea, there lived a fisherman who",
    "Q: Not ( ( not not True ) ) is\nA: Let's think step by step.",
    "1, 2, 3, 4, 5,",
    "def fibonacci(n):\n    \"\"\"Return the n-th Fibonacci number.\"\"\"\n",
    "In this task you are given a sentence and must count the number of unique characters.\nSentence: the quick brown fox jumps over the lazy dog\nCount:",
]
CASES = [(["\n"], 24), ([], 48), ([".", "\n", ","], 12)]
ok_all = True
for repo in repos:
    cls = "pathpiece_hf" if "pathpiece" in repo or "sage" in repo or "unigram_greedy" in repo else "mpt_hf"
    args = dict(pretrained=f"luisfrentzen/{repo}", trust_remote_code=True, device=dev, batch_size=8)
    if cls == "pathpiece_hf" and repo.startswith("pathpiecer"):
        args["random_tiebreaker"] = False
    m = get_model(cls)(**args)
    ctx, mask = m.tok_batch_encode(PROMPTS, padding_side="left"); ctx, mask = ctx.to(m.device), mask.to(m.device)
    for stop, n_new in CASES:
        m._native_cache = True
        torch.cuda.synchronize(); t0 = time.time()
        a = m._model_generate(ctx.clone(), ctx.shape[1] + n_new, stop, attention_mask=mask.clone())
        torch.cuda.synchronize(); ta = time.time() - t0
        m._native_cache = False; m._generate_use_cache = False
        t0 = time.time()
        b = m._model_generate(ctx.clone(), ctx.shape[1] + n_new, stop, attention_mask=mask.clone())
        torch.cuda.synchronize(); tb = time.time() - t0
        a, b = a[:, ctx.shape[1]:].cpu(), b[:, ctx.shape[1]:].cpu()
        L = min(a.shape[1], b.shape[1])
        same = torch.equal(a[:, :L], b[:, :L]) and a.shape == b.shape
        ok_all &= same
        print(f"{repo:45s} {cls:12s} stop={stop!r:20s} max_new={n_new:3d}  equal={same}  native {ta:5.1f}s  uncached {tb:5.1f}s  x{tb/max(ta,1e-6):.1f}", flush=True)
        if not same:
            for i in range(a.shape[0]):
                if not torch.equal(a[i, :L], b[i, :L]):
                    print("   row", i, "native  :", repr(m.tok_decode(a[i].tolist())[:80]))
                    print("   row", i, "uncached:", repr(m.tok_decode(b[i].tolist())[:80]))
    del m; torch.cuda.empty_cache()
print("ALL EQUAL" if ok_all else "MISMATCH")
