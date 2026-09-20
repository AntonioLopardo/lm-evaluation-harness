"""pathpiece_hf — the TIMTC checkpoints whose tokenizer is a native PathPiece vocabulary (the 12 PathPiece-based
schemes: pathpiecel_*, pathpiecer_*, sage_*, unigram_greedy_7, unigram_pathpiecel_17; 36 of the 45 models).

Their repositories ship another model's tokenizer.json as a stand-in, or none, so the tokenizer comes from the
scheme's .vocab file through Kensho's `pathpiece` package, with the segmentation flags the scheme was trained with:

    pathpiecer*            greedy=False, random_tiebreaker=True    (PathPieceR)
    pathpiecel*            greedy=False, random_tiebreaker=False   (PathPieceL)
    sage* / *greedy*       greedy=True,  random_tiebreaker=False

The flags are read from the model name unless model_args names them. The vocabulary directory is `vocab_dir`, else
$TIMTC_VOCAB_DIR, else $CODE_DIR/timtc_vocabs_models/vocabularies. PathPiece adds <|endoftext|> as id 0 on top of the
vocabulary's lines, so the vocabulary size is the line count plus one, which is the checkpoint's vocab_size. The
weights load and generate as in mpt_hf, which this class inherits.

    lm_eval --model pathpiece_hf --model_args pretrained=luisfrentzen/pathpiecer_none_18_32768 --tasks blimp
    lm_eval --model pathpiece_hf --model_args pretrained=...,greedy=true,random_tiebreaker=false
"""

import os
from pathlib import Path
from typing import List, Optional, Tuple, Union

import torch

import pathpiece
from lm_eval.api.registry import register_model
from lm_eval.models.mpt_hf import MPTNativeCacheHFLM, as_bool

HF_TOKENIZER_SCHEMES = ("bpe_merge_3", "unigram_likelihood_2", "wordpiece_5")  # the schemes that run through mpt_hf
EOS = "<|endoftext|>"
EOS_ID = 0


def default_vocab_dir() -> str:
    if os.environ.get("TIMTC_VOCAB_DIR"):
        return os.environ["TIMTC_VOCAB_DIR"]
    if os.environ.get("CODE_DIR"):
        return os.path.join(os.environ["CODE_DIR"], "timtc_vocabs_models", "vocabularies")
    raise EnvironmentError("no vocabulary directory: pass vocab_dir= or set TIMTC_VOCAB_DIR (setup/env.sh does)")


def infer_flags(model_name: str) -> Tuple[bool, bool]:
    """(greedy, random_tiebreaker) from a TIMTC model name; an error for the schemes with an HF tokenizer."""
    name = Path(model_name).name.lower()
    if any(name.startswith(scheme) for scheme in HF_TOKENIZER_SCHEMES):
        raise ValueError(f"{model_name} has an HF tokenizer ({', '.join(HF_TOKENIZER_SCHEMES)}); use --model mpt_hf")
    if "pathpiecer" in name:
        return False, True
    if "pathpiecel" in name:
        return False, False
    if "sage" in name or "greedy" in name:
        return True, False
    raise ValueError(f"cannot infer the PathPiece flags of {model_name}; pass greedy= and random_tiebreaker=")


def make_pathpiece(vocab_path: str, greedy: bool, random_tiebreaker: bool):
    """A pathpiece.Tokenizer, whichever of the two signatures the installed package has."""
    try:
        return pathpiece.Tokenizer(vocab_path, special=EOS, greedy=greedy, random_tiebreaker=random_tiebreaker)
    except TypeError:
        return pathpiece.Tokenizer(vocab_path, EOS, greedy, random_tiebreaker)


class PathPieceWrapper:
    """A pathpiece.Tokenizer behind the part of the HuggingFace tokenizer interface the harness touches."""

    def __init__(self, tokenizer, vocab_size: int, name_or_path: str = "pathpiece"):
        self._tokenizer = tokenizer
        self.vocab_size = vocab_size
        self.name_or_path = name_or_path
        self.eos_token_id = EOS_ID
        self.pad_token_id = EOS_ID
        self.bos_token_id = None
        self.unk_token_id = None
        self.eos_token = EOS
        self.pad_token = EOS
        self.bos_token = None
        self.unk_token = None
        self.padding_side = "left"
        self.model_max_length = int(1e9)
        self.chat_template = None
        self.special_tokens_map = {"eos_token": EOS, "pad_token": EOS}
        self.all_special_ids = [EOS_ID]

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
        input_ids = self._ids(text) if isinstance(text, str) else [self._ids(t) for t in text]
        if return_tensors != "pt":
            return {"input_ids": input_ids}
        if input_ids and isinstance(input_ids[0], list):
            longest = max(len(ids) for ids in input_ids)
            padded = [ids + [self.pad_token_id] * (longest - len(ids)) for ids in input_ids]
            return {"input_ids": torch.tensor(padded)}
        return {"input_ids": torch.tensor([input_ids])}

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
        if tokens == EOS:
            return EOS_ID
        raise KeyError(tokens)


@register_model("pathpiece_hf")
class PathPieceHFLM(MPTNativeCacheHFLM):
    """A TIMTC checkpoint with its native PathPiece tokenizer."""

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
        if vocab_path is None:
            vocab_path = os.path.join(vocab_dir or default_vocab_dir(), f"{model_name}.vocab")
        if not Path(vocab_path).exists():
            raise FileNotFoundError(f"vocabulary file not found: {vocab_path} (set vocab_path= or TIMTC_VOCAB_DIR)")
        inferred_greedy, inferred_random = infer_flags(model_name)
        self._greedy = as_bool(greedy, inferred_greedy)
        self._random_tiebreaker = as_bool(random_tiebreaker, inferred_random)
        self._pathpiece_tokenizer = make_pathpiece(vocab_path, self._greedy, self._random_tiebreaker)
        self._vocab_size = len(self._pathpiece_tokenizer.get_ids())
        self._pp_wrapper = PathPieceWrapper(self._pathpiece_tokenizer, self._vocab_size, name_or_path=pretrained)
        kwargs.pop("tokenizer", None)  # the parent must not fetch an HF tokenizer: _create_tokenizer is overridden
        super().__init__(pretrained=pretrained, native_cache=native_cache, generate_use_cache=generate_use_cache, **kwargs)
        self.tokenizer = self._pp_wrapper

    def _create_tokenizer(self, *args, **kwargs):
        """HFLM.__init__ calls this to populate self.tokenizer; the PathPiece wrapper goes in instead."""
        self.tokenizer = self._pp_wrapper
        return self.tokenizer

    def _encode_pair(self, context: str, continuation: str):
        """Context and continuation encoded separately. HFLM encodes the concatenation and cuts it at
        len(encode(context)); without pre-tokenisation (the pathpiecer_none_18 vocabularies) a token can straddle the
        boundary and the cut mis-assigns tokens, which degenerates the two-choice GLUE tasks. For every other scheme
        the boundary is a space and the two encodings coincide. The trailing-space move is HFLM's."""
        n_spaces = len(context) - len(context.rstrip())
        if n_spaces > 0:
            context, continuation = context[:-n_spaces], context[-n_spaces:] + continuation
        return self.tok_encode(context), self.tok_encode(continuation)

    def tok_encode(self, string: str, left_truncate_len=None, add_special_tokens=None) -> List[int]:
        ids = self._pathpiece_tokenizer.encode(string)["input_ids"]
        if left_truncate_len is not None and len(ids) > left_truncate_len:
            ids = ids[-left_truncate_len:]
        return ids

    def tok_decode(self, tokens: Union[List[int], torch.Tensor, int], skip_special_tokens: bool = True) -> str:
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
        longest = max(len(ids) for ids in batch)
        pad = self._pp_wrapper.pad_token_id
        if padding_side == "left":
            padded = [[pad] * (longest - len(ids)) + ids for ids in batch]
            masks = [[0] * (longest - len(ids)) + [1] * len(ids) for ids in batch]
        else:
            padded = [ids + [pad] * (longest - len(ids)) for ids in batch]
            masks = [[1] * len(ids) + [0] * (longest - len(ids)) for ids in batch]
        return torch.tensor(padded), torch.tensor(masks)

    @property
    def eot_token_id(self) -> int:
        return EOS_ID

    @property
    def max_length(self) -> int:
        return getattr(self._model.config, "max_seq_len", 2048)
