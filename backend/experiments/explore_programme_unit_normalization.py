"""Explore a common representation for programme units across sample documents.

This experiment deliberately stays outside the application layer. It tests whether
heterogeneous programme markers can be normalized into a small common observation:
marker, label, start/end positions, and source provenance.
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

ANNEX_PATTERN = re.compile(r"^ANEXO\s+([IVXLCDM]+)$", re.IGNORECASE)
PROGRAMME_PATTERN = re.compile(r"^\d+\.\s*Programa\.?$", re.IGNORECASE)
TEMA_PATTERN = re.compile(r"^Tema\s+(\d+)(?:\s*[.\-–—])\s*(.*)$", re.IGNORECASE)
ITEM_PATTERN = re.compile(r"^(\d+)\.\s+(\S.*)$")


@dataclass(frozen=True)
class Unit:
    marker: str
    number: int
    title: str
    start_order: int
    end_order: int
    page: int


def extract_units(path: Path) -> list[tuple[int, int, str]]:
    reader = PdfReader(path)
    units: list[tuple[int, int, str]] = []
    order = 0
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for line in text.splitlines():
            normalized = " ".join(line.split())
            if not normalized:
                continue
            order += 1
            units.append((page_number, order, normalized))
    return units


def positions(units: list[tuple[int, int, str]]) -> dict[int, int]:
    return {order: index for index, (_, order, _) in enumerate(units)}


def find_annexes(units: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    return [item for item in units if ANNEX_PATTERN.match(item[2])]


def find_programmes(units: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    return [item for item in units if PROGRAMME_PATTERN.match(item[2])]


def programme_spans(
    units: list[tuple[int, int, str]],
) -> list[tuple[int, int, str, int]]:
    index_by_order = positions(units)
    programmes = find_programmes(units)
    annexes = find_annexes(units)
    spans: list[tuple[int, int, str, int]] = []

    for page, order, text in programmes:
        start = index_by_order[order]
        next_programmes = [item for item in programmes if item[1] > order]
        next_annexes = [item for item in annexes if item[1] > order]
        boundaries = next_programmes + next_annexes
        end = min((index_by_order[item[1]] for item in boundaries), default=len(units))
        spans.append((start, end, text, order))
    return spans


def normalize_tema_units(
    units: list[tuple[int, int, str]],
) -> list[Unit]:
    index_by_order = positions(units)
    matches = [item for item in units if TEMA_PATTERN.match(item[2])]
    result: list[Unit] = []
    for index, (page, order, text) in enumerate(matches):
        match = TEMA_PATTERN.match(text)
        assert match is not None
        number = int(match.group(1))
        title = match.group(2).strip()
        end = index_by_order[matches[index + 1][1]] if index + 1 < len(matches) else len(units)
        result.append(Unit("tema", number, title, order, units[end - 1][1], page))
    return result


def normalize_boe_units(
    units: list[tuple[int, int, str]],
) -> list[Unit]:
    index_by_order = positions(units)
    result: list[Unit] = []
    for start, end, _, _ in programme_spans(units):
        scoped = units[start:end]
        matches = [item for item in scoped if ITEM_PATTERN.match(item[2])]
        for index, (page, order, text) in enumerate(matches):
            match = ITEM_PATTERN.match(text)
            assert match is not None
            number = int(match.group(1))
            title = match.group(2).strip()
            if index + 1 < len(matches):
                unit_end = index_by_order[matches[index + 1][1]]
            else:
                unit_end = end
            result.append(Unit("item", number, title, order, units[unit_end - 1][1], page))
    return result


def print_units(units: list[Unit], limit: int = 12) -> None:
    for unit in units[:limit]:
        print(
            f"    {unit.marker} {unit.number}: "
            f"u{unit.start_order}-u{unit.end_order} p{unit.page} | {unit.title}"
        )
    if len(units) > limit:
        print(f"    ... {len(units) - limit} more")


def sequence_report(units: list[Unit]) -> tuple[int, int]:
    if not units:
        return 0, 0
    breaks = 0
    for previous, current in zip(units, units[1:]):
        if current.number != previous.number + 1:
            breaks += 1
    return len(units), breaks


def main() -> None:
    samples_dir = Path(__file__).resolve().parents[1] / "tests" / "samples"

    print("PROGRAMME UNIT NORMALIZATION")
    print("  samples: BOE + BOJA + Archiveros")
    print("  purpose: test a common study-unit observation across structures")
    print("  normalized fields: marker + number + title + span + page")

    for sample in SAMPLES:
        units = extract_units(samples_dir / sample)
        print()
        print(f"DOCUMENT: {sample}")
        print(f"  text units: {len(units)}")
        if not units:
            print("  status: no_extractable_text")
            continue

        if sample.startswith("BOE-"):
            programme_count = len(find_programmes(units))
            normalized = normalize_boe_units(units)
            print(f"  detected programme markers: {programme_count}")
            print("  normalization strategy: top-level numbered items inside programme spans")
        else:
            tema_count = len([item for item in units if TEMA_PATTERN.match(item[2])])
            normalized = normalize_tema_units(units)
            print(f"  detected Tema markers: {tema_count}")
            print("  normalization strategy: Tema N spans to next Tema marker")

        count, breaks = sequence_report(normalized)
        print(f"  normalized units: {count}")
        print(f"  sequence breaks: {breaks}")
        print("  examples:")
        print_units(normalized)

        if normalized:
            print(
                "  span coverage: "
                f"first=u{normalized[0].start_order}, "
                f"last=u{normalized[-1].end_order}"
            )


if __name__ == "__main__":
    main()
