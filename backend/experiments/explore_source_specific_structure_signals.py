"""Explore deterministic structural signals across non-BOE sample documents.

This experiment deliberately does not implement a parser. It inventories simple,
source-agnostic textual signals so we can distinguish missing generic heuristics
from genuinely different document structures.
"""

from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader


SAMPLES = (
    "BOJA24-138-00046-48048-01_00304998.pdf",
    "Programa_Archiveros_0.pdf",
)

SIGNALS = {
    "annex": re.compile(r"^ANEXO(?:\s+[IVXLCDM]+)?$", re.IGNORECASE),
    "programme": re.compile(
        r"^(?:\d+\.\s*)?(?:PROGRAMA|TEMARIO|CONTENIDO)\.?$",
        re.IGNORECASE,
    ),
    "decimal": re.compile(r"^\d+(?:\.\d+)*[.)]?\s+\S+"),
    "roman": re.compile(r"^[IVXLCDM]+[.)]?\s+\S+", re.IGNORECASE),
    "letter": re.compile(r"^[a-z][.)]\s+\S+", re.IGNORECASE),
}


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


def matching_units(units: list[tuple[int, int, str]], pattern: re.Pattern[str]):
    return [(page, order, text) for page, order, text in units if pattern.match(text)]


def print_examples(name: str, matches: list[tuple[int, int, str]], limit: int = 12) -> None:
    print(f"  {name}: {len(matches)}")
    for page, order, text in matches[:limit]:
        print(f"    [p{page} u{order}] {text}")
    if len(matches) > limit:
        print(f"    ... {len(matches) - limit} more")


def main() -> None:
    samples_dir = Path(__file__).resolve().parents[1] / "tests" / "samples"

    print("SOURCE-SPECIFIC STRUCTURE SIGNALS")
    print("  samples: BOJA + Archiveros")
    print("  purpose: distinguish missing generic signals from different structures")

    for sample in SAMPLES:
        path = samples_dir / sample
        units = extract_units(path)
        print()
        print(f"DOCUMENT: {sample}")
        print(f"  text units: {len(units)}")
        if not units:
            print("  status: no_extractable_text")
            continue

        for name, pattern in SIGNALS.items():
            print_examples(name, matching_units(units, pattern))

        print("  first units:")
        for page, order, text in units[:8]:
            print(f"    [p{page} u{order}] {text}")

        print("  last units:")
        for page, order, text in units[-8:]:
            print(f"    [p{page} u{order}] {text}")


if __name__ == "__main__":
    main()
