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

MAX_NODES = 60

# A structural marker is deliberately broader than a knowledge unit. The
# experiment first tries to recover document hierarchy and only later decides
# which nodes are relevant to the knowledge model.
TEMA_PATTERN = re.compile(r"^Tema\s+(?P<number>\d+)\s*[.\-–—:]?\s*(?P<title>.+)$", re.IGNORECASE)
NUMERIC_PATTERN = re.compile(
    r"^(?P<marker>\d+(?:\s*\.\s*\d+)*\s*[.)])\s*(?P<title>.+)$"
)
ROMAN_PATTERN = re.compile(
    r"^(?P<marker>[IVXLCDM]+(?:\s*\.\s*\d+)*\s*[.)])\s*(?P<title>.+)$",
    re.IGNORECASE,
)
LETTER_PATTERN = re.compile(
    r"^(?P<marker>[A-Z](?:\s*\.\s*\d+)*\s*[.)])\s*(?P<title>.+)$"
)
PROGRAMME_PATTERN = re.compile(r"\bprograma(?:\s+de\s+materias)?\b", re.IGNORECASE)


@dataclass(frozen=True)
class StructuralMarker:
    line_number: int
    marker: str
    title: str
    kind: str
    level: int
    continuation: tuple[str, ...]
    parent_index: int | None = None


def _normalise_marker(marker: str) -> str:
    marker = re.sub(r"\s+", "", marker)
    return marker.rstrip(".")


def _marker_level(marker: str, kind: str) -> int:
    if kind == "topic":
        return 3

    normalised = _normalise_marker(marker)
    parts = normalised.split(".")

    if kind == "roman":
        # Roman top-level sections (I., II.) and their descendants (II.1.).
        return 1 + max(0, len(parts) - 1)

    if kind == "letter":
        return 2 + max(0, len(parts) - 1)

    return len(parts)


def _match_marker(line: str) -> tuple[str, str, str, int] | None:
    match = TEMA_PATTERN.match(line)
    if match:
        marker = f"Tema {match.group('number')}"
        return marker, match.group("title").strip(), "topic", 3

    for pattern, kind in (
        (ROMAN_PATTERN, "roman"),
        (LETTER_PATTERN, "letter"),
        (NUMERIC_PATTERN, "numeric"),
    ):
        match = pattern.match(line)
        if match:
            marker = _normalise_marker(match.group("marker"))
            return marker, match.group("title").strip(), kind, _marker_level(marker, kind)

    return None


def _is_programme_marker(line: str) -> bool:
    return bool(PROGRAMME_PATTERN.search(line))


def _looks_like_parent_heading(line: str) -> bool:
    if _is_programme_marker(line):
        return True
    if len(line) > 180:
        return False
    return bool(re.fullmatch(r"[A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑ\s,.-]{4,}", line))


def _extract_markers(lines: list[str]) -> list[StructuralMarker]:
    markers: list[StructuralMarker] = []

    index = 0
    while index < len(lines):
        line = lines[index]
        matched = _match_marker(line)

        if matched is None:
            index += 1
            continue

        marker, title, kind, level = matched
        continuation: list[str] = []
        next_index = index + 1

        while next_index < len(lines):
            next_line = lines[next_index]
            if _match_marker(next_line) or _looks_like_parent_heading(next_line):
                break
            continuation.append(next_line)
            next_index += 1

        markers.append(
            StructuralMarker(
                line_number=index + 1,
                marker=marker,
                title=title,
                kind=kind,
                level=level,
                continuation=tuple(continuation),
            )
        )
        index = next_index

    return markers


def _is_simple_marker(marker: StructuralMarker) -> bool:
    return marker.kind in {"numeric", "roman", "letter"} and "." not in marker.marker


def _build_hierarchy(markers: list[StructuralMarker]) -> list[StructuralMarker]:
    result: list[StructuralMarker] = []
    stack: list[int] = []
    enumeration_level: int | None = None

    for marker in markers:
        effective_level = marker.level

        # A simple marker immediately following an explicitly nested marker
        # may be an enumeration inside that section rather than a new
        # top-level section. This covers patterns such as:
        #
        #   6.10.2 Exención...
        #       1 ...
        #       2 ...
        #       c) ...
        #       d) ...
        #
        # The context is intentionally narrow: it starts only after a nested
        # marker and is discarded as soon as an explicit multi-part marker or
        # a normal top-level section appears.
        if enumeration_level is not None:
            if _is_simple_marker(marker) and marker.level == 1:
                effective_level = enumeration_level
            else:
                enumeration_level = None

        if enumeration_level is None and result:
            previous = result[-1]
            if previous.level >= 3 and _is_simple_marker(marker) and marker.level == 1:
                enumeration_level = previous.level + 1
                effective_level = enumeration_level

        while stack and result[stack[-1]].level >= effective_level:
            stack.pop()

        parent_index = stack[-1] if stack else None
        node = StructuralMarker(
            line_number=marker.line_number,
            marker=marker.marker,
            title=marker.title,
            kind=marker.kind,
            level=effective_level,
            continuation=marker.continuation,
            parent_index=parent_index,
        )
        result.append(node)
        stack.append(len(result) - 1)

    return result


def _print_marker_summary(lines: list[str], markers: list[StructuralMarker]) -> None:
    programmes = sum(_is_programme_marker(line) for line in lines)
    by_kind = {}
    for marker in markers:
        by_kind[marker.kind] = by_kind.get(marker.kind, 0) + 1

    print("\nStructural marker summary:")
    print(f"  programme markers: {programmes}")
    print(f"  structural markers: {len(markers)}")
    print("  by kind: " + ", ".join(f"{kind}={count}" for kind, count in sorted(by_kind.items())))


def _print_tree(markers: list[StructuralMarker]) -> None:
    print(f"\nStructural hierarchy: {min(len(markers), MAX_NODES)} shown (max {MAX_NODES})")

    for marker in markers[:MAX_NODES]:
        parent = markers[marker.parent_index].marker if marker.parent_index is not None else "<root>"
        indent = "  " * max(0, marker.level - 1)
        print(f"{indent}- [{marker.kind}] {marker.marker} {marker.title}")
        print(f"{indent}  line={marker.line_number} level={marker.level} parent={parent}")

        if marker.continuation:
            preview = marker.continuation[0]
            print(f"{indent}  continuation: {preview[:140]}")


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
    markers = _build_hierarchy(_extract_markers(lines))
    _print_marker_summary(lines, markers)
    _print_tree(markers)


def main() -> None:
    for name, path in SAMPLES:
        inspect_document(name, path)


if __name__ == "__main__":
    main()
