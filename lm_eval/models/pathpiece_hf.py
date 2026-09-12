"""
PathPiece model wrapper for lm-evaluation-harness (SOAR fork, patched).

Replaces lm_eval/models/pathpiece_hf.py in AntonioLopardo/lm-evaluation-harness @ 8eeb32d.
The original was never used in any historical run; running all 45 TIMTC models through it
surfaced three defects, all fixed here (verified 45/45 through the harness):

1. Per-family flags. The original defaulted greedy=True and had no random_tiebreaker at all,
   which is wrong for 9 of the 15 kept families. Flags are now inferred from the model name
   (explicit model_args still win):
       pathpiecer*                -> greedy=False, random_tiebreaker=True   (PathPieceR)
       pathpiecel*                -> greedy=False, random_tiebreaker=False  (PathPieceL)
       sage* / *greedy*           -> greedy=True,  random_tiebreaker=False
   and the three .json families (bpe_merge_3, unigram_likelihood_2, wordpiece_5) raise a
   pointed error telling you to use --model hf.
2. The parent HFLM.__init__ calls _create_tokenizer -> AutoTokenizer.from_pretrained. For the
   29 stand-in repos that silently loads bpe_merge_3's tokenizer and discards it (masking the
   bug); for the 7 `.notjson` repos there is nothing to load and it dies with
   "Unrecognized configuration class ... MPTConfig". Overriding _create_tokenizer installs the
   PathPiece wrapper directly, so no HF tokenizer is ever fetched.
3. The wrapper was incomplete: it had pad_token_id but no pad_token, so configure_pad_token()
   threw once the wrapper was actually used through the full init path. String-valued token
   attributes and the rest of the HF surface the harness touches are provided.

Vocabulary lookup: vocab_dir defaults to $TIMTC_VOCAB_DIR, then $CODE_DIR/timtc_vocabs_models/vocabularies.
PathPiece adds <|endoftext|> as id 0 on top of the N .vocab lines, so len(get_ids()) == N+1 == config.vocab_size.

Usage:
    lm_eval --model pathpiece_hf --model_args pretrained=luisfrentzen/pathpiecer_none_18_32768 --tasks blimp
    lm_eval --model pathpiece_hf --model_args pretrained=...,greedy=true,random_tiebreaker=false   # explicit override
"""

import importlib
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple, Union

import torch

import pathpiece
from lm_eval.api.registry import register_model
from lm_eval.models.huggingface import HFLM

_JSON_FAMILIES = ("bpe_merge_3", "unigram_likelihood_2", "wordpiece_5")
_EOS = "<|endoftext|>"
_EOS_ID = 0


def _default_vocab_dir() -> str:
    if os.environ.get("TIMTC_VOCAB_DIR"):
        return os.environ["TIMTC_VOCAB_DIR"]
    code_dir = os.environ.get("CODE_DIR", "/opt/soar")
    return f"{code_dir}/timtc_vocabs_models/vocabularies"


def infer_flags(model_name: str) -> Tuple[bool, bool]:
    """Return (greedy, random_tiebreaker) for a TIMTC model name. Raises for HF-tokenizer families."""
    n = Path(model_name).name.lower()
    if any(n.startswith(f) for f in _JSON_FAMILIES):
        raise ValueError(
            f"{model_name} is an HF-tokenizer family ({', '.join(_JSON_FAMILIES)}); "
            f"run it with --model hf, not pathpiece_hf."
        )
    if "pathpiecer" in n:
        return False, True
    if "pathpiecel" in n:
        return False, False
    if "sage" in n or "greedy" in n:
        return True, False
    raise ValueError(f"Cannot infer PathPiece flags for {model_name}; pass greedy= and random_tiebreaker= explicitly.")


def _as_bool(v, default: bool) -> bool:
    if v is None:
        return default
    if isinstance(v, bool):
        return v
    return str(v).strip().lower() in ("1", "true", "yes", "y", "t")


def _make_pathpiece(vocab_path: str, greedy: bool, random_tiebreaker: bool):
    """Construct pathpiece.Tokenizer across the two pyo3 signature variants seen in the wild."""
    try:
        return pathpiece.Tokenizer(vocab_path, special=_EOS, greedy=greedy, random_tiebreaker=random_tiebreaker)
    except TypeError:
        return pathpiece.Tokenizer(vocab_path, _EOS, greedy, random_tiebreaker)


class PathPieceWrapper:
    """Minimal HuggingFace-tokenizer-shaped interface over a pathpiece.Tokenizer."""

    def __init__(self, pp_tokenizer, vocab_size: int, name_or_path: str = "pathpiece"):
        self._tokenizer = pp_tokenizer
        self.vocab_size = vocab_size
        self.name_or_path = name_or_path
        # token ids
        self.eos_token_id = _EOS_ID
        self.pad_token_id = _EOS_ID
        self.bos_token_id = None
        self.unk_token_id = None
        # string-valued attributes: configure_pad_token() and friends read these
        self.eos_token = _EOS
        self.pad_token = _EOS
        self.bos_token = None
        self.unk_token = None
        self.padding_side = "left"
        self.model_max_length = int(1e9)
        self.chat_template = None
        self.special_tokens_map = {"eos_token": _EOS, "pad_token": _EOS}
        self.all_special_ids = [_EOS_ID]

    def __len__(self):
        return self.vocab_size

    def get_vocab(self):
        return {str(i): i for i in range(self.vocab_size)}

    def add_special_tokens(self, *args, **kwargs):
        return 0

    def apply_chat_template(self, *args, **kwargs):
        raise NotImplementedError("PathPiece TIMTC models have no chat template")

    def _ids(self, text: str) -> List[int]:
        return self._tokenizer.encode(text)["input_ids"]

    def __call__(self, text, return_tensors=None, **kwargs):
        if isinstance(text, str):
            input_ids = self._ids(text)
        else:
            input_ids = [self._ids(t) for t in text]
        if return_tensors == "pt":
            if input_ids and isinstance(input_ids[0], list):
                max_len = max(len(ids) for ids in input_ids)
                padded = [ids + [self.pad_token_id] * (max_len - len(ids)) for ids in input_ids]
                return {"input_ids": torch.tensor(padded)}
            return {"input_ids": torch.tensor([input_ids])}
        return {"input_ids": input_ids}

    def encode(self, text, add_special_tokens=True, **kwargs):
        return self._ids(text)

    def decode(self, token_ids, skip_special_tokens=True, **kwargs):
        if isinstance(token_ids, torch.Tensor):
            token_ids = token_ids.tolist()
        valid = [t for t in token_ids if t < self.vocab_size]
        return self._tokenizer.decode(valid) if valid else ""

    def batch_decode(self, batch_ids, skip_special_tokens=True, **kwargs):
        return [self.decode(ids, skip_special_tokens) for ids in batch_ids]

    def convert_tokens_to_ids(self, tokens):
        if tokens == _EOS:
            return _EOS_ID
        raise KeyError(tokens)


# Vendored Kensho/MosaicML MPT remote code (mpt_code/<vintage>/, one package per code vintage, repos.json maps the 45
# TIMTC repos onto them; SOAR_MPT_CODE_DIR overrides the location). The packages carry the six compatibility shims for
# transformers 4.57 (01-environment/README.md) so the hub cache is never modified and trust_remote_code is not needed
# for the model: weights and config come from the hub, the code from here.
_MPT_CODE_DIR = os.environ.get("SOAR_MPT_CODE_DIR") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "mpt_code")


def vendored_mpt_classes(pretrained: str):
    """(MPTConfig, MPTForCausalLM) from the vendored package for this repo, or None if the repo is not a TIMTC model."""
    repos_file = os.path.join(_MPT_CODE_DIR, "repos.json")
    if not os.path.exists(repos_file):
        return None
    repos = json.load(open(repos_file))
    vintage = repos.get(pretrained) or repos.get(f"luisfrentzen/{Path(pretrained).name}")
    if vintage is None:
        return None
    pkg = f"soar_mpt_{vintage}"
    if pkg not in sys.modules:
        root = os.path.join(_MPT_CODE_DIR, vintage)
        spec = importlib.util.spec_from_file_location(pkg, os.path.join(root, "__init__.py"), submodule_search_locations=[root])
        mod = importlib.util.module_from_spec(spec)
        sys.modules[pkg] = mod
        spec.loader.exec_module(mod)
    cfg = importlib.import_module(f"{pkg}.configuration_mpt")
    mdl = importlib.import_module(f"{pkg}.modeling_mpt")
    return cfg.MPTConfig, mdl.MPTForCausalLM


@register_model("mpt_hf")
class MPTNativeCacheHFLM(HFLM):
    """HFLM whose generate_until runs a greedy loop on the model's own list-of-tuples KV cache.

    The Kensho/MosaicML MPT remote code keeps keys as (b, h, d, s) and values as (b, h, s, d) and manages the cache
    itself. transformers >= 4.5x GenerationMixin wraps whatever the model returns in a DynamicCache, which measures and
    concatenates along the wrong axis: cached generate() is silently wrong on all 45 TIMTC repos and crashes on six
    (H-TMTC-13). Disabling the cache is exact but ~10x slower on the 265k generation requests of the English list.
    This class calls the model's forward directly, feeding its cache straight back, so the cache is used the way the
    code was written for. Decoding is greedy (argmax), per-sequence stop on eos or on a stop string in the decoded
    lookback window, as in lm_eval's stop_sequences_criteria; finished sequences are padded with pad_token_id, as
    generate() does. Use it for the .json families (--model mpt_hf); pathpiece_hf inherits it.
        native_cache=true   (default) greedy loop on the native cache
        native_cache=false  fall back to HFLM.generate (with generate_use_cache=false: uncached, exact, slow)
    """

    def __init__(self, pretrained: str, native_cache=True, generate_use_cache=True, vendored_mpt=True, **kwargs):
        self._native_cache = _as_bool(native_cache, True)
        self._generate_use_cache = _as_bool(generate_use_cache, True)
        # vendored_mpt=false loads the repo's own remote code from the hub cache (needs the patcher's shims there)
        self._vendored = vendored_mpt_classes(pretrained) if _as_bool(vendored_mpt, True) else None
        super().__init__(pretrained=pretrained, **kwargs)

    def _get_config(self, pretrained: str, *, revision: str = "main", trust_remote_code: bool = False, **kwargs) -> None:
        if self._vendored is None:
            return super()._get_config(pretrained, revision=revision, trust_remote_code=trust_remote_code, **kwargs)
        self._config = self._vendored[0].from_pretrained(pretrained, revision=revision)

    def _create_model(self, pretrained: str, revision: str | None = "main", dtype="auto", trust_remote_code: bool | None = False, **kwargs) -> None:
        if self._vendored is None:
            return super()._create_model(pretrained, revision=revision, dtype=dtype, trust_remote_code=trust_remote_code, **kwargs)
        from lm_eval.models.utils_hf import get_dtype
        self._model = self._vendored[1].from_pretrained(pretrained, revision=revision, dtype=get_dtype(dtype), config=self._config)
        if getattr(self._model, "generation_config", None) is None:  # the vendored class is not a GenerationMixin
            from transformers import GenerationConfig
            try:
                self._model.generation_config = GenerationConfig.from_pretrained(pretrained, revision=revision)
            except Exception:
                self._model.generation_config = GenerationConfig.from_model_config(self._config)

    def _model_generate(self, context, max_length, stop, **generation_kwargs):
        if self._native_cache:
            if generation_kwargs.get("do_sample"):
                raise NotImplementedError("native_cache generation is greedy only; pass native_cache=false to sample")
            return self._native_greedy(context, generation_kwargs.get("attention_mask"), max_length, stop)
        if not self._generate_use_cache and not getattr(self, "_nocache_wrapped", False):
            _orig = self.model.generate
            def _gen(*a, **k):
                k["use_cache"] = False
                return _orig(*a, **k)
            self.model.generate = _gen
            self._nocache_wrapped = True
        return super()._model_generate(context, max_length, stop, **generation_kwargs)

    def _stop_lookback(self, stop: List[str]) -> List[int]:
        # lm_eval.models.utils.MultiTokenEOSCriteria: window = len(tokenize(stop)) + 2 generated tokens
        return [len(self.tok_encode(s, add_special_tokens=False)) + 2 for s in stop]

    @torch.no_grad()
    def _native_greedy(self, context, attention_mask, max_length: int, stop: List[str]) -> torch.Tensor:
        model, dev = self.model, self.device
        input_ids = context.to(dev)
        attn = (attention_mask.to(dev) if attention_mask is not None else torch.ones_like(input_ids)).bool()
        b, ctx_len = input_ids.shape
        n_new = max_length - ctx_len
        eos = model.generation_config.eos_token_id
        eos = [] if eos is None else ([eos] if isinstance(eos, int) else list(eos))
        pad = self.tokenizer.pad_token_id
        if pad is None:
            pad = eos[0] if eos else 0
        lookback = self._stop_lookback(stop) if stop else []
        done = torch.zeros(b, dtype=torch.bool, device=dev)
        gen: List[torch.Tensor] = []
        capture = getattr(self, "_capture_logits", None)  # validate_native_cache.py: list to receive per-step logits
        with torch.autocast(device_type=dev.type, dtype=self.mixed_precision_dtype,
                            enabled=self.mixed_precision_dtype is not None):
            out = model(input_ids=input_ids, attention_mask=attn, use_cache=True, return_dict=True)
            past = out.past_key_values
            for step in range(n_new):
                if capture is not None:
                    capture.append(out.logits[:, -1, :].float().cpu())
                nxt = out.logits[:, -1, :].argmax(dim=-1)
                nxt = torch.where(done, torch.full_like(nxt, pad), nxt)
                gen.append(nxt)
                if eos:
                    done |= torch.isin(nxt, torch.tensor(eos, device=dev))
                if stop and not bool(done.all()):
                    g = torch.stack(gen, dim=1)
                    for i in (~done).nonzero(as_tuple=True)[0].tolist():
                        for s, lb in zip(stop, lookback):
                            if s in self.tok_decode(g[i, -lb:].tolist(), skip_special_tokens=False):
                                done[i] = True
                                break
                if bool(done.all()) or step == n_new - 1:
                    break
                attn = torch.cat([attn, torch.ones(b, 1, dtype=torch.bool, device=dev)], dim=1)
                out = model(input_ids=nxt[:, None], attention_mask=attn, past_key_values=past, use_cache=True,
                            return_dict=True)
                past = out.past_key_values
        return torch.cat([input_ids, torch.stack(gen, dim=1)], dim=1)


@register_model("pathpiece_hf")
class PathPieceHFLM(MPTNativeCacheHFLM):
    """HuggingFace LM with a native PathPiece tokenizer (TIMTC .vocab families)."""

    def __init__(
        self,
        pretrained: str,
        vocab_path: Optional[str] = None,
        greedy=None,
        random_tiebreaker=None,
        generate_use_cache=True,
        native_cache=True,
        vocab_dir: Optional[str] = None,
        **kwargs,
    ):
        model_name = Path(pretrained).name
        vocab_dir = vocab_dir or _default_vocab_dir()
        if vocab_path is None:
            vocab_path = f"{vocab_dir}/{model_name}.vocab"
        if not Path(vocab_path).exists():
            raise FileNotFoundError(
                f"Vocab file not found: {vocab_path} (set vocab_path= or TIMTC_VOCAB_DIR)"
            )

        inferred_g, inferred_r = infer_flags(model_name)
        self._greedy = _as_bool(greedy, inferred_g)
        self._random_tiebreaker = _as_bool(random_tiebreaker, inferred_r)
        self._pathpiece_tokenizer = _make_pathpiece(vocab_path, self._greedy, self._random_tiebreaker)
        self._vocab_size = len(self._pathpiece_tokenizer.get_ids())
        self._pp_wrapper = PathPieceWrapper(self._pathpiece_tokenizer, self._vocab_size, name_or_path=pretrained)

        # The parent must not fetch an HF tokenizer (stand-in or missing); _create_tokenizer is overridden.
        kwargs.pop("tokenizer", None)
        super().__init__(pretrained=pretrained, native_cache=native_cache, generate_use_cache=generate_use_cache, **kwargs)
        self.tokenizer = self._pp_wrapper

    # HFLM.__init__ calls this to populate self.tokenizer; install the PathPiece wrapper instead.
    def _create_tokenizer(self, *args, **kwargs):
        self.tokenizer = self._pp_wrapper
        return self.tokenizer

    def _encode_pair(self, context: str, continuation: str):
        """Encode context and continuation separately (H-TMTC-14). HFLM encodes the concatenation and cuts it at
        len(encode(context)); for the pathpiecer_none_18 vocabularies (no pre-tokenisation, so a token can straddle
        the context/continuation boundary) that cut mis-assigns tokens and the two-choice GLUE tasks degenerate
        (MRPC/QQP f1 = 0.000, glue 0.29 vs the published 0.47; separate encoding gives f1 0.821/0.522 and reproduces
        the paper). For every other family the boundary is a space and both encodings coincide. The trailing-space
        move is HFLM's."""
        n_spaces = len(context) - len(context.rstrip())
        if n_spaces > 0:
            context, continuation = context[:-n_spaces], context[-n_spaces:] + continuation
        return self.tok_encode(context), self.tok_encode(continuation)

    def tok_encode(self, string: str, left_truncate_len=None, add_special_tokens=None) -> List[int]:
        ids = self._pathpiece_tokenizer.encode(string)["input_ids"]
        if left_truncate_len is not None and len(ids) > left_truncate_len:
            ids = ids[-left_truncate_len:]
        return ids

    def tok_decode(self, tokens: Union[List[int], torch.Tensor], skip_special_tokens: bool = True) -> str:
        if isinstance(tokens, torch.Tensor):
            tokens = tokens.tolist()
        if isinstance(tokens, int):  # the harness passes a bare eot_token_id in generate_until
            tokens = [tokens]
        if hasattr(tokens, "tolist"):
            tokens = tokens.tolist()
        valid = [t for t in tokens if t < self._vocab_size]
        return self._pathpiece_tokenizer.decode(valid) if valid else ""

    def tok_batch_encode(
        self,
        strings: List[str],
        padding_side: str = "left",
        left_truncate_len: int = None,
        truncation: bool = False,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        batch = [self.tok_encode(s, left_truncate_len=left_truncate_len) for s in strings]
        max_len = max(len(ids) for ids in batch)
        pad = self._pp_wrapper.pad_token_id
        if padding_side == "left":
            padded = [[pad] * (max_len - len(ids)) + ids for ids in batch]
            masks = [[0] * (max_len - len(ids)) + [1] * len(ids) for ids in batch]
        else:
            padded = [ids + [pad] * (max_len - len(ids)) for ids in batch]
            masks = [[1] * len(ids) + [0] * (max_len - len(ids)) for ids in batch]
        return torch.tensor(padded), torch.tensor(masks)

    @property
    def eot_token_id(self) -> int:
        return _EOS_ID

    @property
    def max_length(self) -> int:
        if hasattr(self._model.config, "max_seq_len"):
            return self._model.config.max_seq_len
        return 2048


def needs_pathpiece(model_name: str, vocab_dir: Optional[str] = None) -> bool:
    vocab_dir = vocab_dir or _default_vocab_dir()
    return (Path(vocab_dir) / f"{Path(model_name).name}.vocab").exists()


def get_tokenizer_type(model_name: str, vocab_dir: Optional[str] = None) -> str:
    vocab_dir = vocab_dir or _default_vocab_dir()
    name = Path(model_name).name
    if (Path(vocab_dir) / f"{name}.json").exists():
        return "huggingface"
    if (Path(vocab_dir) / f"{name}.vocab").exists():
        g, r = infer_flags(name)
        return "pathpiece_greedy" if g else ("pathpiece_R" if r else "pathpiece_L")
    return "unknown"
