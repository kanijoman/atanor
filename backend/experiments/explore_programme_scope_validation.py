"""Validate deterministic programme scopes and study-unit extraction quality.

This experiment stays outside the application layer. It checks whether extracted
programme scopes and study units are structurally coherent and traceable. The
validation rules are exploratory and must not become product contracts.
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


def process_is_in_opening(units: list[TextUnit], annex: Annex, opening_size: int = 8) -> bool:
    opening = units[annex.start - 1 : min(annex.end, annex.start + opening_size - 1)]
    return any(PROCESS_PATTERN.search(unit.text) for unit in opening)


def find_programme(units: list[TextUnit], annex: Annex) -> TextUnit | None:
    for unit in units[annex.start - 1 : annex.end]:
        if PROGRAMME_PATTERN.fullmatch(unit.text):
            return unit
    return None


def extract_boe_units(units: list[TextUnit], annex: Annex) -> tuple[TextUnit | None, list[StudyUnit]]:
    programme = find_programme(units, annex)
    if programme is None:
        return None, []

    scoped = units[programme.order - 1 : annex.end]
    sections = [
        (match.group(1).upper(), unit.order)
        for unit in scoped
        if (match := ROMAN_PATTERN.fullmatch(unit.text))
    ]
    candidates = [
        unit
        for unit in scoped
        if ITEM_PATTERN.fullmatch(unit.text)
        and not PROGRAMME_PATTERN.fullmatch(unit.text)
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
        boundaries = [candidate.order for candidate in (next_item,) if candidate is not None]
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
    return programme, result


def extract_tema_units(units: list[TextUnit]) -> list[StudyUnit]:
    candidates = [unit for unit in units if TEMA_PATTERN.fullmatch(unit.text)]
    result: list[StudyUnit] = []
    for index, unit in enumerate(candidates):
        match = TEMA_PATTERN.fullmatch(unit.text)
        assert match is not None
        next_tema = candidates[index + 1] if index + 1 < len(candidates) else None
        end = next_tema.order - 1 if next_tema else units[-1].order
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


def validate_units(units: list[StudyUnit]) -> dict[str, int | str]:
    if not units:
        return {"status": "no_units"}

    nonempty_titles = sum(bool(unit.title) for unit in units)
    monotonic = all(
        current.start > previous.start and current.end >= current.start
        for previous, current in zip(units, units[1:])
    )
    non_overlapping = all(
        current.start > previous.end
        for previous, current in zip(units, units[1:])
    )
    page_monotonic = all(
        current.page >= previous.page
        for previous, current in zip(units, units[1:])
    )

    sequence_breaks = 0
    for previous, current in zip(units, units[1:]):
        if current.section == previous.section and current.number != previous.number + 1:
            sequence_breaks += 1
        if current.section != previous.section and current.number != 1:
            sequence_breaks += 1

    return {
        "status": "coherent"
        if nonempty_titles == len(units)
        and monotonic
        and non_overlapping
        and page_monotonic
        and sequence_breaks == 0
        else "needs_review",
        "nonempty_titles": nonempty_titles,
        "monotonic_spans": int(monotonic),
        "non_overlapping_spans": int(non_overlapping),
        "monotonic_pages": int(page_monotonic),
        "sequence_breaks": sequence_breaks,
    }


def print_examples(units: list[StudyUnit], limit: int = 5) -> None:
    for unit in units[:limit]:
        section = f" [{unit.section}]" if unit.section else ""
        print(
            f"    {unit.marker} {unit.number}{section}: "
            f"u{unit.start}-u{unit.end} p{unit.page} | {unit.title}"
        )


def main() -> None:
    samples_dir = Path(__file__).resolve().parents[1] / "tests" / "samples"

    print("PROGRAMME SCOPE VALIDATION")
    print("  purpose: validate deterministic scope and study-unit coherence")
    print("  validation: titles + spans + pages + numbering + traceability")

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
                ),
                None,
            )
            if target_annex is None:
                print("  scope status: process_not_found")
                continue

            programme, study_units = extract_boe_units(units, target_annex)
            validation = validate_units(study_units)
            print(f"  process: {TARGET_PROCESS}")
            print(f"  scope: ANEXO {target_annex.name}")
            print(f"  programme marker: u{programme.order}" if programme else "  programme marker: none")
            print(f"  study units: {len(study_units):,}")
            print(f"  scope span: u{programme.order}-{target_annex.end}" if programme else "  scope span: none")
            print(f"  validation status: {validation['status']}")
            for key, value in validation.items():
                if key != "status":
                    print(f"  {key}: {value}")
            print("  examples:")
            print_examples(study_units)
            continue

        study_units = extract_tema_units(units)
        validation = validate_units(study_units)
        first = study_units[0] if study_units else None
        last = study_units[-1] if study_units else None
        print("  scope strategy: first Tema marker through last Tema span")
        print(f"  study units: {len(study_units):,}")
        print(
            f"  scope span: u{first.start}-u{last.end}"
            if first and last
            else "  scope span: none"
        )
        print(f"  validation status: {validation['status']}")
        for key, value in validation.items():
            if key != "status":
                print(f"  {key}: {value}")
        print("  examples:")
        print_examples(study_units)


if __name__ == "__main__":
    main()
