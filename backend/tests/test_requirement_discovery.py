import pytest
from uuid import UUID

from app.application.requirement_discovery import (
    PdfRequirementDiscoveryStrategy,
    RequirementMention,
    discover_numbered_requirement_mentions,
    discover_requirements,
)
from app.application.requirements import discover_and_persist_requirements
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


def test_discover_numbered_requirement_mentions_discovers_simple_marker() -> None:
    source_id = UUID("11111111-1111-1111-1111-111111111111")

    result = discover_numbered_requirement_mentions(
        "1. Constitución Española",
        source_id,
    )

    assert result == [
        RequirementMention(
            expression="Constitución Española",
            source_id=source_id,
            locator="line:1",
        )
    ]


def test_discover_numbered_requirement_mentions_discovers_multilevel_marker() -> None:
    source_id = UUID("22222222-2222-2222-2222-222222222222")

    result = discover_numbered_requirement_mentions(
        "1.2) Ley 39/2015, de 1 de octubre",
        source_id,
    )

    assert result == [
        RequirementMention(
            expression="Ley 39/2015, de 1 de octubre",
            source_id=source_id,
            locator="line:1",
        )
    ]


def test_discover_numbered_requirement_mentions_normalises_expression_spacing() -> None:
    source_id = UUID("33333333-3333-3333-3333-333333333333")

    result = discover_numbered_requirement_mentions(
        "  1.   Constitución    Española   ",
        source_id,
    )

    assert result[0].expression == "Constitución Española"


def test_discover_numbered_requirement_mentions_ignores_non_markers() -> None:
    source_id = UUID("44444444-4444-4444-4444-444444444444")

    result = discover_numbered_requirement_mentions(
        "Texto general\n1. Requisito válido\nSin marcador\nTema 2: otro texto",
        source_id,
    )

    assert [mention.expression for mention in result] == ["Requisito válido"]


def test_discover_numbered_requirement_mentions_uses_source_id_and_line_locator() -> None:
    source_id = UUID("55555555-5555-5555-5555-555555555555")

    result = discover_numbered_requirement_mentions(
        "Introducción\n\n2) Ley aplicable",
        source_id,
    )

    assert result[0].source_id == source_id
    assert result[0].locator == "line:3"


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
    monkeypatch.setattr("app.application.requirement_discovery.extract_pdf_text", lambda _: "1. Requisitos\nPROGRAMA\n1. Constitución Española")

    result = PdfRequirementDiscoveryStrategy().discover(source)

    assert result == [RequirementMention(expression="Constitución Española", source_id=source.id, locator="line:3")]


def test_pdf_strategy_ignores_numbered_items_outside_program_context(monkeypatch: pytest.MonkeyPatch) -> None:
    source = Source(title="call.pdf", locator="/tmp/call.pdf")
    monkeypatch.setattr("app.application.requirement_discovery.extract_pdf_text", lambda _: "1. Requisitos\n2. Desarrollo\n")

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


def test_pdf_strategy_rejects_sources_without_locator() -> None:
    source = Source(title="call.pdf")

    with pytest.raises(ValueError, match="PDF source must have a locator"):
        PdfRequirementDiscoveryStrategy().discover(source)


def test_pdf_strategy_rejects_non_pdf_sources() -> None:
    source = Source(title="call.docx", locator="/tmp/call.docx")

    with pytest.raises(ValueError, match="Requirement discovery source must be a PDF"):
        PdfRequirementDiscoveryStrategy().discover(source)


def test_pdf_strategy_uses_source_id_and_expected_locators(monkeypatch: pytest.MonkeyPatch) -> None:
    source = Source(title="call.pdf", locator="/tmp/call.pdf")
    monkeypatch.setattr(
        "app.application.requirement_discovery.extract_pdf_text",
        lambda _: "1. Constitución Española\n2. Ley 39/2015",
    )

    result = PdfRequirementDiscoveryStrategy().discover(source)

    assert [(item.expression, item.source_id, item.locator) for item in result] == [
        ("Constitución Española", source.id, "line:1"),
        ("Ley 39/2015", source.id, "line:2"),
    ]
