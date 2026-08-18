from pathlib import Path

from app.application.document_structure import (
    DocumentStructureMarker,
    analyze_document_structure,
    build_structure_hierarchy,
    classify_structure_markers,
    extract_structure_markers,
)
from app.application.pdf_extraction import extract_pdf_text
from app.domain.models import Source


def marker(number: str, level: int, kind: str = "numeric") -> DocumentStructureMarker:
    return DocumentStructureMarker(
        line_number=1,
        marker=number,
        title=number,
        kind=kind,
        level=level,
        continuation=(),
    )


def test_simple_enumeration_is_nested_under_previous_nested_section():
    markers = [
        marker("6", 1),
        marker("6.10", 2),
        marker("6.10.2", 3),
        marker("1", 1),
        marker("2", 1),
        marker("c", 1, "letter"),
        marker("d", 1, "letter"),
        marker("7", 1),
    ]

    result = build_structure_hierarchy(markers)

    assert [node.level for node in result] == [1, 2, 3, 4, 4, 4, 4, 1]
    assert [result[node.parent_index].marker if node.parent_index is not None else None for node in result] == [
        None,
        "6",
        "6.10",
        "6.10.2",
        "6.10.2",
        "6.10.2",
        "6.10.2",
        None,
    ]


def test_explicit_nested_marker_breaks_enumeration_context():
    markers = [
        marker("6.10.2", 3),
        marker("1", 1),
        marker("6.10.3", 3),
        marker("1", 1),
    ]

    result = build_structure_hierarchy(markers)

    assert [node.level for node in result] == [3, 4, 3, 4]
    assert result[1].parent_index == 0
    assert result[2].parent_index is None
    assert result[3].parent_index == 2


def test_top_level_sequence_does_not_inherit_previous_nested_context():
    markers = [
        marker("6.10.2", 3),
        marker("7", 1),
        marker("1", 1),
    ]

    result = build_structure_hierarchy(markers)

    assert [node.level for node in result] == [3, 1, 1]
    assert result[1].parent_index is None
    assert result[2].parent_index is None


def test_simple_numeric_markers_are_structural():
    markers = classify_structure_markers([
        marker("1", 1),
        marker("2", 1),
        marker("3", 1),
    ])

    assert [item.classification for item in markers] == [
        "STRUCTURAL",
        "STRUCTURAL",
        "STRUCTURAL",
    ]


def test_nested_numeric_markers_are_structural():
    markers = classify_structure_markers([
        marker("2", 1),
        marker("2.1", 2),
        marker("2.1.1", 3),
        marker("2.1.2", 3),
    ])

    assert [item.classification for item in markers] == [
        "STRUCTURAL",
        "STRUCTURAL",
        "STRUCTURAL",
        "STRUCTURAL",
    ]


def test_numeric_and_letter_enumeration_is_classified_as_enumeration():
    markers = classify_structure_markers([
        marker("6.10", 2),
        marker("1", 1),
        marker("2", 1),
        marker("c", 1, "letter"),
        marker("d", 1, "letter"),
        marker("7", 1),
    ])

    assert [item.classification for item in markers] == [
        "STRUCTURAL",
        "ENUMERATION",
        "ENUMERATION",
        "ENUMERATION",
        "ENUMERATION",
        "STRUCTURAL",
    ]


def test_topic_markers_are_structural():
    markers = extract_structure_markers([
        "Tema 1 – La Constitución Española.",
        "Contenido del tema.",
        "Tema 2 – La Administración General del Estado.",
    ])

    assert [(item.kind, item.classification, item.marker) for item in markers] == [
        ("topic", "STRUCTURAL", "Tema 1"),
        ("topic", "STRUCTURAL", "Tema 2"),
    ]


def test_structural_marker_preserves_continuation():
    markers = extract_structure_markers([
        "1 Primer apartado.",
        "Texto que continúa el apartado.",
        "Más contenido del mismo apartado.",
        "2 Segundo apartado.",
    ])

    assert markers[0].marker == "1"
    assert markers[0].continuation == (
        "Texto que continúa el apartado.",
        "Más contenido del mismo apartado.",
    )
    assert markers[1].marker == "2"
    assert markers[1].continuation == ()


def test_analyze_document_structure_returns_empty_for_meaningless_text():
    assert analyze_document_structure("Only one line") == []


def test_real_pdf_can_be_extracted_and_analyzed():
    sample = Path(__file__).parent / "samples" / "Programa_Archiveros_0.pdf"
    source = Source(title=sample.name, locator=str(sample))

    text = extract_pdf_text(source)
    result = analyze_document_structure(text)

    assert len(result) == 25
    assert result[0].marker == "Tema 1"
    assert result[0].classification == "STRUCTURAL"
    assert result[-1].marker == "Tema 25"
    assert all(marker.kind == "topic" for marker in result)
