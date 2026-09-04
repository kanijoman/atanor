"""Compare deterministic structure boundaries across the sample documents.

This experiment applies the same structural signals to every available sample
PDF. It measures whether annex and programme boundaries generalise beyond the
BOE sample used by AT-064.

The heuristic is intentionally exploratory. It is not an application rule or
product contract.
"""

from dataclasses import dataclass
from pathlib import Path
import re

from pypdf import PdfReader


SAMPLES_DIR = Path("tests/samples")

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
        boundaries.append(ProgrammeBoundary(start=programme, end=end))
    return boundaries


def print_document_summary(pdf_path: Path, units: list[TextUnit]) -> None:
    annexes = find_annexes(units)
    programmes = find_programmes(units)

    print(f"\nDOCUMENT: {pdf_path.name}")
    print(f"  pages: {len(PdfReader(pdf_path).pages)}")
    print(f"  text units: {len(units):,}")

    if not units:
        print("  status: no_extractable_text")
        return

    print(f"  annexes: {len(annexes)}")
    print(f"  programmes: {len(programmes)}")

    if not annexes:
        print("  status: no_annex_structure_detected")
        if programmes:
            print("  programme candidates outside annexes:")
            for programme in programmes:
                print(
                    f"    {programme.text} [p{programme.page} u{programme.order}]"
                )
        return

    print("  status: annex_structure_detected")
    print("  boundaries:")
    for index, annex in enumerate(annexes):
        next_annex = annexes[index + 1] if index + 1 < len(annexes) else None
        annex_end = next_annex.order - 1 if next_annex else units[-1].order
        boundaries = programme_boundaries(units, annex, next_annex)
        print(
            f"    {annex.text}: u{annex.order}-u{annex_end}, "
            f"programmes: {len(boundaries)}"
        )
        for boundary in boundaries:
            print(
                f"      {boundary.start.text}: "
                f"u{boundary.start.order}-u{boundary.end}"
            )


def main() -> None:
    samples = sorted(SAMPLES_DIR.glob("*.pdf"))
    if not samples:
        raise FileNotFoundError(f"No PDF samples found in {SAMPLES_DIR}")

    print("CROSS-DOCUMENT STRUCTURE BOUNDARIES")
    print(f"  samples: {len(samples)}")
    print("  structural signals: ANEXO + numbered Programa")

    for pdf_path in samples:
        units = extract_units(pdf_path)
        print_document_summary(pdf_path, units)


if __name__ == "__main__":
    main()
