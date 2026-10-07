"""Helpers to read the official wording of a programme unit."""

import re

_SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+(?=[A-Za-zÁÉÍÓÚÑáéíóúñ¿¡])")


def statements(wording: str) -> list[str]:
    """The sentences of a unit's wording: each one names a subject the candidate must study."""
    return [part for part in _SENTENCE_BREAK.split(wording.strip()) if part]


def states_subject_with_scope(wording: str, subject: str, scope_terms: tuple[str, ...]) -> bool:
    """Whether a (casefolded) unit wording asks for exactly what a topic's material covers.

    A topic's material is designed around a concrete scope: its `subject` and one
    marker in `scope_terms` per further statement. The wording matches when it opens
    with the subject, mentions every marker, and has no statement the topic does not
    account for. A syllabus that opens with the same subject but lists other
    subtopics, or asks for more than the material covers, must not be presented as
    covered by that material.
    """
    if not leading_statement(wording).startswith(subject):
        return False
    if not all(term in wording for term in scope_terms):
        return False
    markers = (subject, *scope_terms)
    return all(any(marker in statement for marker in markers) for statement in statements(wording))


def leading_statement(wording: str) -> str:
    """The first sentence of a unit's wording: the main subject it asks to study.

    A programme unit often lists several subjects ("La Ley X. El recurso Y. ...");
    recognising a topic only from the leading statement keeps a later mention of
    another law from making the unit look like that topic.
    """
    return _SENTENCE_BREAK.split(wording.strip(), maxsplit=1)[0]
