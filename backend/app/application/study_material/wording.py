"""Helpers to read the official wording of a programme unit."""

import re

_SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+(?=[A-Za-zÁÉÍÓÚÑáéíóúñ¿¡])")


def leading_statement(wording: str) -> str:
    """The first sentence of a unit's wording: the main subject it asks to study.

    A programme unit often lists several subjects ("La Ley X. El recurso Y. ...");
    recognising a topic only from the leading statement keeps a later mention of
    another law from making the unit look like that topic.
    """
    return _SENTENCE_BREAK.split(wording.strip(), maxsplit=1)[0]
