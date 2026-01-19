"""
PathPiece model wrapper for lm-evaluation-harness

This module provides a custom LM class that uses PathPiece tokenizer
for models that require .vocab files instead of HuggingFace tokenizers.

Usage:
    lm_eval run --model pathpiece_hf \
        --model_args pretrained=luisfrentzen/sage_initbpe_firstspace_6_40960,vocab_path=/path/to/vocab.vocab,greedy=true \
        --tasks hellaswag --device cuda
"""

import torch
from typing import Optional, Union, List, Tuple
from pathlib import Path
import pathpiece
from lm_eval.api.registry import register_model
from lm_eval.models.huggingface import HFLM


@register_model("pathpiece_hf")
class PathPieceHFLM(HFLM):
    """
    HuggingFace LM with PathPiece tokenizer.
    """

    def __init__(
        self,
        pretrained: str,
        vocab_path: Optional[str] = None,
        greedy: bool = True,
        vocab_dir: str = "/home/timtc_vocabs_models/vocabularies",
        **kwargs,
    ):
        # Determine vocab path
        if vocab_path is None:
            model_name = Path(pretrained).name
            vocab_path = f"{vocab_dir}/{model_name}.vocab"
        
        if not Path(vocab_path).exists():
            raise FileNotFoundError(f"Vocab file not found: {vocab_path}")
        
        # Load PathPiece tokenizer
        self._pathpiece_tokenizer = pathpiece.Tokenizer(vocab_path, greedy=greedy)
        self._vocab_size = len(self._pathpiece_tokenizer.get_ids())
        self._greedy = greedy
        
        # Don't let parent class load tokenizer
        kwargs['tokenizer'] = None
        
        # Call parent init without tokenizer loading
        super().__init__(pretrained=pretrained, **kwargs)
        
        # Override tokenizer properties
        self._setup_pathpiece_tokenizer()
    
    def _setup_pathpiece_tokenizer(self):
        """Setup PathPiece as the tokenizer."""
        # Create a minimal tokenizer interface
        class PathPieceWrapper:
            def __init__(wrapper_self, pp_tokenizer, vocab_size):
                wrapper_self._tokenizer = pp_tokenizer
                wrapper_self.vocab_size = vocab_size
                wrapper_self.eos_token_id = 0  # PathPiece uses 0 for EOS
                wrapper_self.pad_token_id = 0
                wrapper_self.bos_token_id = None
                wrapper_self.unk_token_id = None
            
            def __call__(wrapper_self, text, return_tensors=None, **kwargs):
                if isinstance(text, str):
                    encoded = wrapper_self._tokenizer.encode(text)
                    input_ids = encoded['input_ids']
                else:
                    input_ids = [wrapper_self._tokenizer.encode(t)['input_ids'] for t in text]
                
                if return_tensors == "pt":
                    if isinstance(input_ids[0], list):
                        # Batch - need to pad
                        max_len = max(len(ids) for ids in input_ids)
                        padded = [ids + [0] * (max_len - len(ids)) for ids in input_ids]
                        return {"input_ids": torch.tensor(padded)}
                    return {"input_ids": torch.tensor([input_ids])}
                return {"input_ids": input_ids}
            
            def encode(wrapper_self, text, add_special_tokens=True):
                encoded = wrapper_self._tokenizer.encode(text)
                return encoded['input_ids']
            
            def decode(wrapper_self, token_ids, skip_special_tokens=True):
                if isinstance(token_ids, torch.Tensor):
                    token_ids = token_ids.tolist()
                # Filter out OOV tokens
                valid_ids = [t for t in token_ids if t < wrapper_self.vocab_size]
                if not valid_ids:
                    return ""
                return wrapper_self._tokenizer.decode(valid_ids)
            
            def batch_decode(wrapper_self, batch_ids, skip_special_tokens=True):
                return [wrapper_self.decode(ids, skip_special_tokens) for ids in batch_ids]
        
        self.tokenizer = PathPieceWrapper(self._pathpiece_tokenizer, self._vocab_size)
    
    def tok_encode(self, string: str, left_truncate_len=None, add_special_tokens=None) -> List[int]:
        """Encode string using PathPiece."""
        encoded = self._pathpiece_tokenizer.encode(string)
        ids = encoded['input_ids']
        
        if left_truncate_len is not None and len(ids) > left_truncate_len:
            ids = ids[-left_truncate_len:]
        
        return ids
    
    def tok_decode(self, tokens: Union[List[int], torch.Tensor], skip_special_tokens: bool = True) -> str:
        """Decode tokens using PathPiece."""
        if isinstance(tokens, torch.Tensor):
            tokens = tokens.tolist()
        
        # Filter out OOV tokens (beyond vocab size)
        valid_tokens = [t for t in tokens if t < self._vocab_size]
        
        if not valid_tokens:
            return ""
        
        return self._pathpiece_tokenizer.decode(valid_tokens)
    
    def tok_batch_encode(
        self,
        strings: List[str],
        padding_side: str = "left",
        left_truncate_len: int = None,
        truncation: bool = False,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Batch encode strings using PathPiece."""
        
        encoded_batch = []
        for s in strings:
            ids = self.tok_encode(s, left_truncate_len=left_truncate_len)
            encoded_batch.append(ids)
        
        # Pad to max length
        max_len = max(len(ids) for ids in encoded_batch)
        
        if padding_side == "left":
            padded = [[0] * (max_len - len(ids)) + ids for ids in encoded_batch]
            attn_masks = [[0] * (max_len - len(ids)) + [1] * len(ids) for ids in encoded_batch]
        else:
            padded = [ids + [0] * (max_len - len(ids)) for ids in encoded_batch]
            attn_masks = [[1] * len(ids) + [0] * (max_len - len(ids)) for ids in encoded_batch]
        
        return torch.tensor(padded), torch.tensor(attn_masks)
    
    @property
    def eot_token_id(self) -> int:
        """End of text token ID (PathPiece uses 0)."""
        return 0
    
    @property  
    def max_length(self) -> int:
        """Maximum sequence length."""
        if hasattr(self._model.config, 'max_seq_len'):
            return self._model.config.max_seq_len
        return 2048


# Convenience function to check if a model needs PathPiece
def needs_pathpiece(model_name: str, vocab_dir: str = "/home/timtc_vocabs_models/vocabularies") -> bool:
    """Check if a model needs PathPiece tokenizer (has .vocab file)."""
    vocab_path = Path(vocab_dir) / f"{model_name}.vocab"
    return vocab_path.exists()


def get_tokenizer_type(model_name: str, vocab_dir: str = "/home/timtc_vocabs_models/vocabularies") -> str:
    """Get the tokenizer type for a model."""
    vocab_path = Path(vocab_dir) / f"{model_name}.vocab"
    json_path = Path(vocab_dir) / f"{model_name}.json"
    
    if json_path.exists():
        return "huggingface"
    elif vocab_path.exists():
        # Check if greedy or optimal
        if any(x in model_name for x in ["greedy", "sage", "wordpiece"]):
            return "pathpiece_greedy"
        else:
            return "pathpiece_optimal"
    else:
        return "unknown"
