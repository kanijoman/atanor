import pytest
from pathlib import Path
from uuid import UUID

from app.application.document_processing import DocumentProcessingResult, process_document
from app.application.document_structure import analyze_document_structure
from app.application.requirement_discovery import (
    PdfRequirementDiscoveryStrategy,
    RequirementDiscoveryStrategy,
    RequirementMention,
    discover_numbered_requirement_mentions,
    discover_requirements,
)
from app.application.requirements import discover_and_persist_requirements
from app.domain.models import Requirement, Source


SAMPLES_DIR = Path(__file__).parent / "samples"


class FakeRequirementDiscoveryStrategy:
    def __init__(self, mentions: list[RequirementMention]) -> None:
        self.mentions = mentions
        self.received_result: DocumentProcessingResult | None = None

    def discover(self, processing_result: DocumentProcessingResult) -> list[RequirementMention]:
        self.received_result = processing_result
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


def _processing_result(source: Source, text: str) -> DocumentProcessingResult:
    structure = tuple(analyze_document_structure(text))
    return DocumentProcessingResult(source=source, text=text, structure=structure)


def test_discover_numbered_requirement_mentions_discovers_simple_marker() -> None:
    source_id = UUID("11111111-1111-1111-1111-111111111111")
    result = discover_numbered_requirement_mentions("1. Constitución Española", source_id)
    assert result == [RequirementMention("Constitución Española", source_id, "line:1")]


def test_discover_numbered_requirement_mentions_discovers_multilevel_marker() -> None:
    source_id = UUID("22222222-2222-2222-2222-222222222222")
    result = discover_numbered_requirement_mentions("1.2) Ley 39/2015, de 1 de octubre", source_id)
    assert result == [RequirementMention("Ley 39/2015, de 1 de octubre", source_id, "line:1")]


def test_discover_numbered_requirement_mentions_normalises_expression_spacing() -> None:
    source_id = UUID("33333333-3333-3333-3333-333333333333")
    result = discover_numbered_requirement_mentions("  1.   Constitución    Española   ", source_id)
    assert result[0].expression == "Constitución Española"


def test_discover_numbered_requirement_mentions_ignores_non_markers() -> None:
    source_id = UUID("44444444-4444-4444-4444-444444444444")
    result = discover_numbered_requirement_mentions("Texto general\n1. Requisito válido\nSin marcador\nTema 2: otro texto", source_id)
    assert [mention.expression for mention in result] == ["Requisito válido"]


def test_discover_numbered_requirement_mentions_uses_source_id_and_line_locator() -> None:
    source_id = UUID("55555555-5555-5555-5555-555555555555")
    result = discover_numbered_requirement_mentions("Introducción\n\n2) Ley aplicable", source_id)
    assert result[0].source_id == source_id
    assert result[0].locator == "line:3"


def test_discover_requirements_processes_source_once_and_delegates_result(monkeypatch: pytest.MonkeyPatch) -> None:
    source = Source(title="call.pdf", locator="/tmp/call.pdf")
    processing_result = _processing_result(source, "PROGRAMA\n1. Constitución Española")
    mentions = [RequirementMention("Constitución Española", source.id, "line:2")]
    strategy = FakeRequirementDiscoveryStrategy(mentions)
    calls: list[Source] = []

    def fake_process_document(received_source: Source) -> DocumentProcessingResult:
        calls.append(received_source)
        return processing_result

    monkeypatch.setattr("app.application.document_processing.process_document", fake_process_document)
    result = discover_requirements(source, strategy)

    assert result == mentions
    assert strategy.received_result is processing_result
    assert calls == [source]


def test_discover_and_persist_requirements_creates_requirements_from_mentions(monkeypatch: pytest.MonkeyPatch) -> None:
    source = Source(title="call.pdf", locator="/tmp/call.pdf")
    processing_result = _processing_result(source, "PROGRAMA\n1. Constitución Española")
    mentions = [
        RequirementMention("Constitución Española", source.id, "line:10"),
        RequirementMention("Ley 39/2015", source.id, "line:11"),
    ]
    strategy = FakeRequirementDiscoveryStrategy(mentions)
    repository = FakeRequirementRepository()
    monkeypatch.setattr("app.application.document_processing.process_document", lambda _: processing_result)

    result = discover_and_persist_requirements(source, strategy, repository)

    assert result == repository.saved
    assert [requirement.title for requirement in result] == ["Constitución Española", "Ley 39/2015"]
    assert all(requirement.source_id == source.id for requirement in result)
    assert strategy.received_result is processing_result


def test_discover_and_persist_requirements_returns_empty_when_no_mentions(monkeypatch: pytest.MonkeyPatch) -> None:
    source = Source(title="call.pdf", locator="/tmp/call.pdf")
    processing_result = _processing_result(source, "PROGRAMA\n1. Constitución Española")
    strategy = FakeRequirementDiscoveryStrategy([])
    repository = FakeRequirementRepository()
    monkeypatch.setattr("app.application.document_processing.process_document", lambda _: processing_result)

    result = discover_and_persist_requirements(source, strategy, repository)
    assert result == []
    assert repository.saved == []


def test_pdf_strategy_discovers_numbered_items_inside_program_context() -> None:
    source = Source(title="call.pdf", locator="/tmp/call.pdf")
    result = PdfRequirementDiscoveryStrategy().discover(_processing_result(source, "1. Requisitos\nPROGRAMA\n1. Constitución Española"))
    assert result == [RequirementMention("Constitución Española", source.id, "line:3")]


def test_pdf_strategy_ignores_numbered_items_outside_program_context() -> None:
    source = Source(title="call.pdf", locator="/tmp/call.pdf")
    result = PdfRequirementDiscoveryStrategy().discover(_processing_result(source, "1. Requisitos\n2. Desarrollo"))
    assert result == []


def test_pdf_strategy_discovers_mentions_from_real_boe_sample() -> None:
    source = Source(title="BOE-A-2024-14098.pdf", locator=str(SAMPLES_DIR / "BOE-A-2024-14098.pdf"))
    result = PdfRequirementDiscoveryStrategy().discover(process_document(source))
    assert result
    assert all(mention.source_id == source.id for mention in result)
    assert any("Constitución Española" in mention.expression for mention in result)


def test_pdf_strategy_discovers_tema_items_from_real_jcyl_sample() -> None:
    source = Source(title="Programa_Archiveros_0.pdf", locator=str(SAMPLES_DIR / "Programa_Archiveros_0.pdf"))
    result = PdfRequirementDiscoveryStrategy().discover(process_document(source))
    assert result
    assert all(mention.source_id == source.id for mention in result)
    assert result[0].expression.startswith("Tema 1")
    assert any(mention.expression.startswith("Tema 2") for mention in result)


def test_pdf_strategy_returns_no_mentions_for_scanned_pdf_sample() -> None:
    source = Source(title="OPOS_AYTO_LEON_INFORMATICA_B.pdf", locator=str(SAMPLES_DIR / "OPOS_AYTO_LEON_INFORMATICA_B.pdf"))
    result = PdfRequirementDiscoveryStrategy().discover(process_document(source))
    assert result == []


def test_pdf_strategy_rejects_sources_without_locator() -> None:
    source = Source(title="call.pdf")
    processing_result = DocumentProcessingResult(source=source, text="", structure=())
    with pytest.raises(ValueError, match="PDF source must have a locator"):
        PdfRequirementDiscoveryStrategy().discover(processing_result)


def test_pdf_strategy_rejects_non_pdf_sources() -> None:
    source = Source(title="call.docx", locator="/tmp/call.docx")
    processing_result = DocumentProcessingResult(source=source, text="", structure=())
    with pytest.raises(ValueError, match="Requirement discovery source must be a PDF"):
        PdfRequirementDiscoveryStrategy().discover(processing_result)


def test_pdf_strategy_uses_source_id_and_expected_locators() -> None:
    source = Source(title="call.pdf", locator="/tmp/call.pdf")
    processing_result = _processing_result(source, "INTRODUCCIÓN\nPROGRAMA\n1. Constitución Española\n2. Ley 39/2015")
    result = PdfRequirementDiscoveryStrategy().discover(processing_result)
    assert [(item.expression, item.source_id, item.locator) for item in result] == [
        ("Constitución Española", source.id, "line:3"),
        ("Ley 39/2015", source.id, "line:4"),
    ]


def test_pdf_strategy_consumes_existing_processing_result_without_reprocessing() -> None:
    source = Source(title="call.pdf", locator="/tmp/call.pdf")
    processing_result = _processing_result(source, "INTRODUCCIÓN\nPROGRAMA\n1. Constitución Española")
    result = PdfRequirementDiscoveryStrategy().discover(processing_result)
    assert result == [RequirementMention("Constitución Española", source.id, "line:3")]
