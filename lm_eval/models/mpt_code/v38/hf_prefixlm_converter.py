# SOAR-COMPAT-STUB: the original imported _expand_mask/_make_causal_mask from
# transformers.models.{bloom,opt}, removed in modern transformers. Dead code for TIMTC
# (prefix_lm: False in every config). Original kept next to this file as .orig.
def convert_hf_causal_lm_to_prefix_lm(model):
    raise NotImplementedError("prefix_lm is not supported by the SOAR compat stub")


def add_bidirectional_mask_if_missing(batch):
    return batch
