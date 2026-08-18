from app.experiments.inspect_document_structure import (
    StructuralMarker,
    _build_hierarchy,
)


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
