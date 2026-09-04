"""Explore deterministic structural scoping for knowledge extraction.

This experiment tests whether a simple structural hierarchy can disambiguate a
study topic without relying on linear proximity or an LLM.

The heuristic is intentionally exploratory and document-oriented: it uses
annexes and programme headings as structural anchors, but does not introduce
those concepts into the application domain model or product contract.
"""

from dataclasses import dataclass
from pathlib import Path
import re

from pypdf import PdfReader


SAMPLES_DIR = Path("tests/samples")
TARGET_SAMPLE = "BOE-A-2024-14098.pdf"
PROCESS = "Cuerpo de Técnicos Auxiliares de Informática"
TOPIC = "La Constitución Española de 1978"

ANNEX_PATTERN = re.compile(r"^ANEXO\s+[IVXLCDM]+$", re.IGNORECASE)
PROGRAMME_PATTERN = re.compile(r"^\d+\.\s*Programa\.?$", re.IGNORECASE)


@dataclass(frozen=True)
class TextUnit:
    page: int
    order: int
    text: str


@dataclass(frozen=True)
class StructuralCandidate:
    process_occurrence: TextUnit
    annex: TextUnit
    programme: TextUnit
    distance: int


def extract_units(pdf_path: Path) -> list[TextUnit]:
    reader = PdfReader(pdf_path)
    units: list[TextUnit] = []
    order = 0

    for page_number, page in enumerate(reader.pages, start=1):
        for line in (page.extract_text() or "").splitlines():
            value = " ".join(line.split())
            if not value:
                continue
            order += 1
            units.append(TextUnit(page_number, order, value))

    return units


def normalise(value: str) -> str:
    return " ".join(value.casefold().split())


def find_occurrences(units: list[TextUnit], phrase: str) -> list[TextUnit]:
    target = normalise(phrase)
    return [unit for unit in units if target in normalise(unit.text)]


def find_annexes(units: list[TextUnit]) -> list[TextUnit]:
    return [unit for unit in units if ANNEX_PATTERN.fullmatch(unit.text)]


def find_programmes(units: list[TextUnit]) -> list[TextUnit]:
    return [unit for unit in units if PROGRAMME_PATTERN.fullmatch(unit.text)]


def annex_for_unit(unit: TextUnit, annexes: list[TextUnit]) -> TextUnit | None:
    previous = [annex for annex in annexes if annex.order <= unit.order]
    return previous[-1] if previous else None


def next_annex(unit: TextUnit, annexes: list[TextUnit]) -> TextUnit | None:
    following = [annex for annex in annexes if annex.order > unit.order]
    return following[0] if following else None


def programmes_in_annex(
    annex: TextUnit, annexes: list[TextUnit], programmes: list[TextUnit]
) -> list[TextUnit]:
    end_annex = next_annex(annex, annexes)
    end_order = end_annex.order if end_annex else float("inf")
    return [
        programme
        for programme in programmes
        if annex.order <= programme.order < end_order
    ]


def build_structural_candidates(
    process_occurrences: list[TextUnit],
    annexes: list[TextUnit],
    programmes: list[TextUnit],
) -> list[StructuralCandidate]:
    candidates: list[StructuralCandidate] = []

    for occurrence in process_occurrences:
        annex = annex_for_unit(occurrence, annexes)
        if annex is None:
            continue

        programmes_in_scope = programmes_in_annex(annex, annexes, programmes)
        following_programmes = [
            programme for programme in programmes_in_scope if programme.order >= occurrence.order
        ]
        if not following_programmes:
            continue

        programme = min(
            following_programmes,
            key=lambda candidate: candidate.order - occurrence.order,
        )
        candidates.append(
            StructuralCandidate(
                process_occurrence=occurrence,
                annex=annex,
                programme=programme,
                distance=programme.order - occurrence.order,
            )
        )

    return candidates


def programme_span(
    units: list[TextUnit], programme: TextUnit, annexes: list[TextUnit]
) -> list[TextUnit]:
    start = next(index for index, unit in enumerate(units) if unit.order == programme.order)
    end = len(units)

    for index in range(start + 1, len(units)):
        unit = units[index]
        if PROGRAMME_PATTERN.fullmatch(unit.text) or ANNEX_PATTERN.fullmatch(unit.text):
            end = index
            break

    return units[start:end]


def topic_matches(units: list[TextUnit], topic: str) -> list[TextUnit]:
    target = normalise(topic)
    return [unit for unit in units if target in normalise(unit.text)]


def print_context(units: list[TextUnit], center: TextUnit, radius: int = 2) -> None:
    index = next(index for index, unit in enumerate(units) if unit.order == center.order)
    start = max(0, index - radius)
    end = min(len(units), index + radius + 1)
    for unit in units[start:end]:
        marker = " <-" if unit.order == center.order else ""
        print(f"    [p{unit.page} u{unit.order}] {unit.text}{marker}")


def main() -> None:
    pdf_path = SAMPLES_DIR / TARGET_SAMPLE
    if not pdf_path.exists():
        raise FileNotFoundError(f"Sample not found: {pdf_path}")

    units = extract_units(pdf_path)
    process_occurrences = find_occurrences(units, PROCESS)
    annexes = find_annexes(units)
    programmes = find_programmes(units)
    candidates = build_structural_candidates(process_occurrences, annexes, programmes)

    if not candidates:
        raise RuntimeError("No structural candidate could be built for the process")

    selected = min(candidates, key=lambda candidate: candidate.distance)
    scoped_units = programme_span(units, selected.programme, annexes)

    global_matches = topic_matches(units, TOPIC)
    scoped_matches = topic_matches(scoped_units, TOPIC)

    print("DETERMINISTIC STRUCTURAL SCOPING")
    print(f"  sample: {pdf_path.name}")
    print(f"  process: {PROCESS}")
    print(f"  topic: {TOPIC}")
    print(f"  total units: {len(units):,}")
    print(f"  process occurrences: {len(process_occurrences)}")
    print(f"  annexes: {len(annexes)}")
    print(f"  programme candidates: {len(programmes)}")

    print("\nPROCESS STRUCTURAL CONTEXT")
    for occurrence in process_occurrences:
        annex = annex_for_unit(occurrence, annexes)
        annex_label = annex.text if annex else "<front matter>"
        print(f"  [p{occurrence.page} u{occurrence.order}] {occurrence.text}")
        print(f"    enclosing annex: {annex_label}")

    print("\nSTRUCTURAL CANDIDATES")
    for candidate in candidates:
        print(
            f"  [p{candidate.process_occurrence.page} u{candidate.process_occurrence.order}] "
            f"{candidate.annex.text} -> "
            f"[p{candidate.programme.page} u{candidate.programme.order}] "
            f"{candidate.programme.text} ({candidate.distance} units)"
        )

    print("\nSELECTED STRUCTURAL SCOPE")
    print(
        f"  process occurrence: p{selected.process_occurrence.page} "
        f"u{selected.process_occurrence.order}"
    )
    print(f"  annex: {selected.annex.text}")
    print(
        f"  programme: p{selected.programme.page} "
        f"u{selected.programme.order} {selected.programme.text}"
    )
    print(f"  scoped programme units: {len(scoped_units):,}")
    print(f"  scoped range: u{scoped_units[0].order}-u{scoped_units[-1].order}")

    print("\nTOPIC MATCH COMPARISON")
    print(f"  global matches: {len(global_matches)}")
    print(f"  scoped matches: {len(scoped_matches)}")
    print(
        f"  global matched characters: "
        f"{sum(len(unit.text) for unit in global_matches):,}"
    )
    print(
        f"  scoped matched characters: "
        f"{sum(len(unit.text) for unit in scoped_matches):,}"
    )

    print("\nSELECTED PROGRAMME CONTEXT")
    print_context(units, selected.programme)

    print("\nSCOPED MATCH CONTEXT")
    if scoped_matches:
        for match in scoped_matches:
            print(f"  match u{match.order} p{match.page}:")
            print_context(scoped_units, match)
    else:
        print("  no scoped topic matches")

    print("\nBASELINE COMPARISON")
    print("  global: literal topic search across the whole document")
    print("  proximity: nearest programme after nearest process occurrence")
    print("  structure: process occurrence -> enclosing annex -> programme")


if __name__ == "__main__":
    main()
