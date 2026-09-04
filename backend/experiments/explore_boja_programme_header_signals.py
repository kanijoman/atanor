"""Explore deterministic signals for BOJA programme headers.

This experiment stays outside the application layer. It inspects candidate
headers and their local surroundings without attempting programme selection.
The goal is to identify observable structural signals that distinguish
programme headers from ordinary content.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


SAMPLE = "BOJA24-138-00046-48048-01_00304998.pdf"
CONTEXT_UNITS = 3
HEADER_PATTERN = re.compile(
    r"^(?P<section>[IVXLCDM]+(?:\.[A-Z0-9]+)*)\.\s+"
    r"(?P<title>.*\bPROGRAMA\b.*)$",
    re.IGNORECASE,
)
TEMA_PATTERN = re.compile(r"^Tema\s+(\d+)(?:\s*[.\-–—])\s*(.*)$", re.IGNORECASE)


@dataclass(frozen=True)
class TextUnit:
    page: int
    order: int
    text: str


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


def find_headers(units: list[TextUnit]) -> list[TextUnit]:
    return [unit for unit in units if HEADER_PATTERN.fullmatch(unit.text)]


def nearby_temas(units: list[TextUnit], header: TextUnit) -> tuple[TextUnit, ...]:
    start = header.order
    end = min(len(units), header.order + 25)
    return tuple(
        unit for unit in units[start:end]
        if TEMA_PATTERN.fullmatch(unit.text)
    )


def print_header(units: list[TextUnit], header: TextUnit) -> None:
    start = max(0, header.order - 1 - CONTEXT_UNITS)
    end = min(len(units), header.order + CONTEXT_UNITS)
    local = units[start:end]
    match = HEADER_PATTERN.fullmatch(header.text)
    section = match.group("section") if match else "?"
    title = match.group("title") if match else header.text
    temas = nearby_temas(units, header)

    print(f"  header: u{header.order} p{header.page}")
    print(f"    section: {section}")
    print(f"    title: {title}")
    print(f"    text length: {len(header.text)}")
    print(f"    local context: u{local[0].order}-u{local[-1].order}")
    print(f"    following Tema markers (next 25 units): {len(temas)}")
    if temas:
        print(
            "    first Tema: "
            f"u{temas[0].order} -> {temas[0].text}"
        )
    if len(temas) > 1:
        print(
            "    last Tema: "
            f"u{temas[-1].order} -> {temas[-1].text}"
        )
    print("    surrounding units:")
    for unit in local:
        marker = " <-- HEADER" if unit.order == header.order else ""
        print(f"      u{unit.order} p{unit.page}: {unit.text}{marker}")


def main() -> None:
    samples_dir = Path(__file__).resolve().parents[1] / "tests" / "samples"
    units = extract_units(samples_dir / SAMPLE)
    headers = find_headers(units)

    print("BOJA PROGRAMME HEADER SIGNALS")
    print("  purpose: identify deterministic signals distinguishing programme headers")
    print(f"  document: {SAMPLE}")
    print(f"  text units: {len(units):,}")
    print(f"  programme headers: {len(headers)}")
    print()

    for index, header in enumerate(headers, start=1):
        print(f"HEADER {index}")
        print_header(units, header)
        print()


if __name__ == "__main__":
    main()
