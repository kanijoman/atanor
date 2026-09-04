"""Explore deterministic identification of an annex from opening evidence.

This experiment deliberately limits process identification to the opening
units of each annex. Later references to process names are ignored.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


SAMPLE = "BOE-A-2024-14098.pdf"
OPENING_UNITS = 8
PROCESS_PATTERNS = (
    ("Cuerpo General Auxiliar", re.compile(r"Cuerpo\s+General\s+Auxiliar", re.IGNORECASE)),
    ("Cuerpo General Administrativo", re.compile(r"Cuerpo\s+General\s+Administrativo", re.IGNORECASE)),
    (
        "Cuerpo de Técnicos Auxiliares de Informática",
        re.compile(r"Cuerpo\s+de\s+Técnicos\s+Auxiliares\s+de\s+Informática", re.IGNORECASE),
    ),
    (
        "Cuerpo de Gestión de la Administración Civil",
        re.compile(r"Cuerpo\s+de\s+Gestión\s+de\s+la\s+Administración\s+Civil", re.IGNORECASE),
    ),
    (
        "Cuerpo de Gestión de Sistemas e Informática",
        re.compile(r"Cuerpo\s+de\s+Gestión\s+de\s+Sistemas\s+e\s+Informática", re.IGNORECASE),
    ),
)
ANNEX_PATTERN = re.compile(r"^ANEXO\s+([IVXLCDM]+)$", re.IGNORECASE)
PROGRAMME_PATTERN = re.compile(r"^\d+\.\s*Programa\.?$", re.IGNORECASE)


@dataclass(frozen=True)
class Unit:
    page: int
    order: int
    text: str


@dataclass(frozen=True)
class Annex:
    name: str
    start: int
    end: int


def extract_units(path: Path) -> list[Unit]:
    reader = PdfReader(path)
    units: list[Unit] = []
    order = 0
    for page_number, page in enumerate(reader.pages, start=1):
        for line in (page.extract_text() or "").splitlines():
            text = " ".join(line.split())
            if not text:
                continue
            order += 1
            units.append(Unit(page_number, order, text))
    return units


def build_annexes(units: list[Unit]) -> list[Annex]:
    markers = [
        (unit.order, ANNEX_PATTERN.match(unit.text).group(1).upper())
        for unit in units
        if ANNEX_PATTERN.match(unit.text)
    ]
    return [
        Annex(
            name=name,
            start=start,
            end=(markers[index + 1][0] - 1 if index + 1 < len(markers) else len(units)),
        )
        for index, (start, name) in enumerate(markers)
    ]


def opening_units(units: list[Unit], annex: Annex) -> list[Unit]:
    end = min(annex.start + OPENING_UNITS - 1, annex.end)
    return units[annex.start - 1 : end]


def detect_processes(units: list[Unit]) -> list[str]:
    text = " ".join(unit.text for unit in units)
    return [name for name, pattern in PROCESS_PATTERNS if pattern.search(text)]


def find_programme(units: list[Unit], annex: Annex) -> Unit | None:
    for unit in units[annex.start - 1 : annex.end]:
        if PROGRAMME_PATTERN.match(unit.text):
            return unit
    return None


def main() -> None:
    samples_dir = Path(__file__).resolve().parents[1] / "tests" / "samples"
    units = extract_units(samples_dir / SAMPLE)
    annexes = build_annexes(units)

    print("DETERMINISTIC ANNEX IDENTITY")
    print(f"  sample: {SAMPLE}")
    print(f"  text units: {len(units)}")
    print(f"  annexes: {len(annexes)}")
    print(f"  opening units: {OPENING_UNITS}")
    print()
    print("ANNEX IDENTITY ASSESSMENT")
    for annex in annexes:
        opening = opening_units(units, annex)
        processes = detect_processes(opening)
        programme = find_programme(units, annex)

        if len(processes) == 1:
            status = "unique_identity"
        elif len(processes) > 1:
            status = "ambiguous_identity"
        else:
            status = "no_identity_evidence"

        print(f"  ANEXO {annex.name}")
        print(f"    opening range: u{opening[0].order}-u{opening[-1].order}")
        print(f"    process candidates: {len(processes)}")
        for process in processes:
            print(f"      -> {process}")
        print(f"    programme: {programme.text if programme else 'not found'}")
        print(f"    status: {status}")

        print("    opening evidence:")
        for unit in opening:
            print(f"      [p{unit.page} u{unit.order}] {unit.text}")
        print()


if __name__ == "__main__":
    main()
