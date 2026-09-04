"""Explore deterministic identification of ambiguous programme candidates.

This experiment stays outside the application layer. It inspects only the local
context around each candidate to determine whether deterministic evidence can
identify the represented selection process without semantic services.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


SAMPLES = ("BOJA24-138-00046-48048-01_00304998.pdf",)
CONTEXT_UNITS = 8

IDENTIFIER_PATTERNS = (
    ("process", re.compile(r"\bproceso\s+selectivo\b", re.IGNORECASE)),
    ("cuerpo", re.compile(r"\bcuerpo\b", re.IGNORECASE)),
    ("escala", re.compile(r"\bescala\b", re.IGNORECASE)),
    ("especialidad", re.compile(r"\bespecialidad\b", re.IGNORECASE)),
    ("categoría", re.compile(r"\bcategor[ií]a\b", re.IGNORECASE)),
    ("turno", re.compile(r"\bturno\b", re.IGNORECASE)),
    ("acceso", re.compile(r"\bacceso\b", re.IGNORECASE)),
)


@dataclass(frozen=True)
class TextUnit:
    page: int
    order: int
    text: str


@dataclass(frozen=True)
class ProgrammeCandidate:
    start: int
    end: int
    first_topic: int
    last_topic: int


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


def find_candidates(units: list[TextUnit]) -> list[ProgrammeCandidate]:
    marker_pattern = re.compile(r"^Tema\s+(\d+)(?:\s*[.\-–—])\s*(.*)$", re.IGNORECASE)
    markers = [
        (unit, int(match.group(1)))
        for unit in units
        if (match := marker_pattern.fullmatch(unit.text))
    ]
    candidates: list[ProgrammeCandidate] = []
    start = 0
    for index in range(1, len(markers) + 1):
        if index == len(markers) or markers[index][1] != markers[index - 1][1] + 1:
            first = markers[start]
            last = markers[index - 1]
            candidates.append(
                ProgrammeCandidate(
                    start=first[0].order,
                    end=last[0].order,
                    first_topic=first[1],
                    last_topic=last[1],
                )
            )
            start = index
    return candidates


def context(units: list[TextUnit], candidate: ProgrammeCandidate) -> list[TextUnit]:
    start = max(0, candidate.start - 1 - CONTEXT_UNITS)
    end = min(len(units), candidate.end + CONTEXT_UNITS)
    return units[start:end]


def identifier_evidence(units: list[TextUnit]) -> list[tuple[str, str]]:
    evidence: list[tuple[str, str]] = []
    for unit in units:
        for name, pattern in IDENTIFIER_PATTERNS:
            if pattern.search(unit.text):
                evidence.append((name, f"u{unit.order} p{unit.page}: {unit.text}"))
    return evidence


def print_candidate(units: list[TextUnit], candidate: ProgrammeCandidate, index: int) -> None:
    local = context(units, candidate)
    evidence = identifier_evidence(local)
    print(
        f"  candidate {index}: u{candidate.start}-u{candidate.end} "
        f"Tema {candidate.first_topic}-{candidate.last_topic}"
    )
    print(f"    local context: u{local[0].order}-u{local[-1].order}")
    print(f"    identifier signals: {len(evidence)}")
    for name, line in evidence:
        print(f"      {name}: {line}")
    print("    context boundary:")
    print(f"      before: u{candidate.start - 1 if candidate.start > 1 else candidate.start}")
    print(f"      after:  u{candidate.end + 1 if candidate.end < len(units) else candidate.end}")
    if local:
        print(f"      first: {local[0].text}")
        print(f"      last:  {local[-1].text}")


def main() -> None:
    samples_dir = Path(__file__).resolve().parents[1] / "tests" / "samples"

    print("DETERMINISTIC PROGRAMME CANDIDATE IDENTIFICATION")
    print("  purpose: test whether local deterministic evidence identifies ambiguous candidates")
    print(f"  context: {CONTEXT_UNITS} units before and after each candidate")

    for sample in SAMPLES:
        units = extract_units(samples_dir / sample)
        candidates = find_candidates(units)
        print()
        print(f"DOCUMENT: {sample}")
        print(f"  text units: {len(units):,}")
        print(f"  candidates: {len(candidates)}")
        for index, candidate in enumerate(candidates, start=1):
            print_candidate(units, candidate, index)


if __name__ == "__main__":
    main()
