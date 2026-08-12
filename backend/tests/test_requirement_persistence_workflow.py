from uuid import uuid4

from app.application.requirement import RequirementMention, persist_requirement_mentions
from app.domain.models import Requirement


class FakeRequirementRepository:
    def __init__(self) -> None:
        self.saved: list[Requirement] = []

    def save(self, requirement: Requirement) -> Requirement:
        self.saved.append(requirement)
        return requirement


def test_persist_requirement_mentions_creates_requirements() -> None:
    source_id = uuid4()
    mentions = [
        RequirementMention(
            expression="Constitución Española",
            source_id=source_id,
            locator="line:1",
        ),
        RequirementMention(
            expression="Procedimiento administrativo común",
            source_id=source_id,
            locator="line:2",
        ),
    ]
    repository = FakeRequirementRepository()

    result = persist_requirement_mentions(mentions, repository)

    assert result == repository.saved
    assert [requirement.title for requirement in result] == [
        "Constitución Española",
        "Procedimiento administrativo común",
    ]
    assert [requirement.source_id for requirement in result] == [source_id, source_id]


def test_persist_requirement_mentions_does_not_resolve_duplicate_expressions() -> None:
    source_id = uuid4()
    mentions = [
        RequirementMention(
            expression="Constitución Española",
            source_id=source_id,
        ),
        RequirementMention(
            expression="Constitución de España",
            source_id=source_id,
        ),
    ]
    repository = FakeRequirementRepository()

    result = persist_requirement_mentions(mentions, repository)

    assert len(result) == 2
    assert [requirement.title for requirement in result] == [
        "Constitución Española",
        "Constitución de España",
    ]
