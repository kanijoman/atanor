from app.application.requirement_structure import (
    discover_numbered_candidates_in_context,
    find_program_context,
)


def test_program_context_is_detected_case_insensitively() -> None:
    context = find_program_context(["Bases", "PROGRAMA"])

    assert context is not None
    assert context.name == "programa"


def test_numbered_program_heading_is_detected() -> None:
    context = find_program_context(["Bases", "11.\u2003Programa."])

    assert context is not None
    assert context.name == "programa"


def test_numbered_candidates_are_ignored_outside_program_context() -> None:
    text = """1. Requisitos de los aspirantes
2. Desarrollo del proceso
PROGRAMA
1. Constitución Española
"""

    result = discover_numbered_candidates_in_context(text)

    assert [candidate.expression for candidate in result] == ["Constitución Española"]
    assert [candidate.line_number for candidate in result] == [4]


def test_numbered_candidates_are_empty_without_program_context() -> None:
    text = """1. Requisitos de los aspirantes
2. Desarrollo del proceso
"""

    assert discover_numbered_candidates_in_context(text) == []


def test_nested_numbered_items_are_candidates_inside_program_context() -> None:
    text = """PROGRAMA
1. Organización pública
1.1. La Constitución Española
2. Sistemas operativos
"""

    result = discover_numbered_candidates_in_context(text)

    assert [candidate.expression for candidate in result] == [
        "Organización pública",
        "La Constitución Española",
        "Sistemas operativos",
    ]
