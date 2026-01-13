import datasets


def process_results(doc, results):
    """Check if prediction matches any of the target answers."""
    pred = results[0].strip().lower()
    targets = [t.strip().lower() for t in doc["targets"]]
    
    # Exact match against any target
    exact_match = 1.0 if pred in targets else 0.0
    
    return {"exact_match": exact_match}


# Create filter functions for each language
def _make_filter(lang):
    def filter_func(dataset):
        return dataset.filter(lambda x: x["question_language"] == lang)
    return filter_func


filter_arabic = _make_filter("arabic")
filter_bengali = _make_filter("bengali")
filter_cantonese = _make_filter("cantonese")
filter_czech = _make_filter("czech")
filter_dutch = _make_filter("dutch")
filter_english = _make_filter("english")
filter_farsi = _make_filter("farsi")
filter_french = _make_filter("french")
filter_german = _make_filter("german")
filter_hebrew = _make_filter("hebrew")
filter_hindi = _make_filter("hindi")
filter_indonesian = _make_filter("indonesian")
filter_italian = _make_filter("italian")
filter_japanese = _make_filter("japanese")
filter_khmer = _make_filter("khmer")
filter_korean = _make_filter("korean")
filter_malay = _make_filter("malay")
filter_marathi = _make_filter("marathi")
filter_polish = _make_filter("polish")
filter_portuguese = _make_filter("portuguese")
filter_romanian = _make_filter("romanian")
filter_russian = _make_filter("russian")
filter_simplified_mandarin = _make_filter("simplified_mandarin")
filter_spanish = _make_filter("spanish")
filter_swedish = _make_filter("swedish")
filter_tagalog = _make_filter("tagalog")
filter_thai = _make_filter("thai")
filter_traditional_mandarin = _make_filter("traditional_mandarin")
filter_turkish = _make_filter("turkish")
filter_urdu = _make_filter("urdu")
filter_vietnamese = _make_filter("vietnamese")
