#!/usr/bin/env python3
"""validate_native_cache.py — checks of the native-cache generation loop of mpt_hf / pathpiece_hf, on one repository
of each version of the modeling code by default, on batched left-padded prompts of mixed length.

  tokens   the loop's output against the uncached transformers generate() path, with and without stop strings:
           the two must be equal token for token (bf16, the run's dtype)
  logits   the loop's per-step next-token logits against one plain full forward over the produced sequence, in
           bf16 and fp32: a correct cache shows about 1e-3 (bf16) and 1e-5 (fp32) differences and full argmax
           agreement in fp32; token disagreements between cached and uncached decoding in bf16 near ties are expected

  validate_native_cache.py <cuda:N> [tokens|logits|all] [repo ...]"""

import sys
import time
from typing import List, Tuple

import torch

from lm_eval.api.registry import get_model

DEFAULT_REPOS = ["bpe_merge_3_32768", "unigram_greedy_7_32768", "pathpiecer_none_18_32768", "wordpiece_5_40960"]
PROMPTS = [
    "The capital of France is",
    "Question: How many letters are in the word 'strawberry'?\nAnswer:",
    'Spell the word "banana" with hyphens between letters: b-a-n-a-n-a. Spell the word "reproduction" with hyphens between letters:',
    "Once upon a time, in a village by the sea, there lived a fisherman who",
    "Q: Not ( ( not not True ) ) is\nA: Let's think step by step.",
    "1, 2, 3, 4, 5,",
    'def fibonacci(n):\n    """Return the n-th Fibonacci number."""\n',
    "In this task you are given a sentence and must count the number of unique characters.\nSentence: the quick brown fox jumps over the lazy dog\nCount:",
]
# (stop strings, tokens to generate) of the token check
TOKEN_CASES: List[Tuple[List[str], int]] = [(["\n"], 24), ([], 48), ([".", "\n", ","], 12)]
LOGIT_STEPS = 32


def model_class(repo: str) -> str:
    return "pathpiece_hf" if any(k in repo for k in ("pathpiece", "sage", "unigram_greedy")) else "mpt_hf"


def load(repo: str, device: str, dtype: str = "auto"):
    args = dict(pretrained=f"luisfrentzen/{repo}", trust_remote_code=True, device=device, batch_size=8, dtype=dtype)
    if repo.startswith("pathpiecer"):
        args["random_tiebreaker"] = False  # deterministic, so the two paths can be compared
    return get_model(model_class(repo))(**args)


def encode_prompts(model):
    context, mask = model.tok_batch_encode(PROMPTS, padding_side="left")
    return context.to(model.device), mask.to(model.device)


def timed_generate(model, context, mask, n_new: int, stop: List[str]) -> Tuple[torch.Tensor, float]:
    torch.cuda.synchronize()
    start = time.time()
    out = model._model_generate(context.clone(), context.shape[1] + n_new, stop, attention_mask=mask.clone())
    torch.cuda.synchronize()
    return out[:, context.shape[1] :].cpu(), time.time() - start


def check_tokens(repo: str, device: str) -> bool:
    """The native loop against uncached generate(), token for token; prints each case and the speed-up."""
    model = load(repo, device)
    context, mask = encode_prompts(model)
    all_equal = True
    for stop, n_new in TOKEN_CASES:
        model._native_cache = True
        native, t_native = timed_generate(model, context, mask, n_new, stop)
        model._native_cache = False
        model._generate_use_cache = False
        uncached, t_uncached = timed_generate(model, context, mask, n_new, stop)
        length = min(native.shape[1], uncached.shape[1])
        equal = native.shape == uncached.shape and torch.equal(native[:, :length], uncached[:, :length])
        all_equal &= equal
        print(
            f"{repo:42s} {model_class(repo):12s} stop={stop!r:20s} max_new={n_new:3d}  equal={equal}  "
            f"native {t_native:5.1f}s  uncached {t_uncached:5.1f}s  x{t_uncached / max(t_native, 1e-6):.1f}",
            flush=True,
        )
        if not equal:
            for i in range(native.shape[0]):
                if not torch.equal(native[i, :length], uncached[i, :length]):
                    print("   row", i, "native  :", repr(model.tok_decode(native[i].tolist())[:80]))
                    print("   row", i, "uncached:", repr(model.tok_decode(uncached[i].tolist())[:80]))
    del model
    torch.cuda.empty_cache()
    return all_equal


def check_logits(repo: str, device: str) -> None:
    """The loop's per-step logits against a plain full forward over its own output, in bf16 and fp32."""
    for dtype in ("bfloat16", "float32"):
        model = load(repo, device, dtype)
        context, mask = encode_prompts(model)
        model._capture_logits = []
        out = model._model_generate(context.clone(), context.shape[1] + LOGIT_STEPS, [], attention_mask=mask.clone())
        captured = torch.stack(model._capture_logits, dim=1)  # (batch, steps, vocab)
        steps = captured.shape[1]
        n_generated = out.shape[1] - context.shape[1]
        full_mask = torch.cat([mask, torch.ones(out.shape[0], n_generated, dtype=mask.dtype, device=mask.device)], 1)
        with torch.no_grad():
            reference = model.model(input_ids=out, attention_mask=full_mask.bool(), use_cache=False, return_dict=True)
        first = context.shape[1] - 1
        reference = reference.logits[:, first : first + steps, :].float().cpu()
        diff = (captured - reference).abs()
        agree = captured.argmax(-1) == reference.argmax(-1)
        valid = steps_before_eos(out[:, context.shape[1] :].cpu(), model._eos_ids(), steps)
        margins = [round(float(torch.topk(reference[i, j], 2).values.diff().abs()), 4) for i, j in (~agree & valid).nonzero().tolist()]
        print(
            f"{repo:42s} {model_class(repo):12s} {dtype:9s} steps={steps:3d} max|dlogit|={diff[valid].max():.2e} "
            f"mean={diff[valid].mean():.2e} argmax agree {int(agree[valid].sum())}/{int(valid.sum())}  "
            f"reference top-2 margin at the disagreements={margins[:6]}",
            flush=True,
        )
        del model
        torch.cuda.empty_cache()


def steps_before_eos(generated: torch.Tensor, eos: List[int], steps: int) -> torch.Tensor:
    """(batch, steps) mask of the steps up to and including each row's first eos; later steps are padding."""
    valid = torch.ones(generated.shape[0], steps, dtype=torch.bool)
    for i in range(generated.shape[0]):
        hits = [j for j in range(min(steps, generated.shape[1])) if generated[i, j].item() in eos]
        if hits:
            valid[i, hits[0] + 1 :] = False
    return valid


def main() -> None:
    device = sys.argv[1]
    which = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] in ("tokens", "logits", "all") else "all"
    repos = [a for a in sys.argv[2:] if a not in ("tokens", "logits", "all")] or DEFAULT_REPOS
    all_equal = True
    for repo in repos:
        if which in ("tokens", "all"):
            all_equal &= check_tokens(repo, device)
        if which in ("logits", "all"):
            check_logits(repo, device)
    if which in ("tokens", "all"):
        print("ALL EQUAL" if all_equal else "MISMATCH")


if __name__ == "__main__":
    main()
