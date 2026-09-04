"""Explore deterministic programme-scope selection from structural evidence.

This experiment stays outside the application layer. It tests whether a source
can yield one, several, or no defensible programme scopes without semantic
services or arbitrary proximity rules. The heuristics are experimental.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


SAMPLES = (
    "BOE-A-2024-14098.pdf",
    "BOJA24-138-00046-48048-01_00304998.pdf",
    "Programa_Archiveros_0.pdf",
)

TARGET_PROCESS = "Cuerpo de Técnicos Auxiliares de Informática"

ANNEX_PATTERN = re.compile(r"^ANEXO\s+([IVXLCDM]+)$", re.IGNORECASE)
PROGRAMME_PATTERN = re.compile(r"^\d+\.\s*Programa\.?$", re.IGNORECASE)
TEMA_PATTERN = re.compile(r"^Tema\s+(\d+)(?:\s*[.\-–—])\s*(.*)$", re.IGNORECASE)
PROCESS_PATTERN = re.compile(
    r"Cuerpo\s+de\s+Técnicos\s+Auxiliares\s+de\s+Informática",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class TextUnit:
    page: int
    order: int
    text: str


@dataclass(frozen=True)
class Annex:
    name: str
    start: int
    end: int


@dataclass(frozen=True)
class ProgrammeCandidate:
    start: int
    end: int
    marker: int | None
    units: int
    evidence: str


def extract_units(path: Path) -> list[TextUnit]:
    reader = PdfReader(path)
    units: list[TextUnit] = []
    order = 0
    for page_number, page in enumerate(reader.pages, start=1):
        for line in (page.extract_text() or "").splitlines():
            text = " ".join(line.split())
            if text:
                order += 1
                units.append(TextUnit(page_number, order, text))
    return units


def build_annexes(units: list[TextUnit]) -> list[Annex]:
    markers = [
        (unit.order, match.group(1).upper())
        for unit in units
        if (match := ANNEX_PATTERN.fullmatch(unit.text))
    ]
    return [
        Annex(
            name=name,
            start=start,
            end=markers[index + 1][0] - 1
            if index + 1 < len(markers)
            else len(units),
        )
        for index, (start, name) in enumerate(markers)
    ]


def find_programme(units: list[TextUnit], annex: Annex) -> TextUnit | None:
    return next(
        (
            unit
            for unit in units[annex.start - 1 : annex.end]
            if PROGRAMME_PATTERN.fullmatch(unit.text)
        ),
        None,
    )


def opening_contains_process(units: list[TextUnit], annex: Annex, size: int = 8) -> bool:
    opening = units[annex.start - 1 : min(annex.end, annex.start + size - 1)]
    return any(PROCESS_PATTERN.search(unit.text) for unit in opening)


def boe_candidate(units: list[TextUnit], annex: Annex) -> ProgrammeCandidate | None:
    if not opening_contains_process(units, annex):
        return None
    programme = find_programme(units, annex)
    if programme is None:
        return None
    return ProgrammeCandidate(
        start=programme.order,
        end=annex.end,
        marker=programme.order,
        units=sum(
            1
            for unit in units[programme.order - 1 : annex.end]
            if unit.order >= programme.order
        ),
        evidence=f"ANEXO {annex.name} opening identifies target process",
    )


def tema_sequences(units: list[TextUnit]) -> list[ProgrammeCandidate]:
    markers = [
        (unit, int(match.group(1)))
        for unit in units
        if (match := TEMA_PATTERN.fullmatch(unit.text))
    ]
    if not markers:
        return []

    candidates: list[ProgrammeCandidate] = []
    start_index = 0
    for index in range(1, len(markers) + 1):
        if index == len(markers) or markers[index][1] != markers[index - 1][1] + 1:
            first = markers[start_index][0]
            last = markers[index - 1][0]
            candidates.append(
                ProgrammeCandidate(
                    start=first.order,
                    end=last.order,
                    marker=None,
                    units=index - start_index,
                    evidence=f"Tema sequence {markers[start_index][1]}-{markers[index - 1][1]}",
                )
            )
            start_index = index
    return candidates


def classify(candidates: list[ProgrammeCandidate]) -> str:
    if not candidates:
        return "NOT_FOUND"
    if len(candidates) == 1:
        return "SELECTED"
    return "AMBIGUOUS"


def print_candidate(candidate: ProgrammeCandidate, index: int) -> None:
    marker = f"u{candidate.marker}" if candidate.marker else "none"
    print(
        f"    candidate {index}: u{candidate.start}-u{candidate.end} "
        f"units={candidate.units} marker={marker}"
    )
    print(f"      evidence: {candidate.evidence}")


def main() -> None:
    samples_dir = Path(__file__).resolve().parents[1] / "tests" / "samples"

    print("DETERMINISTIC PROGRAMME SCOPE SELECTION")
    print("  purpose: select a programme only when structural evidence is sufficient")
    print("  outcomes: SELECTED | AMBIGUOUS | NOT_FOUND")

    for sample in SAMPLES:
        units = extract_units(samples_dir / sample)
        print()
        print(f"DOCUMENT: {sample}")
        print(f"  text units: {len(units):,}")
        if not units:
            print("  status: NOT_FOUND")
            print("  reason: no extractable text")
            continue

        annexes = build_annexes(units)
        candidates: list[ProgrammeCandidate]

        if sample.startswith("BOE-"):
            candidates = [
                candidate
                for annex in annexes
                if (candidate := boe_candidate(units, annex)) is not None
            ]
            strategy = "target process → annex opening evidence → programme marker"
        else:
            candidates = tema_sequences(units)
            strategy = "continuous Tema numbering sequences"

        print(f"  strategy: {strategy}")
        print(f"  candidates: {len(candidates)}")
        print(f"  status: {classify(candidates)}")
        for index, candidate in enumerate(candidates, start=1):
            print_candidate(candidate, index)


if __name__ == "__main__":
    main()
