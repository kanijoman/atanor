"""Explore deterministic programme-unit signals across sample documents.

This experiment does not implement a parser. It inventories candidate study-unit
markers and their local context to determine whether programme units can be
recognized deterministically despite different document structures.
"""

from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader


SAMPLES = (
    "BOE-A-2024-14098.pdf",
    "BOJA24-138-00046-48048-01_00304998.pdf",
    "Programa_Archiveros_0.pdf",
)

PATTERNS = {
    "topic": re.compile(r"^Tema\s+\d+(?:\s*[.\-–—])", re.IGNORECASE),
    "item": re.compile(r"^\d+[.)]\s+\S+"),
    "subitem": re.compile(r"^\d+\.\d+(?:\.\d+)*[.)]?\s+\S+"),
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


def print_examples(matches: list[tuple[int, int, str]], limit: int = 20) -> None:
    for page, order, text in matches[:limit]:
        print(f"    [p{page} u{order}] {text}")
    if len(matches) > limit:
        print(f"    ... {len(matches) - limit} more")


def print_topic_spans(units: list[tuple[int, int, str]], matches: list[tuple[int, int, str]]) -> None:
    if not matches:
        return
    positions = {order: index for index, (_, order, _) in enumerate(units)}
    print("  topic candidate spans:")
    for index, (page, order, text) in enumerate(matches[:20], start=1):
        start = positions[order]
        next_orders = [candidate_order for _, candidate_order, _ in matches if candidate_order > order]
        end = positions[next_orders[0]] if next_orders else len(units)
        span = units[start:end]
        print(
            f"    #{index} [p{page} u{order}] -> "
            f"u{span[0][1]}-u{span[-1][1]} ({len(span)} units)"
        )
        print(f"      start: {text}")
        if len(span) > 1:
            print(f"      next:  {span[1][2]}")


def main() -> None:
    samples_dir = Path(__file__).resolve().parents[1] / "tests" / "samples"

    print("PROGRAMME UNIT SIGNALS")
    print("  samples: BOE + BOJA + Archiveros")
    print("  purpose: identify deterministic study-unit markers")

    for sample in SAMPLES:
        units = extract_units(samples_dir / sample)
        print()
        print(f"DOCUMENT: {sample}")
        print(f"  text units: {len(units)}")
        if not units:
            print("  status: no_extractable_text")
            continue

        for name, pattern in PATTERNS.items():
            matches = matching_units(units, pattern)
            print(f"  {name}: {len(matches)}")
            print_examples(matches)
            if name == "topic":
                print_topic_spans(units, matches)


if __name__ == "__main__":
    main()
