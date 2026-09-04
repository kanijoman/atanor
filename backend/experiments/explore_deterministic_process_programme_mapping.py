"""Explore deterministic mapping between selection processes and programmes.

This experiment does not implement a parser. It tests whether process occurrences
can be associated with their enclosing annex/programme and deliberately exposes
ambiguity instead of forcing a single mapping.
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
    "Cuerpo Gestión de Sistemas e Informática",
)
ANNEX_PATTERN = re.compile(r"^ANEXO\s+([IVXLCDM]+)$", re.IGNORECASE)
PROGRAMME_PATTERN = re.compile(r"^\d+\.\s*Programa\.?$", re.IGNORECASE)


@dataclass(frozen=True)
class Unit:
    page: int
    order: int
    text: str


@dataclass(frozen=True)
class Programme:
    annex: str
    programme_text: str
    start: int
    end: int


def extract_units(path: Path) -> list[Unit]:
    reader = PdfReader(path)
    units: list[Unit] = []
    order = 0
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for line in text.splitlines():
            normalized = " ".join(line.split())
            if not normalized:
                continue
            order += 1
            units.append(Unit(page_number, order, normalized))
    return units


def find_process_occurrences(units: list[Unit]) -> list[tuple[str, int]]:
    occurrences: list[tuple[str, int]] = []
    for marker in PROCESS_MARKERS:
        for unit in units:
            if marker.casefold() in unit.text.casefold():
                occurrences.append((marker, unit.order))
    return sorted(occurrences, key=lambda item: item[1])


def build_programmes(units: list[Unit]) -> list[Programme]:
    annexes = [
        (unit.order, ANNEX_PATTERN.match(unit.text).group(1).upper())
        for unit in units
        if ANNEX_PATTERN.match(unit.text)
    ]
    programmes = [
        unit.order
        for unit in units
        if PROGRAMME_PATTERN.match(unit.text)
    ]

    result: list[Programme] = []
    for annex_index, (annex_start, annex_name) in enumerate(annexes):
        annex_end = (
            annexes[annex_index + 1][0] - 1
            if annex_index + 1 < len(annexes)
            else len(units)
        )
        annex_programmes = [
            order for order in programmes if annex_start <= order <= annex_end
        ]
        for programme_index, programme_start in enumerate(annex_programmes):
            programme_end = (
                annex_programmes[programme_index + 1] - 1
                if programme_index + 1 < len(annex_programmes)
                else annex_end
            )
            programme_unit = units[programme_start - 1]
            result.append(
                Programme(
                    annex=annex_name,
                    programme_text=programme_unit.text,
                    start=programme_start,
                    end=programme_end,
                )
            )
    return result


def enclosing_programme(order: int, programmes: list[Programme]) -> Programme | None:
    candidates = [programme for programme in programmes if programme.start <= order <= programme.end]
    return candidates[-1] if candidates else None


def nearby_context(units: list[Unit], order: int, radius: int = 2) -> list[Unit]:
    index = order - 1
    return units[max(0, index - radius) : min(len(units), index + radius + 1)]


def main() -> None:
    samples_dir = Path(__file__).resolve().parents[1] / "tests" / "samples"
    units = extract_units(samples_dir / SAMPLE)
    programmes = build_programmes(units)
    occurrences = find_process_occurrences(units)

    print("DETERMINISTIC PROCESS-PROGRAMME MAPPING")
    print(f"  sample: {SAMPLE}")
    print(f"  text units: {len(units)}")
    print(f"  process markers: {len(PROCESS_MARKERS)}")
    print(f"  process occurrences: {len(occurrences)}")
    print(f"  programmes: {len(programmes)}")
    print()
    print("PROCESS OCCURRENCES")
    for marker, order in occurrences:
        unit = units[order - 1]
        programme = enclosing_programme(order, programmes)
        mapping = (
            f"ANEXO {programme.annex} / {programme.programme_text}"
            if programme
            else "outside programme"
        )
        print(f"  {marker} [p{unit.page} u{order}] -> {mapping}")
        for context_unit in nearby_context(units, order):
            print(f"    [p{context_unit.page} u{context_unit.order}] {context_unit.text}")

    print()
    print("MAPPING SUMMARY")
    for marker in PROCESS_MARKERS:
        marker_occurrences = [order for candidate, order in occurrences if candidate == marker]
        mapped = [
            enclosing_programme(order, programmes)
            for order in marker_occurrences
        ]
        mapped = [programme for programme in mapped if programme is not None]
        unique = sorted({(programme.annex, programme.start) for programme in mapped})
        print(f"  {marker}")
        print(f"    occurrences: {len(marker_occurrences)}")
        print(f"    programme candidates: {len(unique)}")
        for annex, start in unique:
            programme = next(p for p in mapped if p.annex == annex and p.start == start)
            print(f"      -> ANEXO {annex} / u{programme.start}: {programme.programme_text}")
        if len(unique) == 1:
            status = "unique_mapping"
        elif len(unique) > 1:
            status = "ambiguous_mapping"
        else:
            status = "unmapped"
        print(f"    status: {status}")


if __name__ == "__main__":
    main()
