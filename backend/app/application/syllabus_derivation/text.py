"""Deterministic Spanish text normalisation for matching syllabus wording against laws."""

import re
import unicodedata

# Function words that carry no subject matter in legal and syllabus Spanish.
STOPWORDS = frozenset(
    [
        "de",
        "la",
        "el",
        "los",
        "las",
        "y",
        "en",
        "a",
        "que",
        "del",
        "al",
        "por",
        "con",
        "para",
        "un",
        "una",
        "es",
        "se",
        "lo",
        "su",
        "sus",
        "o",
        "como",
        "mas",
        "e",
        "u",
        "le",
        "les",
        "este",
        "esta",
        "estos",
        "estas",
        "sobre",
        "entre",
        "sin",
        "ser",
        "son",
        "han",
        "ha",
        "tiene",
        "tienen",
        "sera",
        "seran",
        "podra",
        "podran",
        "cada",
        "todo",
        "toda",
        "todos",
        "todas",
        "cuando",
        "donde",
        "asi",
        "segun",
        "ante",
        "bajo",
        "desde",
        "hasta",
        "hacia",
        "durante",
        "mediante",
    ]
)
# Truncating words to a fixed prefix is a cheap, language-independent stemmer: it maps
# "retribuciones" and "retribución" to the same term without any dictionary.
STEM_LENGTH = 6
_WORD = re.compile(r"[a-z0-9]+")


def strip_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(char for char in decomposed if unicodedata.category(char) != "Mn")


def tokens(text: str) -> list[str]:
    """Stemmed content words of `text`, in order and with repetitions."""
    return [
        word[:STEM_LENGTH]
        for word in _WORD.findall(strip_accents(text))
        if word not in STOPWORDS and len(word) > 2
    ]
