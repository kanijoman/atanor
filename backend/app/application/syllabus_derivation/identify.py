"""Decide which laws a syllabus unit refers to, and say why."""

import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from app.application.normative_source import NormativeSourceCandidate
from app.application.syllabus_derivation.law_catalog import SEED_LAWS, SeedLaw
from app.application.syllabus_derivation.references import LawReference, find_references
from app.application.syllabus_derivation.text import strip_accents


@dataclass(frozen=True)
class IdentifiedLaw:
    law: NormativeSourceCandidate
    basis: Literal["reference", "keywords"]
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class LawIdentification:
    laws: tuple[IdentifiedLaw, ...]
    # Cited laws that are not in the seed catalog; a BOE lookup may still resolve them.
    unresolved_references: tuple[LawReference, ...]

    @property
    def identifiers(self) -> frozenset[str]:
        return frozenset(item.law.identifier for item in self.laws)


def _mentions(text: str, phrase: str) -> bool:
    return re.search(rf"\b{re.escape(phrase)}\b", text) is not None


def identify_laws(text: str, catalog: Sequence[SeedLaw] = SEED_LAWS) -> LawIdentification:
    normalized = strip_accents(text)
    by_designation: dict[str, IdentifiedLaw] = {}
    unresolved: list[LawReference] = []
    for reference in find_references(text):
        seed = next((law for law in catalog if law.designation == reference.designation), None)
        if seed is None:
            unresolved.append(reference)
        else:
            by_designation[seed.designation] = IdentifiedLaw(
                seed.candidate, "reference", (reference.designation,)
            )
    for seed in catalog:
        if seed.designation in by_designation:
            continue
        evidence = tuple(word for word in seed.keywords if _mentions(normalized, word))
        if evidence:
            by_designation[seed.designation] = IdentifiedLaw(seed.candidate, "keywords", evidence)
    return LawIdentification(tuple(by_designation.values()), tuple(unresolved))
