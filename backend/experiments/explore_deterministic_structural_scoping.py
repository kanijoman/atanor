"""Explore deterministic structural scoping for knowledge extraction.

This experiment tests whether simple document structure can disambiguate a
selection process and its programme without using an LLM.

The heuristic is intentionally exploratory. It is not an application rule or
product contract.
"""

from dataclasses import dataclass
from pathlib import Path
import re

from pypdf import PdfReader


SAMPLES_DIR = Path("tests/samples")
TARGET_SAMPLE = "BOE-A-2024-14098.pdf"
PROCESS = "Cuerpo de Técnicos Auxiliares de Informática"
TOPIC = "La Constitución Española de 1978"

ANNEX_PATTERN = re.compile(r"^ANEXO\s+([IVXLCDM]+)$", re.IGNORECASE)
PROGRAMME_PATTERN = re.compile(r"^\d+\.\s*Programa\.?$", re.IGNORECASE)


@dataclass(frozen=True)
class TextUnit:
    page: int
    order: int
    text: str


@dataclass(frozen=True)
class StructuralCandidate:
    annex: TextUnit
    programme: TextUnit
    programme_end: int
    topic_matches: tuple[TextUnit, ...]


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


def find_enclosing_annex(
    annexes: list[TextUnit], unit: TextUnit
) -> TextUnit | None:
    previous = [annex for annex in annexes if annex.order <= unit.order]
    return previous[-1] if previous else None


def programme_span(
    units: list[TextUnit], programme: TextUnit, next_programme: TextUnit | None
) -> list[TextUnit]:
    start = next(index for index, unit in enumerate(units) if unit.order == programme.order)
    end = len(units)
    if next_programme is not None:
        end = next(index for index, unit in enumerate(units) if unit.order == next_programme.order)
    return units[start:end]


def structural_candidates(
    units: list[TextUnit], process_occurrences: list[TextUnit], topic: str
) -> list[StructuralCandidate]:
    annexes = find_annexes(units)
    programmes = find_programmes(units)
    candidates: list[StructuralCandidate] = []

    for process in process_occurrences:
        annex = find_enclosing_annex(annexes, process)
        if annex is None:
            continue

        programmes_in_annex = [programme for programme in programmes if programme.order > annex.order]
        next_annex = next((item for item in annexes if item.order > annex.order), None)
        if next_annex is not None:
            programmes_in_annex = [
                programme for programme in programmes_in_annex
                if programme.order < next_annex.order
            ]

        for index, programme in enumerate(programmes_in_annex):
            next_programme = programmes_in_annex[index + 1] if index + 1 < len(programmes_in_annex) else None
            span = programme_span(units, programme, next_programme)
            matches = tuple(find_occurrences(span, topic))
            candidates.append(
                StructuralCandidate(
                    annex=annex,
                    programme=programme,
                    programme_end=span[-1].order,
                    topic_matches=matches,
                )
            )

    return candidates


def print_context(units: list[TextUnit], matches: tuple[TextUnit, ...]) -> None:
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
    candidates = structural_candidates(units, process_occurrences, TOPIC)

    print("DETERMINISTIC STRUCTURAL SCOPING")
    print(f"  sample: {pdf_path.name}")
    print(f"  process: {PROCESS}")
    print(f"  topic: {TOPIC}")
    print(f"  total units: {len(units):,}")
    print(f"  process occurrences: {len(process_occurrences)}")
    print(f"  annexes: {len(find_annexes(units))}")
    print(f"  programmes: {len(find_programmes(units))}")

    print("\nSTRUCTURAL CANDIDATES")
    for candidate in candidates:
        print(
            f"  annex {candidate.annex.text} "
            f"[p{candidate.annex.page} u{candidate.annex.order}] -> "
            f"{candidate.programme.text} "
            f"[p{candidate.programme.page} u{candidate.programme.order}] -> "
            f"end u{candidate.programme_end} -> "
            f"topic matches: {len(candidate.topic_matches)}"
        )

    selected = next((candidate for candidate in candidates if candidate.topic_matches), None)

    print("\nSELECTION")
    if selected is None:
        print("  no structural candidate contains the topic")
    else:
        print(f"  annex: {selected.annex.text}")
        print(f"  programme: {selected.programme.text}")
        print(f"  topic matches: {len(selected.topic_matches)}")

        print("\nSELECTED MATCH CONTEXT")
        print_context(units, selected.topic_matches)

    global_matches = find_occurrences(units, TOPIC)
    scoped_matches = selected.topic_matches if selected else ()
    print("\nBASELINE COMPARISON")
    print(f"  global matches: {len(global_matches)}")
    print(f"  structural matches: {len(scoped_matches)}")
    print(f"  global matched characters: {sum(len(unit.text) for unit in global_matches):,}")
    print(f"  structural matched characters: {sum(len(unit.text) for unit in scoped_matches):,}")


if __name__ == "__main__":
    main()
