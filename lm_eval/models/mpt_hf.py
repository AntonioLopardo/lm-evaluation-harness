"""mpt_hf — the TIMTC checkpoints (Kensho's MPT models) loaded through their own modeling code, with generation on
the model's own KV cache.

The 45 repositories ship their modeling code, which does not run under transformers 4.57 (two dead imports) and
whose list-of-tuples KV cache the modern generate() wraps in a DynamicCache and concatenates along the wrong axis,
so cached decoding is silently wrong. This class loads weights and config from the hub but the code from timtc_mpt
(the reproduction repository: the checkpoints' own code with the fixes marked TMMC-COMPAT-*), so
nothing in the hub cache is executed or modified and trust_remote_code is not needed; and it generates with a greedy
loop that calls the model's forward directly, feeding its cache straight back. Decoding is greedy, per-sequence stop
on eos or on a stop string in the decoded lookback window (as lm_eval's stop criteria), finished sequences padded
with pad_token_id, as generate() does.

    lm_eval --model mpt_hf --model_args pretrained=luisfrentzen/bpe_merge_3_32768 --tasks blimp
        native_cache=true       (default) the greedy loop on the native cache
        native_cache=false      HFLM.generate(); with generate_use_cache=false uncached, exact and about 10x slower.
                                Needs vendored_mpt=false: the timtc_mpt classes have no generate() under
                                transformers 4.57 (the repositories' own code, run as remote code, still has one)
        vendored_mpt=true       (default) the code from timtc_mpt; false runs the repository's own remote code

The three schemes with an HF tokenizer (bpe_merge_3, unigram_likelihood_2, wordpiece_5) run through this class;
their tokenizer.json pre-tokenises with ByteLevel but ships no decoder, which the class installs. The PathPiece
schemes run through pathpiece_hf, which inherits this class.
"""

from typing import List

import torch

from lm_eval.api.registry import register_model
from lm_eval.models.huggingface import HFLM

try:
    from timtc_mpt import mpt_classes
except ImportError:  # without the package there is nothing to load; the repository's own code is used

    def mpt_classes(pretrained: str):
        return None


def as_bool(value, default: bool) -> bool:
    """A model_args value as a bool: absent gives the default; strings read as true/false."""
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("1", "true", "yes", "y", "t")


def fix_missing_decoder(tokenizer):
    """Install the decoder a ByteLevel tokenizer ships without, so decode() gives text and not the byte-level
    alphabet: ByteLevel, after stripping WordPiece's continuing prefix where there is one."""
    backend = getattr(tokenizer, "backend_tokenizer", None)
    if backend is None or backend.decoder is not None or type(backend.pre_tokenizer).__name__ != "ByteLevel":
        return
    from tokenizers import decoders

    prefix = getattr(backend.model, "continuing_subword_prefix", None)
    if prefix:
        backend.decoder = decoders.Sequence([decoders.WordPiece(prefix=prefix, cleanup=False), decoders.ByteLevel()])
    else:
        backend.decoder = decoders.ByteLevel()


@register_model("mpt_hf")
class MPTNativeCacheHFLM(HFLM):
    """HFLM for the TIMTC checkpoints: the code from timtc_mpt, generation on the model's own KV cache."""

    def __init__(self, pretrained: str, native_cache=True, generate_use_cache=True, vendored_mpt=True, **kwargs):
        self._native_cache = as_bool(native_cache, True)
        self._generate_use_cache = as_bool(generate_use_cache, True)
        self._vendored = mpt_classes(pretrained) if as_bool(vendored_mpt, True) else None
        super().__init__(pretrained=pretrained, **kwargs)

    def _create_tokenizer(self, *args, **kwargs):
        super()._create_tokenizer(*args, **kwargs)
        fix_missing_decoder(self.tokenizer)

    def _get_config(self, pretrained: str, *, revision: str = "main", trust_remote_code: bool = False, **kwargs) -> None:
        if self._vendored is None:
            return super()._get_config(pretrained, revision=revision, trust_remote_code=trust_remote_code, **kwargs)
        config_class, _ = self._vendored
        self._config = config_class.from_pretrained(pretrained, revision=revision)

    def _create_model(
        self, pretrained: str, revision: str | None = "main", dtype="auto", trust_remote_code: bool | None = False, **kwargs
    ) -> None:
        if self._vendored is None:
            return super()._create_model(
                pretrained, revision=revision, dtype=dtype, trust_remote_code=trust_remote_code, **kwargs
            )
        from lm_eval.models.utils_hf import get_dtype

        _, model_class = self._vendored
        self._model = model_class.from_pretrained(pretrained, revision=revision, dtype=get_dtype(dtype), config=self._config)
        if getattr(self._model, "generation_config", None) is None:  # the class is not a GenerationMixin
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
            original_generate = self.model.generate

            def generate_without_cache(*args, **kwargs):
                kwargs["use_cache"] = False
                return original_generate(*args, **kwargs)

            self.model.generate = generate_without_cache
            self._nocache_wrapped = True
        return super()._model_generate(context, max_length, stop, **generation_kwargs)

    def _stop_lookback(self, stop: List[str]) -> List[int]:
        """How many generated tokens to decode when looking for each stop string: lm_eval's window, the stop's
        token count plus two."""
        return [len(self.tok_encode(s, add_special_tokens=False)) + 2 for s in stop]

    def _eos_ids(self) -> List[int]:
        eos = self.model.generation_config.eos_token_id
        if eos is None:
            return []
        return [eos] if isinstance(eos, int) else list(eos)

    def _hit_stop_string(self, generated: torch.Tensor, stop: List[str], lookback: List[int]) -> bool:
        """Whether one of the stop strings appears in the decoded tail of one sequence's generated tokens."""
        for s, window in zip(stop, lookback):
            if s in self.tok_decode(generated[-window:].tolist(), skip_special_tokens=False):
                return True
        return False

    @torch.no_grad()
    def _native_greedy(self, context, attention_mask, max_length: int, stop: List[str]) -> torch.Tensor:
        """Greedy decoding through the model's forward and its own cache: `context` (b, n) left-padded, returns the
        context with up to max_length - n generated tokens appended. `self._capture_logits`, when a list is set on
        the instance, receives every step's next-token logits (the validation script reads them)."""
        model, dev = self.model, self.device
        input_ids = context.to(dev)
        attn = (attention_mask.to(dev) if attention_mask is not None else torch.ones_like(input_ids)).bool()
        batch, context_len = input_ids.shape
        eos = self._eos_ids()
        pad = self.tokenizer.pad_token_id
        if pad is None:
            pad = eos[0] if eos else 0
        lookback = self._stop_lookback(stop) if stop else []
        done = torch.zeros(batch, dtype=torch.bool, device=dev)
        generated: List[torch.Tensor] = []
        capture = getattr(self, "_capture_logits", None)
        autocast = torch.autocast(
            device_type=dev.type, dtype=self.mixed_precision_dtype, enabled=self.mixed_precision_dtype is not None
        )
        with autocast:
            out = model(input_ids=input_ids, attention_mask=attn, use_cache=True, return_dict=True)
            past = out.past_key_values
            for step in range(max_length - context_len):
                if capture is not None:
                    capture.append(out.logits[:, -1, :].float().cpu())
                next_ids = out.logits[:, -1, :].argmax(dim=-1)
                next_ids = torch.where(done, torch.full_like(next_ids, pad), next_ids)
                generated.append(next_ids)
                if eos:
                    done |= torch.isin(next_ids, torch.tensor(eos, device=dev))
                if stop and not bool(done.all()):
                    stacked = torch.stack(generated, dim=1)
                    for i in (~done).nonzero(as_tuple=True)[0].tolist():
                        if self._hit_stop_string(stacked[i], stop, lookback):
                            done[i] = True
                if bool(done.all()) or step == max_length - context_len - 1:
                    break
                attn = torch.cat([attn, torch.ones(batch, 1, dtype=torch.bool, device=dev)], dim=1)
                out = model(
                    input_ids=next_ids[:, None], attention_mask=attn, past_key_values=past, use_cache=True, return_dict=True
                )
                past = out.past_key_values
        return torch.cat([input_ids, torch.stack(generated, dim=1)], dim=1)
