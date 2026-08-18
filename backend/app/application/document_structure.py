from dataclasses import dataclass
import re


@dataclass(frozen=True)
class DocumentStructureMarker:
    """A structural marker detected in extracted document text."""

    line_number: int
    marker: str
    title: str
    kind: str
    level: int
    continuation: tuple[str, ...]
    classification: str = "STRUCTURAL"
    parent_index: int | None = None


TEMA_PATTERN = re.compile(
    r"^Tema\s+(?P<number>\d+)\s*[.\-–—:]?\s*(?P<title>.+)$",
    re.IGNORECASE,
)
NUMERIC_PATTERN = re.compile(
    r"^(?P<marker>\d+(?:\s*\.\s*\d+)*\s*[.)]?)(?:\s+)(?P<title>.+)$"
)
ROMAN_PATTERN = re.compile(
    r"^(?P<marker>[IVXLCDM]+(?:\s*\.\s*\d+)*\s*[.)]?)\s+(?P<title>.+)$"
)
LETTER_PATTERN = re.compile(
    r"^(?P<marker>(?:[A-Z](?:\s*\.\s*\d+)*|[a-z](?:\s*\.\s*\d+)*[.)]))\s+(?P<title>.+)$"
)


def _normalise_marker(marker: str) -> str:
    marker = re.sub(r"\s+", "", marker)
    return marker.rstrip(".")


def _marker_level(marker: str, kind: str) -> int:
    if kind == "topic":
        return 3

    parts = _normalise_marker(marker).split(".")

    if kind == "roman":
        return 1 + max(0, len(parts) - 1)

    if kind == "letter":
        return 2 + max(0, len(parts) - 1)

    return len(parts)


def _match_marker(line: str) -> tuple[str, str, str, int] | None:
    match = TEMA_PATTERN.match(line)
    if match:
        return f"Tema {match.group('number')}", match.group("title").strip(), "topic", 3

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


def _looks_like_parent_heading(line: str) -> bool:
    if len(line) > 180:
        return False
    return bool(re.fullmatch(r"[A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑ\s,.-]{4,}", line))


def extract_structure_markers(lines: list[str]) -> list[DocumentStructureMarker]:
    """Extract structural markers and their immediate continuation text."""
    markers: list[DocumentStructureMarker] = []
    index = 0
    pending_continuation: list[str] = []

    while index < len(lines):
        line = lines[index]
        matched = _match_marker(line)
        if matched is None:
            if _looks_like_parent_heading(line):
                pending_continuation = []
            else:
                pending_continuation.append(line)
            index += 1
            continue

        marker, title, kind, level = matched
        continuation: list[str] = pending_continuation
        pending_continuation = []
        next_index = index + 1

        while next_index < len(lines):
            next_line = lines[next_index]
            if _match_marker(next_line) or _looks_like_parent_heading(next_line):
                break
            continuation.append(next_line)
            next_index += 1

        markers.append(
            DocumentStructureMarker(
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


def _is_simple_marker(marker: DocumentStructureMarker) -> bool:
    return marker.kind in {"numeric", "roman", "letter"} and "." not in marker.marker


def _simple_numeric_value(marker: DocumentStructureMarker) -> int | None:
    if marker.kind != "numeric" or not _is_simple_marker(marker):
        return None
    try:
        return int(marker.marker)
    except ValueError:
        return None


def _with_classification(
    marker: DocumentStructureMarker,
    classification: str,
) -> DocumentStructureMarker:
    return DocumentStructureMarker(
        line_number=marker.line_number,
        marker=marker.marker,
        title=marker.title,
        kind=marker.kind,
        level=marker.level,
        continuation=marker.continuation,
        classification=classification,
        parent_index=marker.parent_index,
    )


def classify_structure_markers(
    markers: list[DocumentStructureMarker],
) -> list[DocumentStructureMarker]:
    """Classify the locally identifiable markers as structural or enumeration."""
    result: list[DocumentStructureMarker] = []
    enumeration_level: int | None = None
    expected_numeric: int | None = None

    for marker in markers:
        numeric_value = _simple_numeric_value(marker)

        if enumeration_level is not None:
            if numeric_value is not None:
                if expected_numeric == numeric_value:
                    result.append(_with_classification(marker, "ENUMERATION"))
                    expected_numeric = numeric_value + 1
                    continue
                enumeration_level = None
                expected_numeric = None
            elif _is_simple_marker(marker) and marker.kind in {"roman", "letter"}:
                result.append(_with_classification(marker, "ENUMERATION"))
                continue
            else:
                enumeration_level = None
                expected_numeric = None

        previous = result[-1] if result else None
        if numeric_value == 1 and previous is not None and previous.level >= 2:
            enumeration_level = previous.level + 1
            expected_numeric = 2
            result.append(_with_classification(marker, "ENUMERATION"))
            continue

        result.append(_with_classification(marker, "STRUCTURAL"))

    return result


def build_structure_hierarchy(
    markers: list[DocumentStructureMarker],
) -> list[DocumentStructureMarker]:
    """Build parent relationships while keeping enumerations inside their context."""
    if any(marker.classification == "STRUCTURAL" for marker in markers):
        markers = classify_structure_markers(markers)

    result: list[DocumentStructureMarker] = []
    stack: list[int] = []
    enumeration_level: int | None = None

    for marker in markers:
        effective_level = marker.level

        if marker.classification == "ENUMERATION":
            if enumeration_level is None:
                previous = result[-1] if result else None
                enumeration_level = marker.level if previous is None else previous.level + 1
            effective_level = enumeration_level
        elif enumeration_level is not None:
            enumeration_level = None

        while stack and result[stack[-1]].level >= effective_level:
            stack.pop()

        parent_index = stack[-1] if stack else None
        node = DocumentStructureMarker(
            line_number=marker.line_number,
            marker=marker.marker,
            title=marker.title,
            kind=marker.kind,
            level=effective_level,
            continuation=marker.continuation,
            classification=marker.classification,
            parent_index=parent_index,
        )
        result.append(node)
        stack.append(len(result) - 1)

    return result


def analyze_document_structure(text: str) -> list[DocumentStructureMarker]:
    """Analyze extracted text and return its deterministic document structure."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) < 2:
        return []

    extracted = extract_structure_markers(lines)
    classified = classify_structure_markers(extracted)
    return build_structure_hierarchy(classified)
