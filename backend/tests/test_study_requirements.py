from pathlib import Path
from uuid import UUID, uuid4

import pytest

from app.application.document_processing import DocumentProcessingResult
from app.application.requirement_discovery import (
    PdfRequirementDiscoveryStrategy,
    RequirementDiscoveryStrategy,
    RequirementMention,
)
from app.application.requirement_workflow import get_study_requirements
from app.domain.models import Requirement, Source


SAMPLE_NAMES = (
    "BOE-A-2024-14098.pdf",
    "Programa_Archiveros_0.pdf",
)


class InMemoryRequirementRepository:
    def __init__(self, requirements: tuple[Requirement, ...] = ()) -> None:
        self._requirements = requirements

    def list_by_source(self, source_id: UUID) -> list[Requirement]:
        return [
            requirement
            for requirement in self._requirements
            if requirement.source_id == source_id
        ]


class StubRequirementDiscoveryStrategy:
    def __init__(self, expressions: tuple[str, ...]) -> None:
        self._expressions = expressions
        self.received_result: DocumentProcessingResult | None = None

    def discover(self, processing_result: DocumentProcessingResult) -> list[RequirementMention]:
        self.received_result = processing_result
        return [
            RequirementMention(
                expression=expression,
                source_id=processing_result.source.id,
            )
            for expression in self._expressions
        ]


def _stub_processing_result(source: Source) -> DocumentProcessingResult:
    return DocumentProcessingResult(source=source, text="", structure=())


def test_get_study_requirements_returns_resolved_requirements(monkeypatch: pytest.MonkeyPatch) -> None:
    source = Source(id=uuid4(), title="Call PDF", locator="call.pdf")
    requirement = Requirement(title="Operating Systems", description="Required knowledge.", source_id=source.id)
    repository = InMemoryRequirementRepository((requirement,))
    strategy: RequirementDiscoveryStrategy = StubRequirementDiscoveryStrategy(("Operating Systems",))
    processing_result = _stub_processing_result(source)
    monkeypatch.setattr("app.application.document_processing.process_document", lambda _: processing_result)

    result = get_study_requirements(source, repository, strategy)

    assert result.source == source
    assert result.requirements == (requirement,)
    assert all(isinstance(item, Requirement) for item in result.requirements)


def test_get_study_requirements_does_not_expose_resolution_details(monkeypatch: pytest.MonkeyPatch) -> None:
    source = Source(id=uuid4(), title="Call PDF", locator="call.pdf")
    repository = InMemoryRequirementRepository()
    strategy: RequirementDiscoveryStrategy = StubRequirementDiscoveryStrategy(())
    monkeypatch.setattr("app.application.document_processing.process_document", lambda _: _stub_processing_result(source))

    result = get_study_requirements(source, repository, strategy)

    assert not hasattr(result, "resolutions")
    assert not hasattr(result, "candidates")
    assert not hasattr(result, "mentions")


def test_get_study_requirements_excludes_unresolved_candidates(monkeypatch: pytest.MonkeyPatch) -> None:
    source = Source(id=uuid4(), title="Call PDF", locator="call.pdf")
    resolved = Requirement(title="Operating Systems", source_id=source.id)
    repository = InMemoryRequirementRepository((resolved,))
    strategy: RequirementDiscoveryStrategy = StubRequirementDiscoveryStrategy(("Operating Systems", "Unknown requirement"))
    monkeypatch.setattr("app.application.document_processing.process_document", lambda _: _stub_processing_result(source))

    result = get_study_requirements(source, repository, strategy)

    assert result.requirements == (resolved,)
    assert all(item.source_id == source.id for item in result.requirements)


def test_get_study_requirements_returns_empty_set_when_nothing_is_resolved(monkeypatch: pytest.MonkeyPatch) -> None:
    source = Source(id=uuid4(), title="Call PDF", locator="missing.pdf")
    repository = InMemoryRequirementRepository()
    strategy: RequirementDiscoveryStrategy = StubRequirementDiscoveryStrategy(("Unknown requirement",))
    monkeypatch.setattr("app.application.document_processing.process_document", lambda _: _stub_processing_result(source))

    result = get_study_requirements(source, repository, strategy)

    assert result.source == source
    assert result.requirements == ()


@pytest.mark.parametrize("sample_name", SAMPLE_NAMES)
def test_supported_real_samples_produce_a_user_oriented_requirement_set(
    sample_name: str,
) -> None:
    samples_dir = Path(__file__).parent / "samples"
    source = Source(id=uuid4(), title=sample_name, locator=str(samples_dir / sample_name))
    mentions = PdfRequirementDiscoveryStrategy().discover(source)
    requirements = tuple(
        Requirement(title=mention.expression, source_id=source.id)
        for mention in mentions
    )
    repository = InMemoryRequirementRepository(requirements)

    result = get_study_requirements(source, repository, PdfRequirementDiscoveryStrategy())

    assert result.source == source
    assert isinstance(result.requirements, tuple)
    assert result.requirements
    assert all(requirement.source_id == source.id for requirement in result.requirements)


def test_user_oriented_result_does_not_require_knowledge_of_internal_resolution(monkeypatch: pytest.MonkeyPatch) -> None:
    source = Source(id=uuid4(), title="Call PDF", locator="call.pdf")
    repository = InMemoryRequirementRepository((Requirement(title="Operating Systems", source_id=source.id),))
    strategy: RequirementDiscoveryStrategy = StubRequirementDiscoveryStrategy(("Operating Systems",))
    monkeypatch.setattr("app.application.document_processing.process_document", lambda _: _stub_processing_result(source))

    result = get_study_requirements(source, repository, strategy)

    assert result.source.id == source.id
    assert result.requirements is not None
    assert all(isinstance(requirement, Requirement) for requirement in result.requirements)
