"""
TokSuite model wrappers for lm-evaluation-harness

This module provides custom LM classes for TokSuite models that use non-HuggingFace tokenizers:
- tiktoken (GPT-4o): Uses tiktoken's o200k_base encoding
- tokenmonster: Uses tokenmonster library
- Also handles models that produce token_type_ids (mBERT, Comma, Tekken)

Usage:
    # For tiktoken-based models (GPT-4o)
    lm_eval --model toksuite_tiktoken \
        --model_args pretrained=toksuite/supertoken_models-llama_tiktoken-gpt-4o \
        --tasks winogrande --device cuda

    # For tokenmonster-based models
    lm_eval --model toksuite_tokenmonster \
        --model_args pretrained=toksuite/supertoken_models-llama_tokenmonster-englishcode-32000-consistent-v1,vocab=englishcode-32000-consistent-v1 \
        --tasks winogrande --device cuda
"""

import torch
from typing import Optional, List, Tuple, Union
from lm_eval.api.registry import register_model
from lm_eval.models.huggingface import HFLM


@register_model("toksuite_tiktoken")
class TokSuiteTiktokenLM(HFLM):
    """
    TokSuite model with tiktoken tokenizer (for GPT-4o model).
    Uses tiktoken's o200k_base encoding which is GPT-4o's tokenizer.
    """

    def __init__(
        self,
        pretrained: str,
        encoding: str = "o200k_base",
        tokenizer_name: str = None,  # Accept but ignore - we use tiktoken
        **kwargs,
    ):
        # Import tiktoken
        try:
            import tiktoken
        except ImportError:
            raise ImportError("tiktoken is required for toksuite_tiktoken model. Install with: pip install tiktoken")
        
        # Use tokenizer_name to determine encoding if provided
        if tokenizer_name and "gpt-4o" in tokenizer_name:
            encoding = "o200k_base"
        
        self._tiktoken_enc = tiktoken.get_encoding(encoding)
        
        # Create a minimal tokenizer wrapper for compatibility
        self._tok_wrapper = TiktokenWrapper(self._tiktoken_enc)
        
        # Remove tokenizer arg - we'll set it ourselves
        kwargs.pop("tokenizer", None)
        
        # We need to bypass parent's tokenizer loading by pre-setting the attribute
        # Initialize model loading components manually
        import transformers
        
        # Set tokenizer before parent init to prevent parent from loading one
        self._tokenizer = self._tok_wrapper
        
        # Now call parent with a dummy tokenizer that will be overridden
        # We use 'gpt2' as a placeholder since tiktoken doesn't have a HF tokenizer
        super().__init__(pretrained=pretrained, tokenizer="gpt2", **kwargs)
        
        # Force override the tokenizer after parent init
        self._tokenizer = self._tok_wrapper

    def _create_tokenizer(self, *args, **kwargs):
        """Override to prevent parent from creating a tokenizer."""
        # Don't call parent - we already have our tokenizer
        pass

    @property
    def tokenizer(self):
        return self._tok_wrapper
    
    @tokenizer.setter
    def tokenizer(self, value):
        # Keep our wrapper
        self._tokenizer = self._tok_wrapper

    @property 
    def eot_token_id(self):
        return self._tiktoken_enc.eot_token

    @property
    def prefix_token_id(self) -> int:
        return self._tiktoken_enc.eot_token

    @property
    def max_length(self):
        return 4096  # TokSuite models use 4096 context

    def tok_encode(self, string: str, left_truncate_len=None, add_special_tokens=None) -> List[int]:
        encoding = self._tiktoken_enc.encode(string)
        if left_truncate_len:
            encoding = encoding[-left_truncate_len:]
        return encoding

    def tok_decode(self, tokens, skip_special_tokens=True) -> str:
        if isinstance(tokens, torch.Tensor):
            tokens = tokens.tolist()
        # Handle single token (int) case
        if isinstance(tokens, int):
            tokens = [tokens]
        return self._tiktoken_enc.decode(tokens)

    def _model_call(self, inps, attn_mask=None, labels=None):
        # Remove token_type_ids if present
        if hasattr(inps, 'keys'):
            inps = {k: v for k, v in inps.items() if k != 'token_type_ids'}
        return super()._model_call(inps, attn_mask, labels)


class TiktokenWrapper:
    """Minimal wrapper to make tiktoken compatible with HF tokenizer interface."""
    
    def __init__(self, enc):
        self.enc = enc
        self.eos_token_id = enc.eot_token
        self.pad_token_id = enc.eot_token  # Use EOT as pad
        self.bos_token_id = None
        self.unk_token_id = None
        self.eos_token = "<|endoftext|>"
        self.pad_token = "<|endoftext|>"
        self.bos_token = None
        self.unk_token = None
        self.vocab_size = enc.n_vocab
        self.padding_side = "left"  # For generate_until compatibility
        
    def __call__(self, text, return_tensors=None, **kwargs):
        if isinstance(text, str):
            input_ids = self.enc.encode(text)
        else:
            input_ids = [self.enc.encode(t) for t in text]
        
        if return_tensors == "pt":
            if isinstance(input_ids[0], list):
                # Batch - need padding
                max_len = max(len(ids) for ids in input_ids)
                padded = [ids + [self.pad_token_id] * (max_len - len(ids)) for ids in input_ids]
                attention_mask = [[1] * len(ids) + [0] * (max_len - len(ids)) for ids in input_ids]
                return {
                    "input_ids": torch.tensor(padded),
                    "attention_mask": torch.tensor(attention_mask)
                }
            else:
                return {
                    "input_ids": torch.tensor([input_ids]),
                    "attention_mask": torch.ones(1, len(input_ids), dtype=torch.long)
                }
        return {"input_ids": input_ids}
    
    def encode(self, text, add_special_tokens=True):
        # Allow all special tokens to avoid ValueError for things like <|endoftext|>
        return self.enc.encode(text, allowed_special="all")
    
    def decode(self, tokens, skip_special_tokens=True):
        if isinstance(tokens, torch.Tensor):
            tokens = tokens.tolist()
        # Handle single token (int) case
        if isinstance(tokens, int):
            tokens = [tokens]
        return self.enc.decode(tokens)
    
    def batch_decode(self, sequences, skip_special_tokens=True, **kwargs):
        """Decode a batch of token sequences."""
        results = []
        for seq in sequences:
            if isinstance(seq, torch.Tensor):
                seq = seq.tolist()
            if isinstance(seq, int):
                seq = [seq]
            results.append(self.enc.decode(seq))
        return results
    
    def convert_tokens_to_ids(self, tokens):
        if isinstance(tokens, str):
            return self.enc.encode(tokens)[0] if tokens else 0
        return [self.enc.encode(t)[0] if t else 0 for t in tokens]

    def add_special_tokens(self, special_tokens_dict):
        """No-op for tiktoken."""
        return 0


@register_model("toksuite_tokenmonster")
class TokSuiteTokenMonsterLM(HFLM):
    """
    TokSuite model with TokenMonster tokenizer.
    """

    def __init__(
        self,
        pretrained: str,
        vocab: str = "englishcode-32000-consistent-v1",
        **kwargs,
    ):
        # Import tokenmonster
        try:
            import tokenmonster
        except ImportError:
            raise ImportError("tokenmonster is required. Install with: pip install tokenmonster")
        
        self._tm_vocab = tokenmonster.load(vocab)
        self._tok_wrapper = TokenMonsterWrapper(self._tm_vocab)
        
        # Remove tokenizer arg
        kwargs.pop("tokenizer", None)
        
        # Pre-set tokenizer
        self._tokenizer = self._tok_wrapper
        
        # Initialize parent with dummy tokenizer
        super().__init__(pretrained=pretrained, tokenizer="gpt2", **kwargs)
        
        # Force override
        self._tokenizer = self._tok_wrapper

    def _create_tokenizer(self, *args, **kwargs):
        """Override to prevent parent from creating a tokenizer."""
        pass

    @property
    def tokenizer(self):
        return self._tok_wrapper
    
    @tokenizer.setter
    def tokenizer(self, value):
        self._tokenizer = self._tok_wrapper

    @property
    def eot_token_id(self):
        # Use newline (token 1) as EOT - more natural for text
        return 1

    @property
    def prefix_token_id(self) -> int:
        # Use newline as prefix for consistency
        return 1

    @property
    def max_length(self):
        return 4096

    def tok_encode(self, string: str, left_truncate_len=None, add_special_tokens=None) -> List[int]:
        if not string:
            # Return a single token for empty strings to avoid assertion errors
            return [0]
        encoding = self._tm_vocab.tokenize(string).tolist()
        if not encoding:
            # Fallback if tokenization returns empty
            return [0]
        if left_truncate_len:
            encoding = encoding[-left_truncate_len:]
        return encoding

    def tok_decode(self, tokens: List[int], skip_special_tokens=True) -> str:
        if isinstance(tokens, torch.Tensor):
            tokens = tokens.tolist()
        return self._tm_vocab.decode(tokens)

    def _model_call(self, inps, attn_mask=None, labels=None):
        if hasattr(inps, 'keys'):
            inps = {k: v for k, v in inps.items() if k != 'token_type_ids'}
        return super()._model_call(inps, attn_mask, labels)

    def _encode_pair(self, context: str, continuation: str) -> Tuple[List[int], List[int]]:
        """Override to handle edge cases where tokenization produces empty continuation."""
        assert context, "Context cannot be empty!"
        
        n_spaces = len(context) - len(context.rstrip())
        if n_spaces > 0:
            continuation = context[-n_spaces:] + continuation
            context = context[:-n_spaces]
        
        whole_enc = self.tok_encode(context + continuation)
        context_enc = self.tok_encode(context)
        
        context_enc_len = len(context_enc)
        continuation_enc = whole_enc[context_enc_len:]
        
        # Handle edge case: if continuation is empty after split, encode continuation separately
        if len(continuation_enc) == 0:
            continuation_enc = self.tok_encode(continuation)
            if len(continuation_enc) == 0:
                # Last resort: use a single token
                continuation_enc = [0]
        
        return context_enc, continuation_enc


class TokenMonsterWrapper:
    """Wrapper for TokenMonster compatibility with HuggingFace tokenizer interface.
    
    TokenMonster uses:
    - Learned whitespace/boundary handling (no fixed pretokenization)
    - Capcode markers (tokens 36, 37, 38, etc.) for capitalization
    - No UNK token by default
    - vocab_size accessible via vocab.vocab_size or len(vocab)
    - token_to_id() for string->id conversion (returns None if not found)
    - id_to_token_decoded() for id->string conversion (capcode-decoded form)
    - vocab.decoder() for streaming token-by-token decoding
    
    See: https://github.com/alasdairforsythe/tokenmonster
    """
    
    def __init__(self, vocab):
        self.vocab = vocab
        # TokenMonster has no explicit EOS/BOS/PAD tokens
        # Token 0 = tab, Token 1 = newline, Token 3 = space
        self.eos_token_id = 1  # newline as EOS (more natural)
        self.pad_token_id = 0  # tab as pad (rarely used in text)
        self.bos_token_id = None
        # TokenMonster has no UNK token by default (returns None if disabled)
        self._unk_token_id = vocab.unk_token_id()
        self.eos_token = "\n"
        self.pad_token = "\t"
        self.bos_token = None
        self.unk_token = None
        self.padding_side = "left"  # Required for generation in lm-eval
        # Get actual vocab size from TokenMonster (both work)
        self._vocab_size = len(vocab)
        # Cache the dictionary for get_vocab
        self._dictionary = None
        
    @property
    def vocab_size(self):
        return self._vocab_size
    
    @property
    def unk_token_id(self):
        return self._unk_token_id
    
    def get_vocab(self):
        """Return vocabulary as dict mapping token strings to IDs."""
        if self._dictionary is None:
            self._dictionary = {}
            vocab_dict = self.vocab.get_dictionary()
            for token_id, info in vocab_dict.items():
                # Use decoded form as key
                token_str = info.get('token_decoded', info.get('token', ''))
                self._dictionary[token_str] = token_id
        return self._dictionary
        
    def __call__(self, text, return_tensors=None, **kwargs):
        # Handle both single strings and batches (list, tuple, etc.)
        is_batched = not isinstance(text, str)
        if not is_batched:
            result = self.vocab.tokenize(text)
            input_ids = result.tolist() if result is not None else []
        else:
            input_ids = []
            for t in text:
                result = self.vocab.tokenize(t)
                input_ids.append(result.tolist() if result is not None else [])
        
        if return_tensors == "pt":
            if is_batched:
                # Handle empty sequences
                if not input_ids or all(len(ids) == 0 for ids in input_ids):
                    input_ids = [[self.pad_token_id] for _ in text]
                max_len = max(len(ids) for ids in input_ids)
                # Respect padding_side for proper batch padding
                if self.padding_side == "left":
                    padded = [[self.pad_token_id] * (max_len - len(ids)) + ids for ids in input_ids]
                    attention_mask = [[0] * (max_len - len(ids)) + [1] * len(ids) for ids in input_ids]
                else:
                    padded = [ids + [self.pad_token_id] * (max_len - len(ids)) for ids in input_ids]
                    attention_mask = [[1] * len(ids) + [0] * (max_len - len(ids)) for ids in input_ids]
                return {
                    "input_ids": torch.tensor(padded),
                    "attention_mask": torch.tensor(attention_mask)
                }
            else:
                if not input_ids:
                    input_ids = [self.pad_token_id]
                return {
                    "input_ids": torch.tensor([input_ids]),
                    "attention_mask": torch.ones(1, len(input_ids), dtype=torch.long)
                }
        return {"input_ids": input_ids}
    
    def encode(self, text, add_special_tokens=True):
        """Tokenize text to token IDs."""
        result = self.vocab.tokenize(text)
        if result is None:
            return []
        return result.tolist()
    
    def decode(self, tokens, skip_special_tokens=True):
        """Decode token IDs to text. Use for complete sequences."""
        if isinstance(tokens, torch.Tensor):
            tokens = tokens.tolist()
        if not tokens:
            return ""
        return self.vocab.decode(tokens)
    
    def batch_decode(self, sequences, skip_special_tokens=True):
        """Decode multiple sequences."""
        results = []
        for seq in sequences:
            if isinstance(seq, torch.Tensor):
                seq = seq.tolist()
            results.append(self.vocab.decode(seq) if seq else "")
        return results
    
    def convert_tokens_to_ids(self, tokens):
        """Convert token strings to IDs using TokenMonster's token_to_id.
        
        Note: token_to_id returns None if token not found (not an exception).
        """
        if isinstance(tokens, str):
            result = self.vocab.token_to_id(tokens)
            return result if result is not None else self.pad_token_id
        results = []
        for tok in tokens:
            result = self.vocab.token_to_id(tok)
            results.append(result if result is not None else self.pad_token_id)
        return results
    
    def convert_ids_to_tokens(self, ids):
        """Convert token IDs to strings using TokenMonster's id_to_token_decoded.
        
        Returns the capcode-decoded form of tokens.
        """
        if isinstance(ids, int):
            result = self.vocab.id_to_token_decoded(ids)
            return result if result is not None else ""
        results = []
        for tid in ids:
            result = self.vocab.id_to_token_decoded(tid)
            results.append(result if result is not None else "")
        return results

    def add_special_tokens(self, special_tokens_dict):
        """No-op for TokenMonster - use vocab.modify() or vocab.add_special_token() instead."""
        return 0
    
    def __len__(self):
        return self._vocab_size
    
    @property
    def is_fast(self):
        """TokenMonster is a fast tokenizer."""
        return True
    
    @property 
    def model_max_length(self):
        """Return a reasonable max length."""
        return 4096


@register_model("toksuite_hf")
class TokSuiteHFLM(HFLM):
    """
    TokSuite model wrapper that handles token_type_ids issues.
    Use this for models like mBERT, Comma, Tekken that produce token_type_ids.
    
    Usage:
        lm_eval --model toksuite_hf \
            --model_args pretrained=toksuite/supertoken_models-llama_google-bert-bert-base-multilingual-cased,tokenizer=google-bert/bert-base-multilingual-cased \
            --tasks winogrande --device cuda
    """

    def __init__(self, pretrained: str, **kwargs):
        # Disable prefix token to avoid issues with some tokenizers
        kwargs.setdefault("add_bos_token", False)
        super().__init__(pretrained=pretrained, **kwargs)

    @property
    def prefix_token_id(self) -> int:
        """Override to ensure we always return a valid token ID."""
        if self.custom_prefix_token_id is not None:
            return self.custom_prefix_token_id
        if self.tokenizer.bos_token_id is not None:
            return self.tokenizer.bos_token_id
        if self.tokenizer.eos_token_id is not None:
            return self.tokenizer.eos_token_id
        # Fallback to CLS token for BERT-style tokenizers
        if hasattr(self.tokenizer, 'cls_token_id') and self.tokenizer.cls_token_id is not None:
            return self.tokenizer.cls_token_id
        # Last resort: use 0
        return 0

    def _model_generate(self, context, max_length, stop, **generation_kwargs):
        # Remove token_type_ids from generation
        generation_kwargs.pop('token_type_ids', None)
        return super()._model_generate(context, max_length, stop, **generation_kwargs)

    def _model_call(self, inps, attn_mask=None, labels=None):
        # Remove token_type_ids if present in inputs
        if isinstance(inps, dict):
            inps = {k: v for k, v in inps.items() if k != 'token_type_ids'}
        return super()._model_call(inps, attn_mask, labels)

    def tok_batch_encode(
        self,
        strings: List[str],
        padding_side: str = "left",
        left_truncate_len: int = None,
        truncation: bool = False,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Override to remove token_type_ids from batch encoding."""
        result = super().tok_batch_encode(strings, padding_side, left_truncate_len, truncation)
        # Result is (input_ids, attention_mask) - no changes needed here
        return result
