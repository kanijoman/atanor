from uuid import UUID, uuid4

from app.application.requirement import (
    RequirementMention,
    discover_numbered_requirement_mentions,
)


def test_discover_numbered_requirement_mentions() -> None:
    source_id = uuid4()
    text = """
1. Constitución Española
Introduction
2.1. Procedimiento administrativo común
3) Empleo público
"""

    result = discover_numbered_requirement_mentions(text, source_id)

    assert result == [
        RequirementMention(
            expression="Constitución Española",
            source_id=source_id,
            locator="line:2",
        ),
        RequirementMention(
            expression="Procedimiento administrativo común",
            source_id=source_id,
            locator="line:4",
        ),
        RequirementMention(
            expression="Empleo público",
            source_id=source_id,
            locator="line:5",
        ),
    ]


def test_discover_numbered_requirement_mentions_normalizes_whitespace() -> None:
    source_id = uuid4()

    result = discover_numbered_requirement_mentions(
        "1.   Constitución   Española\n2. Procedimiento\tAdministrativo",
        source_id,
    )

    assert [mention.expression for mention in result] == [
        "Constitución Española",
        "Procedimiento Administrativo",
    ]


def test_discover_numbered_requirement_mentions_ignores_unmarked_lines() -> None:
    source_id = UUID("00000000-0000-0000-0000-000000000001")

    result = discover_numbered_requirement_mentions(
        "Introduction\nConstitution\nReferences",
        source_id,
    )

    assert result == []
