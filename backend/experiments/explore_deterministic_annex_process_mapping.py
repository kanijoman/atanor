"""Explore deterministic mapping between annexes and selection processes.

The experiment tests whether the opening/header units of an annex identify a
selection process strongly enough to map that annex to its programme.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


SAMPLE = "BOE-A-2024-14098.pdf"
PROCESS_MARKERS = (
    "Cuerpo General Auxiliar",
    "Cuerpo General Administrativo",
    "Cuerpo de Técnicos Auxiliares de Informática",
    "Cuerpo Gestión Administración Civil",
    "Cuerpo de Gestión de Sistemas e Informática",
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
    programme_start: int | None


def extract_units(path: Path) -> list[Unit]:
    reader = PdfReader(path)
    units: list[Unit] = []
    order = 0
    for page_number, page in enumerate(reader.pages, start=1):
        for line in (page.extract_text() or "").splitlines():
            text = " ".join(line.split())
            if text:
                order += 1
                units.append(Unit(page_number, order, text))
    return units


def build_annexes(units: list[Unit]) -> list[Annex]:
    markers = [
        (unit.order, ANNEX_PATTERN.match(unit.text).group(1).upper())
        for unit in units
        if ANNEX_PATTERN.match(unit.text)
    ]
    result: list[Annex] = []
    for index, (start, name) in enumerate(markers):
        end = markers[index + 1][0] - 1 if index + 1 < len(markers) else len(units)
        programme_candidates = [
            unit.order
            for unit in units
            if start <= unit.order <= end and PROGRAMME_PATTERN.match(unit.text)
        ]
        result.append(Annex(name, start, end, programme_candidates[0] if programme_candidates else None))
    return result


def process_matches(units: list[Unit], start: int, end: int) -> list[tuple[str, int]]:
    matches: list[tuple[str, int]] = []
    for marker in PROCESS_MARKERS:
        for unit in units[start - 1 : end]:
            if marker.casefold() in unit.text.casefold():
                matches.append((marker, unit.order))
    return sorted(matches, key=lambda item: item[1])


def opening_units(units: list[Unit], annex: Annex, radius: int = 8) -> list[Unit]:
    return units[annex.start - 1 : min(annex.end, annex.start + radius - 1)]


def main() -> None:
    samples_dir = Path(__file__).resolve().parents[1] / "tests" / "samples"
    units = extract_units(samples_dir / SAMPLE)
    annexes = build_annexes(units)

    print("DETERMINISTIC ANNEX-PROCESS MAPPING")
    print(f"  sample: {SAMPLE}")
    print(f"  text units: {len(units)}")
    print(f"  annexes: {len(annexes)}")
    print()
    print("ANNEX CANDIDATES")
    for annex in annexes:
        matches = process_matches(units, annex.start, annex.end)
        unique = []
        for marker, _ in matches:
            if marker not in unique:
                unique.append(marker)
        programme = units[annex.programme_start - 1].text if annex.programme_start else "none"
        print(f"  ANEXO {annex.name}")
        print(f"    range: u{annex.start}-u{annex.end}")
        print(f"    process matches: {len(matches)}")
        print(f"    process candidates: {len(unique)}")
        for marker in unique:
            first = next(order for candidate, order in matches if candidate == marker)
            print(f"      -> {marker} [u{first}]")
        print(f"    programme: {programme}")

    print()
    print("OPENING EVIDENCE")
    for annex in annexes:
        print(f"  ANEXO {annex.name}")
        for unit in opening_units(units, annex):
            print(f"    [p{unit.page} u{unit.order}] {unit.text}")

    print()
    print("MAPPING ASSESSMENT")
    for annex in annexes:
        matches = process_matches(units, annex.start, annex.end)
        unique = []
        for marker, _ in matches:
            if marker not in unique:
                unique.append(marker)
        if len(unique) == 1 and annex.programme_start is not None:
            status = "unique_mapping"
        elif len(unique) > 1:
            status = "ambiguous_process"
        elif not unique:
            status = "no_process_evidence"
        else:
            status = "process_without_programme"
        print(f"  ANEXO {annex.name}: {status}")


if __name__ == "__main__":
    main()
