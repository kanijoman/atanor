"""Explore deterministic extraction of study units from heterogeneous programme structures.

This experiment stays outside the application layer. It tests whether source-specific
structural observations can be reduced to a common, traceable study-unit representation.
The heuristics are experimental and must not become product contracts.
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
ROMAN_PATTERN = re.compile(r"^([IVXLCDM]+)\.\s+(.+)$", re.IGNORECASE)
ITEM_PATTERN = re.compile(r"^(\d+)\.\s+(.+)$")
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
class StudyUnit:
    marker: str
    number: int
    title: str
    section: str | None
    start: int
    end: int
    page: int


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
        (unit.order, ANNEX_PATTERN.fullmatch(unit.text).group(1).upper())
        for unit in units
        if ANNEX_PATTERN.fullmatch(unit.text)
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
    for unit in units[annex.start - 1 : annex.end]:
        if PROGRAMME_PATTERN.fullmatch(unit.text):
            return unit
    return None


def process_is_in_opening(units: list[TextUnit], annex: Annex, opening_size: int = 8) -> bool:
    opening = units[annex.start - 1 : min(annex.end, annex.start + opening_size - 1)]
    return any(PROCESS_PATTERN.search(unit.text) for unit in opening)


def extract_boe_units(units: list[TextUnit], annex: Annex) -> tuple[int | None, list[StudyUnit]]:
    programme = find_programme(units, annex)
    if programme is None:
        return None, []

    scoped = units[programme.order - 1 : annex.end]
    sections: list[tuple[str, int]] = []
    for unit in scoped:
        match = ROMAN_PATTERN.fullmatch(unit.text)
        if match:
            sections.append((match.group(1).upper(), unit.order))

    candidates = [
        unit for unit in scoped if ITEM_PATTERN.fullmatch(unit.text)
    ]
    result: list[StudyUnit] = []
    for index, unit in enumerate(candidates):
        match = ITEM_PATTERN.fullmatch(unit.text)
        assert match is not None
        next_item = candidates[index + 1] if index + 1 < len(candidates) else None
        next_section = next(
            (section for section in sections if section[1] > unit.order),
            None,
        )
        boundaries = [candidate.order for candidate in (next_item,)]
        if next_section is not None:
            boundaries.append(next_section[1])
        end = min(boundaries) - 1 if boundaries else annex.end
        section = next(
            (name for name, order in reversed(sections) if order < unit.order),
            None,
        )
        result.append(
            StudyUnit(
                marker="item",
                number=int(match.group(1)),
                title=match.group(2).strip(),
                section=section,
                start=unit.order,
                end=end,
                page=unit.page,
            )
        )
    return programme.order, result


def extract_tema_units(units: list[TextUnit], annex: Annex | None = None) -> list[StudyUnit]:
    scoped = units if annex is None else units[annex.start - 1 : annex.end]
    candidates = [unit for unit in scoped if TEMA_PATTERN.fullmatch(unit.text)]
    result: list[StudyUnit] = []
    for index, unit in enumerate(candidates):
        match = TEMA_PATTERN.fullmatch(unit.text)
        assert match is not None
        next_tema = candidates[index + 1] if index + 1 < len(candidates) else None
        end = next_tema.order - 1 if next_tema else (annex.end if annex else units[-1].order)
        result.append(
            StudyUnit(
                marker="tema",
                number=int(match.group(1)),
                title=match.group(2).strip(),
                section=None,
                start=unit.order,
                end=end,
                page=unit.page,
            )
        )
    return result


def sequence_breaks(units: list[StudyUnit]) -> int:
    return sum(
        current.number != previous.number + 1
        for previous, current in zip(units, units[1:])
    )


def print_units(units: list[StudyUnit], limit: int = 12) -> None:
    for unit in units[:limit]:
        section = f" [{unit.section}]" if unit.section else ""
        print(
            f"    {unit.marker} {unit.number}{section}: "
            f"u{unit.start}-u{unit.end} p{unit.page} | {unit.title}"
        )
    if len(units) > limit:
        print(f"    ... {len(units) - limit} more")


def main() -> None:
    samples_dir = Path(__file__).resolve().parents[1] / "tests" / "samples"

    print("DETERMINISTIC PROGRAMME UNIT EXTRACTION")
    print("  samples: BOE + BOJA + Archiveros")
    print("  purpose: extract traceable study units from source-specific structures")
    print("  common fields: marker + number + title + section + span + page")

    for sample in SAMPLES:
        path = samples_dir / sample
        units = extract_units(path)
        print()
        print(f"DOCUMENT: {sample}")
        print(f"  text units: {len(units):,}")
        if not units:
            print("  status: no_extractable_text")
            continue

        annexes = build_annexes(units)
        print(f"  annexes: {len(annexes)}")

        if sample.startswith("BOE-"):
            target_annex = next(
                (
                    annex
                    for annex in annexes
                    if process_is_in_opening(units, annex)
                    and TARGET_PROCESS.casefold()
                    in " ".join(
                        unit.text
                        for unit in units[annex.start - 1 : min(annex.end, annex.start + 7)]
                    ).casefold()
                ),
                None,
            )
            if target_annex is None:
                print("  status: target_process_not_found")
                continue

            programme_start, study_units = extract_boe_units(units, target_annex)
            print(f"  selected annex: ANEXO {target_annex.name}")
            print(f"  programme start: u{programme_start}" if programme_start else "  programme start: none")
            print("  strategy: roman section + top-level numbered items")
            print(f"  normalized units: {len(study_units):,}")
            print(f"  sequence breaks: {sequence_breaks(study_units)}")
            print("  examples:")
            print_units(study_units)
            if study_units:
                print(
                    f"  span coverage: u{study_units[0].start}-u{study_units[-1].end}"
                )
            continue

        study_units = extract_tema_units(units)
        print("  strategy: Tema N spans to next Tema marker")
        print(f"  normalized units: {len(study_units):,}")
        print(f"  sequence breaks: {sequence_breaks(study_units)}")
        print("  examples:")
        print_units(study_units)
        if study_units:
            print(f"  span coverage: u{study_units[0].start}-u{study_units[-1].end}")


if __name__ == "__main__":
    main()
