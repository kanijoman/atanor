from app.application.document_structure import (
    DocumentStructureMarker,
    build_structure_hierarchy,
    extract_structure_markers,
)


def test_numeric_marker_normalises_spacing_and_terminal_punctuation():
    markers = extract_structure_markers(["6. 10. 2. Tercer apartado."])

    assert [(item.marker, item.level, item.title) for item in markers] == [
        ("6.10.2", 3, "Tercer apartado."),
    ]


def test_roman_and_letter_markers_have_expected_structural_levels():
    markers = extract_structure_markers([
        "II Autoridades y personal",
        "B Oposiciones y concursos",
        "c) Detalle",
    ])

    assert [(item.kind, item.marker, item.level) for item in markers] == [
        ("roman", "II", 1),
        ("letter", "B", 2),
        ("letter", "c)", 2),
    ]


def test_non_marker_heading_ends_previous_continuation():
    markers = extract_structure_markers([
        "1 Primer apartado.",
        "CONTENIDO GENERAL",
        "Texto del apartado siguiente.",
        "2 Segundo apartado.",
    ])

    assert markers[0].continuation == ()
    assert markers[1].marker == "2"
    assert markers[1].continuation == ("Texto del apartado siguiente.",)


def test_already_classified_markers_are_not_reclassified_by_hierarchy_builder():
    markers = [
        DocumentStructureMarker(
            line_number=1,
            marker="1",
            title="Enumeration item",
            kind="numeric",
            level=1,
            continuation=(),
            classification="ENUMERATION",
        ),
    ]

    result = build_structure_hierarchy(markers)

    assert result[0].classification == "ENUMERATION"
    assert result[0].level == 1
