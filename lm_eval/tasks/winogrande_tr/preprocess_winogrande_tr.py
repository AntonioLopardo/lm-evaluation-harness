def doc_to_text(doc):
    """Return the answer index (0 or 1) for the correct option."""
    answer_to_num = {"1": 0, "2": 1}
    return answer_to_num[str(doc["answer"])]


def doc_to_target(doc):
    """Return the text after the blank marker."""
    idx = doc["sentence"].index("_") + 1
    return doc["sentence"][idx:].strip()


def doc_to_choice(doc):
    """Create full sentences by inserting each option at the blank position."""
    idx = doc["sentence"].index("_")
    options = [doc["option1"], doc["option2"]]
    return [doc["sentence"][:idx] + opt for opt in options]


def _option_in_sentence(option: str, sentence: str) -> bool:
    """Check if option appears in sentence as a whole word or with Turkish suffixes.
    
    Uses word boundary matching to avoid false positives like 'Sara' in 'Sarah'.
    For common nouns, also handles Turkish agglutinative suffixes (e.g. "yatak" -> "yatağı").
    For proper nouns (capitalized), requires exact word match only.
    """
    import re
    
    option_lower = option.lower()
    sentence_lower = sentence.lower()
    
    # 1. Exact word boundary match (handles most cases including proper nouns)
    pattern = r'\b' + re.escape(option_lower) + r'\b'
    if re.search(pattern, sentence_lower):
        return True
    
    # 2. For proper nouns (capitalized options like names), don't do suffix matching
    # This prevents "Sara" matching "Sarah" or "Neil" matching "Neilson"
    is_proper_noun = option[0].isupper() if option else False
    if is_proper_noun:
        return False
    
    # 3. Turkish suffix handling for common nouns only
    # Turkish adds suffixes without changing the base word in most cases
    # e.g., "battaniye" -> "battaniyeyi", "battaniyeden"
    # But some words undergo consonant mutation: k->ğ, t->d, p->b, ç->c
    
    mutations = {
        'k': 'ğ',  # yatak -> yatağ-ı
        't': 'd',  # kanat -> kanad-ı
        'p': 'b',  # kitap -> kitab-ı
        'ç': 'c',  # ağaç -> ağac-ı
    }
    
    for word in re.findall(r'\b\w+\b', sentence_lower):
        # Direct prefix match for suffix forms (battaniye -> battaniyeyi)
        if word.startswith(option_lower) and len(word) > len(option_lower):
            return True
        
        # Check if word starts with mutated form of option (yatak -> yatağı)
        if len(option_lower) >= 2:
            last_char = option_lower[-1]
            if last_char in mutations:
                mutated = option_lower[:-1] + mutations[last_char]
                if word.startswith(mutated):
                    return True
    
    return False


def filter_valid_samples(dataset):
    """Filter out samples where options don't appear in the sentence.
    
    The Turkish Winogrande dataset has translation quality issues where
    ~42% of samples have mismatches between option text and sentence text.
    This includes:
    - Name spelling differences (Sarah/Sara, Neil/Nil, Adam/Adem)
    - Translated names (Hunter/Avcı)
    - Word form differences (yatak/yatağı, tost makinası/ekmek kızartma makinesi)
    
    We filter to keep only samples where both options appear in the sentence,
    which gives us a clean subset for valid evaluation.
    """
    def is_valid(doc):
        sentence = doc["sentence"]
        opt1 = doc["option1"]
        opt2 = doc["option2"]
        return _option_in_sentence(opt1, sentence) and _option_in_sentence(opt2, sentence)
    
    return dataset.filter(is_valid)
