import math
import re


def process_results(doc, results):
    """Process results for FLORES NLL task.
    
    Computes word perplexity, byte perplexity, bits per byte, and mean NLL.
    Based on the Goldfish paper (Appendix A3).
    """
    (loglikelihood,) = results
    sentence = doc["sentence"]
    
    # Count words (split on whitespace)
    _words = len(re.split(r"\s+", sentence.strip()))
    # Count bytes
    _bytes = len(sentence.encode("utf-8"))
    
    # Mean negative log likelihood (per sentence)
    mean_nll = -loglikelihood
    
    return {
        "word_perplexity": (loglikelihood, _words),
        "byte_perplexity": (loglikelihood, _bytes),
        "bits_per_byte": (loglikelihood, _bytes),
        "mean_nll": mean_nll,
    }


def weighted_perplexity(items):
    """Aggregate word/byte perplexity using weighted sum.
    
    items: list of (loglikelihood, count) tuples
    Returns: perplexity = exp(-sum(loglikelihoods) / sum(counts))
    """
    total_ll = sum(ll for ll, _ in items)
    total_count = sum(count for _, count in items)
    
    if total_count == 0:
        return float("inf")
    
    return math.exp(-total_ll / total_count)


def bits_per_byte(items):
    """Aggregate bits per byte.
    
    items: list of (loglikelihood, byte_count) tuples
    Returns: bits_per_byte = -sum(loglikelihoods) / sum(bytes) / ln(2)
    """
    total_ll = sum(ll for ll, _ in items)
    total_bytes = sum(count for _, count in items)
    
    if total_bytes == 0:
        return float("inf")
    
    return -total_ll / total_bytes / math.log(2)
