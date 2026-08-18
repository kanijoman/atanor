from dataclasses import dataclass
from pathlib import Path
import re

from pypdf import PdfReader

from app.application.pdf_extraction import extract_pdf_text
from app.application.source import import_pdf_source


SAMPLES = [
    ("BOE", Path("tests/samples/BOE-A-2024-14098.pdf")),
    ("BOJA", Path("tests/samples/BOJA24-138-00046-48048-01_00304998.pdf")),
    ("Programa Archiveros", Path("tests/samples/Programa_Archiveros_0.pdf")),
    ("Ayuntamiento de León", Path("tests/samples/OPOS_AYTO_LEON_INFORMATICA_B.pdf")),
]

MAX_UNITS = 40

UNIT_PATTERN = re.compile(
    r"^(?P<marker>(?:Tema\s+\d+|\d+(?:\.\d+)*[.)]?|[IVXLCDM]+(?:\.\d+)*[.)]?))\s+(?P<title>.+)$",
    re.IGNORECASE,
)
PARENT_PATTERN = re.compile(
    r"^(?:[IVXLCDM]+(?:\.\d+)*[.)]?|[A-Z](?:\.\d+)*[.)]?)\s+.+$",
    re.IGNORECASE,
)
PROGRAMME_PATTERN = re.compile(r"\bprograma(?:\s+de\s+materias)?\b", re.IGNORECASE)


@dataclass(frozen=True)
class KnowledgeUnitCandidate:
    line_number: int
    marker: str
    title: str
    parent: str | None
    continuation: tuple[str, ...]


class _InMemorySourceRepository:
    def save(self, source):
        return source


def _is_programme_marker(line: str) -> bool:
    return bool(PROGRAMME_PATTERN.search(line))


def _is_parent_candidate(line: str) -> bool:
    if _is_programme_marker(line):
        return True
    return bool(PARENT_PATTERN.match(line))


def _extract_units(lines: list[str]) -> list[KnowledgeUnitCandidate]:
    candidates: list[KnowledgeUnitCandidate] = []
    current_parent: str | None = None

    for index, line in enumerate(lines):
        match = UNIT_PATTERN.match(line)
        if not match:
            if _is_parent_candidate(line) and len(line) <= 180:
                current_parent = line
            continue

        title = match.group("title").strip()
        continuation: list[str] = []
        next_index = index + 1
        while next_index < len(lines):
            next_line = lines[next_index]
            if UNIT_PATTERN.match(next_line) or _is_parent_candidate(next_line):
                break
            continuation.append(next_line)
            next_index += 1

        candidates.append(
            KnowledgeUnitCandidate(
                line_number=index + 1,
                marker=match.group("marker"),
                title=title,
                parent=current_parent,
                continuation=tuple(continuation),
            )
        )

        if len(candidates) >= MAX_UNITS:
            break

    return candidates


def _print_units(units: list[KnowledgeUnitCandidate]) -> None:
    print(f"\nKnowledge unit candidates: {len(units)} shown (max {MAX_UNITS})")
    for number, unit in enumerate(units, start=1):
        print(f"\n  [{number}] line {unit.line_number}: {unit.marker}")
        print(f"      title: {unit.title}")
        print(f"      parent: {unit.parent or '<none>'}")
        if unit.continuation:
            print(f"      continuation lines: {len(unit.continuation)}")
            for continuation in unit.continuation[:2]:
                print(f"        + {continuation}")
            if len(unit.continuation) > 2:
                print(f"        + ... {len(unit.continuation) - 2} more")


def _print_marker_summary(lines: list[str]) -> None:
    numbered = sum(bool(UNIT_PATTERN.match(line)) for line in lines)
    programmes = sum(bool(PROGRAMME_PATTERN.search(line)) for line in lines)
    parents = sum(_is_parent_candidate(line) for line in lines)
    print("\nStructural marker summary:")
    print(f"  programme markers: {programmes}")
    print(f"  unit markers: {numbered}")
    print(f"  parent-like markers: {parents}")


def inspect_document(name: str, path: Path) -> None:
    source = import_pdf_source(path, _InMemorySourceRepository())
    text = extract_pdf_text(source)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    pages = len(PdfReader(path).pages)

    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)
    print(f"File: {path}")
    print(f"Pages: {pages}")
    print(f"Characters: {len(text)}")
    print(f"Non-empty lines: {len(lines)}")

    if len(lines) < 2:
        print("Extraction status: IMAGE_ONLY_OR_EMPTY")
        print("Structural analysis: SKIPPED")
        print("Reason: no meaningful text was extracted from the PDF.")
        return

    print("Extraction status: TEXT")
    _print_marker_summary(lines)
    _print_units(_extract_units(lines))


def main() -> None:
    for name, path in SAMPLES:
        inspect_document(name, path)


if __name__ == "__main__":
    main()
