"""Explore deterministic context scoping for knowledge extraction.

This experiment tests whether simple document context can disambiguate a topic
that appears in several selection-process programmes, without using an LLM.

It is intentionally exploratory: none of the heuristics here are application
rules or product contracts.
"""

from dataclasses import dataclass
from pathlib import Path
import re

from pypdf import PdfReader


SAMPLES_DIR = Path("tests/samples")
TARGET_SAMPLE = "BOE-A-2024-14098.pdf"
PROCESS = "Cuerpo de Técnicos Auxiliares de Informática"
TOPIC = "La Constitución Española de 1978"

PROGRAMME_PATTERN = re.compile(r"^\d+\.\s*Programa\.?$", re.IGNORECASE)


@dataclass(frozen=True)
class TextUnit:
    page: int
    order: int
    text: str


@dataclass(frozen=True)
class ProgrammeCandidate:
    heading: TextUnit
    process_distance: int


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


def find_programme_candidates(
    units: list[TextUnit], process_occurrences: list[TextUnit]
) -> list[ProgrammeCandidate]:
    candidates: list[ProgrammeCandidate] = []

    for unit in units:
        if not PROGRAMME_PATTERN.fullmatch(unit.text):
            continue

        previous_processes = [
            process for process in process_occurrences if process.order <= unit.order
        ]
        if not previous_processes:
            continue

        process = previous_processes[-1]
        candidates.append(
            ProgrammeCandidate(
                heading=unit,
                process_distance=unit.order - process.order,
            )
        )

    return candidates


def select_programme(candidates: list[ProgrammeCandidate]) -> ProgrammeCandidate:
    if not candidates:
        raise RuntimeError("No programme candidate could be associated with the process")
    return min(candidates, key=lambda candidate: candidate.process_distance)


def programme_span(units: list[TextUnit], heading: TextUnit) -> list[TextUnit]:
    start = next(index for index, unit in enumerate(units) if unit.order == heading.order)
    end = len(units)

    for index in range(start + 1, len(units)):
        if PROGRAMME_PATTERN.fullmatch(units[index].text):
            end = index
            break

    return units[start:end]


def topic_matches(units: list[TextUnit], topic: str) -> list[TextUnit]:
    target = normalise(topic)
    return [unit for unit in units if target in normalise(unit.text)]


def print_match_context(units: list[TextUnit], matches: list[TextUnit]) -> None:
    indexes = {unit.order: index for index, unit in enumerate(units)}
    for match in matches:
        index = indexes[match.order]
        start = max(0, index - 2)
        end = min(len(units), index + 3)
        print(f"  match u{match.order} p{match.page}:")
        for unit in units[start:end]:
            print(f"    [p{unit.page} u{unit.order}] {unit.text}")


def main() -> None:
    pdf_path = SAMPLES_DIR / TARGET_SAMPLE
    if not pdf_path.exists():
        raise FileNotFoundError(f"Sample not found: {pdf_path}")

    units = extract_units(pdf_path)
    process_occurrences = find_occurrences(units, PROCESS)
    candidates = find_programme_candidates(units, process_occurrences)
    selected = select_programme(candidates)
    scoped_units = programme_span(units, selected.heading)

    global_matches = topic_matches(units, TOPIC)
    scoped_matches = topic_matches(scoped_units, TOPIC)

    print("DETERMINISTIC CONTEXT SCOPING")
    print(f"  sample: {pdf_path.name}")
    print(f"  process: {PROCESS}")
    print(f"  topic: {TOPIC}")
    print(f"  total units: {len(units):,}")
    print(f"  process occurrences: {len(process_occurrences)}")
    print(f"  programme candidates: {len(candidates)}")
    print("  programme candidates:")
    for candidate in candidates:
        print(
            f"    [p{candidate.heading.page} u{candidate.heading.order}] "
            f"{candidate.heading.text} <- {candidate.process_distance} units"
        )

    print("  selected programme:")
    print(
        f"    [p{selected.heading.page} u{selected.heading.order}] "
        f"{selected.heading.text}"
    )
    print(f"  selected programme units: {len(scoped_units):,}")
    print(
        f"  selected programme range: "
        f"u{scoped_units[0].order}-u{scoped_units[-1].order}"
    )

    print("\nTOPIC MATCH COMPARISON")
    print(f"  global matches: {len(global_matches)}")
    print(f"  scoped matches: {len(scoped_matches)}")

    print("\nSCOPED MATCH CONTEXT")
    print_match_context(scoped_units, scoped_matches)

    print("\nBASELINE COMPARISON")
    print(f"  global matched characters: {sum(len(unit.text) for unit in global_matches):,}")
    print(f"  scoped matched characters: {sum(len(unit.text) for unit in scoped_matches):,}")


if __name__ == "__main__":
    main()
