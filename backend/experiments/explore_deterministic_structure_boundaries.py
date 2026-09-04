"""Explore deterministic document structure boundaries.

This experiment tests whether generic structural signals can correctly delimit
annexes and programmes before attempting to select a specific study process.

The heuristic is intentionally exploratory. It is not an application rule or
product contract.
"""

from dataclasses import dataclass
from pathlib import Path
import re

from pypdf import PdfReader


SAMPLES_DIR = Path("tests/samples")
TARGET_SAMPLE = "BOE-A-2024-14098.pdf"
TOPIC = "La Constitución Española de 1978"

ANNEX_PATTERN = re.compile(r"^ANEXO\s+([IVXLCDM]+)$", re.IGNORECASE)
PROGRAMME_PATTERN = re.compile(r"^\d+\.\s*Programa\.?$", re.IGNORECASE)


@dataclass(frozen=True)
class TextUnit:
    page: int
    order: int
    text: str


@dataclass(frozen=True)
class ProgrammeBoundary:
    start: TextUnit
    end: int
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


def programme_boundaries(
    units: list[TextUnit], annex: TextUnit, next_annex: TextUnit | None
) -> list[ProgrammeBoundary]:
    programmes = [unit for unit in find_programmes(units) if unit.order > annex.order]
    if next_annex is not None:
        programmes = [unit for unit in programmes if unit.order < next_annex.order]

    boundaries: list[ProgrammeBoundary] = []
    for index, programme in enumerate(programmes):
        next_programme = programmes[index + 1] if index + 1 < len(programmes) else None
        end = next_programme.order - 1 if next_programme else (
            next_annex.order - 1 if next_annex else units[-1].order
        )
        span = [unit for unit in units if programme.order <= unit.order <= end]
        boundaries.append(
            ProgrammeBoundary(
                start=programme,
                end=end,
                topic_matches=tuple(find_occurrences(span, TOPIC)),
            )
        )
    return boundaries


def main() -> None:
    pdf_path = SAMPLES_DIR / TARGET_SAMPLE
    if not pdf_path.exists():
        raise FileNotFoundError(f"Sample not found: {pdf_path}")

    units = extract_units(pdf_path)
    annexes = find_annexes(units)
    programmes = find_programmes(units)

    print("DETERMINISTIC STRUCTURE BOUNDARIES")
    print(f"  sample: {pdf_path.name}")
    print(f"  topic: {TOPIC}")
    print(f"  total units: {len(units):,}")
    print(f"  annexes: {len(annexes)}")
    print(f"  programmes: {len(programmes)}")

    print("\nANNEX / PROGRAMME BOUNDARIES")
    for index, annex in enumerate(annexes):
        next_annex = annexes[index + 1] if index + 1 < len(annexes) else None
        annex_end = next_annex.order - 1 if next_annex else units[-1].order
        boundaries = programme_boundaries(units, annex, next_annex)

        print(
            f"  {annex.text} [p{annex.page} u{annex.order}] "
            f"range: u{annex.order}-u{annex_end} "
            f"programmes: {len(boundaries)}"
        )
        for boundary in boundaries:
            print(
                f"    programme: {boundary.start.text} "
                f"[p{boundary.start.page} u{boundary.start.order}] "
                f"range: u{boundary.start.order}-u{boundary.end} "
                f"topic matches: {len(boundary.topic_matches)}"
            )

    print("\nTOPIC MATCHES BY PROGRAMME")
    for index, annex in enumerate(annexes):
        next_annex = annexes[index + 1] if index + 1 < len(annexes) else None
        for boundary in programme_boundaries(units, annex, next_annex):
            print(
                f"  {annex.text} -> {boundary.start.text}: "
                f"{len(boundary.topic_matches)}"
            )


if __name__ == "__main__":
    main()
