from pathlib import Path
import re

from pypdf import PdfReader

from app.application.document_structure import analyze_document_structure
from app.application.pdf_extraction import extract_pdf_text
from app.application.source import import_pdf_source


SAMPLES = [
    ("BOE", Path("tests/samples/BOE-A-2024-14098.pdf")),
    ("BOJA", Path("tests/samples/BOJA24-138-00046-48048-01_00304998.pdf")),
    ("Programa Archiveros", Path("tests/samples/Programa_Archiveros_0.pdf")),
    ("Ayuntamiento de León", Path("tests/samples/OPOS_AYTO_LEON_INFORMATICA_B.pdf")),
]

MAX_NODES = 60
PROGRAMME_PATTERN = re.compile(r"\bprograma(?:\s+de\s+materias)?\b", re.IGNORECASE)


def _is_programme_marker(line: str) -> bool:
    return bool(PROGRAMME_PATTERN.search(line))


def _print_marker_summary(lines: list[str], markers) -> None:
    programmes = sum(_is_programme_marker(line) for line in lines)
    by_kind = {}
    by_classification = {}

    for marker in markers:
        by_kind[marker.kind] = by_kind.get(marker.kind, 0) + 1
        by_classification[marker.classification] = (
            by_classification.get(marker.classification, 0) + 1
        )

    print("\nStructural marker summary:")
    print(f"  programme markers: {programmes}")
    print(f"  structural markers: {len(markers)}")
    print("  by kind: " + ", ".join(
        f"{kind}={count}" for kind, count in sorted(by_kind.items())
    ))
    print("  by classification: " + ", ".join(
        f"{classification}={count}"
        for classification, count in sorted(by_classification.items())
    ))


def _print_tree(markers) -> None:
    print(f"\nStructural hierarchy: {min(len(markers), MAX_NODES)} shown (max {MAX_NODES})")

    for marker in markers[:MAX_NODES]:
        parent = markers[marker.parent_index].marker if marker.parent_index is not None else "<root>"
        indent = "  " * max(0, marker.level - 1)
        print(f"{indent}- [{marker.classification}] [{marker.kind}] {marker.marker} {marker.title}")
        print(f"{indent}  line={marker.line_number} level={marker.level} parent={parent}")

        if marker.continuation:
            print(f"{indent}  continuation: {marker.continuation[0][:140]}")


def inspect_document(name: str, path: Path) -> None:
    class _InMemorySourceRepository:
        def save(self, source):
            return source

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
    markers = analyze_document_structure(text)
    _print_marker_summary(lines, markers)
    _print_tree(markers)


def main() -> None:
    for name, path in SAMPLES:
        inspect_document(name, path)


if __name__ == "__main__":
    main()
