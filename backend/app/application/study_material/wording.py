"""Helpers to read the official wording of a programme unit."""

import re

_SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+(?=[A-Za-zÁÉÍÓÚÑáéíóúñ¿¡])")


def states_subject_with_scope(wording: str, subject: str, scope_terms: tuple[str, ...]) -> bool:
    """Whether a (casefolded) unit wording asks for `subject` and for everything in `scope_terms`.

    A topic's material is designed around a concrete scope. A unit that opens with
    the same subject but asks for something else (another body lists other
    subtopics) must not be presented as covered by that material.
    """
    return leading_statement(wording).startswith(subject) and all(
        term in wording for term in scope_terms
    )


def leading_statement(wording: str) -> str:
    """The first sentence of a unit's wording: the main subject it asks to study.

    A programme unit often lists several subjects ("La Ley X. El recurso Y. ...");
    recognising a topic only from the leading statement keeps a later mention of
    another law from making the unit look like that topic.
    """
    return _SENTENCE_BREAK.split(wording.strip(), maxsplit=1)[0]
