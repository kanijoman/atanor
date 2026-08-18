import importlib.util
from pathlib import Path
import sys


_EXPERIMENT = Path(__file__).parents[1] / "experiments" / "inspect_document_structure.py"
_SPEC = importlib.util.spec_from_file_location("inspect_document_structure", _EXPERIMENT)
assert _SPEC is not None
assert _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MODULE
_SPEC.loader.exec_module(_MODULE)

StructuralMarker = _MODULE.StructuralMarker
_build_hierarchy = _MODULE._build_hierarchy
_classify_markers = _MODULE._classify_markers
_extract_markers = _MODULE._extract_markers
inspect_document = _MODULE.inspect_document


def marker(number: str, level: int, kind: str = "numeric") -> StructuralMarker:
    return StructuralMarker(
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

    result = _build_hierarchy(markers)

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

    result = _build_hierarchy(markers)

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

    result = _build_hierarchy(markers)

    assert [node.level for node in result] == [3, 1, 1]
    assert result[1].parent_index is None
    assert result[2].parent_index is None


def test_simple_numeric_markers_are_structural():
    markers = _classify_markers([
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
    markers = _classify_markers([
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
    markers = _classify_markers([
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
    markers = _extract_markers([
        "Tema 1 – La Constitución Española.",
        "Contenido del tema.",
        "Tema 2 – La Administración General del Estado.",
    ])

    assert [(item.kind, item.classification, item.marker) for item in markers] == [
        ("topic", "STRUCTURAL", "Tema 1"),
        ("topic", "STRUCTURAL", "Tema 2"),
    ]


def test_structural_marker_preserves_continuation():
    markers = _extract_markers([
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


def test_image_only_document_skips_structural_analysis(capsys):
    sample = Path(__file__).parent / "samples" / "OPOS_AYTO_LEON_INFORMATICA_B.pdf"

    inspect_document("Ayuntamiento de León", sample)

    output = capsys.readouterr().out
    assert "Extraction status: IMAGE_ONLY_OR_EMPTY" in output
    assert "Structural analysis: SKIPPED" in output
