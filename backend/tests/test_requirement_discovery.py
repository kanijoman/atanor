import pytest

from app.application.requirement import (
    PdfRequirementDiscoveryStrategy,
    RequirementMention,
    discover_and_persist_requirements,
    discover_requirements,
)
from app.domain.models import Requirement, Source


class FakeRequirementDiscoveryStrategy:
    def __init__(self, mentions: list[RequirementMention]) -> None:
        self.mentions = mentions
        self.received_source: Source | None = None

    def discover(self, source: Source) -> list[RequirementMention]:
        self.received_source = source
        return self.mentions


class FakeRequirementRepository:
    def __init__(self) -> None:
        self.saved: list[Requirement] = []

    def save(self, requirement: Requirement) -> Requirement:
        self.saved.append(requirement)
        return requirement

    def get_by_id(self, requirement_id: int) -> Requirement | None:
        return None

    def list_all(self) -> list[Requirement]:
        return list(self.saved)


def test_discover_requirements_delegates_to_strategy() -> None:
    source = Source(title="call.pdf", locator="/tmp/call.pdf")
    mentions = [RequirementMention(expression="Constitución Española", source_id=source.id, locator="page:1")]
    strategy = FakeRequirementDiscoveryStrategy(mentions)

    result = discover_requirements(source, strategy)

    assert result == mentions
    assert strategy.received_source is source


def test_discover_and_persist_requirements_creates_requirements_from_mentions() -> None:
    source = Source(title="call.pdf", locator="/tmp/call.pdf")
    mentions = [
        RequirementMention(expression="Constitución Española", source_id=source.id, locator="line:10"),
        RequirementMention(expression="Ley 39/2015", source_id=source.id, locator="line:11"),
    ]
    strategy = FakeRequirementDiscoveryStrategy(mentions)
    repository = FakeRequirementRepository()

    result = discover_and_persist_requirements(source, strategy, repository)

    assert result == repository.saved
    assert [requirement.title for requirement in result] == ["Constitución Española", "Ley 39/2015"]
    assert all(requirement.source_id == source.id for requirement in result)


def test_discover_and_persist_requirements_returns_empty_when_no_mentions() -> None:
    source = Source(title="call.pdf", locator="/tmp/call.pdf")
    strategy = FakeRequirementDiscoveryStrategy([])
    repository = FakeRequirementRepository()

    result = discover_and_persist_requirements(source, strategy, repository)

    assert result == []
    assert repository.saved == []


def test_pdf_strategy_discovers_numbered_items_inside_program_context(monkeypatch: pytest.MonkeyPatch) -> None:
    source = Source(title="call.pdf", locator="/tmp/call.pdf")
    monkeypatch.setattr("app.application.requirement.extract_pdf_text", lambda _: "1. Requisitos\nPROGRAMA\n1. Constitución Española")

    result = PdfRequirementDiscoveryStrategy().discover(source)

    assert result == [RequirementMention(expression="Constitución Española", source_id=source.id, locator="line:3")]


def test_pdf_strategy_ignores_numbered_items_outside_program_context(monkeypatch: pytest.MonkeyPatch) -> None:
    source = Source(title="call.pdf", locator="/tmp/call.pdf")
    monkeypatch.setattr("app.application.requirement.extract_pdf_text", lambda _: "1. Requisitos\n2. Desarrollo\n")

    assert PdfRequirementDiscoveryStrategy().discover(source) == []


def test_pdf_strategy_discovers_mentions_from_real_boe_sample() -> None:
    sample_path = "tests/samples/BOE-A-2024-14098.pdf"
    source = Source(title="BOE-A-2024-14098.pdf", locator=sample_path)

    result = PdfRequirementDiscoveryStrategy().discover(source)

    assert result
    assert all(mention.source_id == source.id for mention in result)
    assert any("Constitución Española" in mention.expression for mention in result)


def test_pdf_strategy_discovers_tema_items_from_real_jcyl_sample() -> None:
    sample_path = "tests/samples/Programa_Archiveros_0.pdf"
    source = Source(title="Programa_Archiveros_0.pdf", locator=sample_path)

    result = PdfRequirementDiscoveryStrategy().discover(source)

    assert result
    assert all(mention.source_id == source.id for mention in result)
    assert result[0].expression.startswith("Tema 1")
    assert any(mention.expression.startswith("Tema 2") for mention in result)


def test_pdf_strategy_returns_no_mentions_for_scanned_pdf_sample() -> None:
    sample_path = "tests/samples/OPOS_AYTO_LEON_INFORMATICA_B.pdf"
    source = Source(title="OPOS_AYTO_LEON_INFORMATICA_B.pdf", locator=sample_path)

    result = PdfRequirementDiscoveryStrategy().discover(source)

    assert result == []


def test_pdf_strategy_rejects_non_pdf_sources() -> None:
    source = Source(title="call.docx", locator="/tmp/call.docx")

    try:
        PdfRequirementDiscoveryStrategy().discover(source)
    except ValueError as exc:
        assert str(exc) == "Requirement discovery source must be a PDF"
    else:
        raise AssertionError("Expected ValueError")
