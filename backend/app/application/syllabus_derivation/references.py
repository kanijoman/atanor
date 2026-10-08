"""Explicit references to laws in syllabus wording ("Ley 19/2013", "Ley Orgánica 3/2007")."""

import re
from dataclasses import dataclass

from app.application.syllabus_derivation.text import strip_accents

# Longest kinds first so "ley organica" is not read as a plain "ley".
KINDS = ("ley organica", "real decreto legislativo", "real decreto-ley", "real decreto", "ley")
_REFERENCE = re.compile(
    rf"\b({'|'.join(re.escape(kind) for kind in KINDS)})\s+(?:num\.?\s*)?(\d{{1,4}}/\d{{4}})\b"
)


@dataclass(frozen=True)
class LawReference:
    kind: str
    number: str  # "39/2015"

    @property
    def designation(self) -> str:
        return f"{self.kind} {self.number}"


def find_references(text: str) -> tuple[LawReference, ...]:
    """The distinct law references in `text`, in order of appearance."""
    found = (LawReference(kind, number) for kind, number in _REFERENCE.findall(strip_accents(text)))
    return tuple(dict.fromkeys(found))
