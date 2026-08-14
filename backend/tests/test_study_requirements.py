from pathlib import Path
from uuid import UUID, uuid4

import pytest

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

    def discover(self, source: Source) -> list[RequirementMention]:
        return [
            RequirementMention(
                expression=expression,
                source_id=source.id,
            )
            for expression in self._expressions
        ]


@pytest.fixture
def samples_dir() -> Path:
    return Path(__file__).parent / "samples"


def test_get_study_requirements_returns_resolved_requirements() -> None:
    source = Source(id=uuid4(), title="Call PDF", locator="call.pdf")
    requirement = Requirement(
        title="Operating Systems",
        description="Required knowledge.",
        source_id=source.id,
    )
    repository = InMemoryRequirementRepository((requirement,))
    strategy: RequirementDiscoveryStrategy = StubRequirementDiscoveryStrategy(
        ("Operating Systems",)
    )

    result = get_study_requirements(source, repository, strategy)

    assert result.source == source
    assert result.requirements == (requirement,)
    assert all(isinstance(item, Requirement) for item in result.requirements)


def test_get_study_requirements_does_not_expose_resolution_details() -> None:
    source = Source(id=uuid4(), title="Call PDF", locator="call.pdf")
    repository = InMemoryRequirementRepository()
    strategy: RequirementDiscoveryStrategy = StubRequirementDiscoveryStrategy(())

    result = get_study_requirements(source, repository, strategy)

    assert not hasattr(result, "resolutions")
    assert not hasattr(result, "candidates")
    assert not hasattr(result, "mentions")


def test_get_study_requirements_excludes_unresolved_candidates() -> None:
    source = Source(id=uuid4(), title="Call PDF", locator="call.pdf")
    resolved = Requirement(title="Operating Systems", source_id=source.id)
    repository = InMemoryRequirementRepository((resolved,))
    strategy: RequirementDiscoveryStrategy = StubRequirementDiscoveryStrategy(
        ("Operating Systems", "Unknown requirement")
    )

    result = get_study_requirements(source, repository, strategy)

    assert result.requirements == (resolved,)
    assert all(item.source_id == source.id for item in result.requirements)


def test_get_study_requirements_returns_empty_set_when_nothing_is_resolved() -> None:
    source = Source(id=uuid4(), title="Call PDF", locator="missing.pdf")
    repository = InMemoryRequirementRepository()
    strategy: RequirementDiscoveryStrategy = StubRequirementDiscoveryStrategy(
        ("Unknown requirement",)
    )

    result = get_study_requirements(source, repository, strategy)

    assert result.source == source
    assert result.requirements == ()


@pytest.mark.parametrize("sample_name", SAMPLE_NAMES)
def test_supported_real_samples_produce_a_user_oriented_requirement_set(
    samples_dir: Path,
    sample_name: str,
) -> None:
    source = Source(
        id=uuid4(),
        title=sample_name,
        locator=str(samples_dir / sample_name),
    )
    mentions = PdfRequirementDiscoveryStrategy().discover(source)
    requirements = tuple(
        Requirement(title=mention.expression, source_id=source.id)
        for mention in mentions
    )
    repository = InMemoryRequirementRepository(requirements)

    result = get_study_requirements(
        source,
        repository,
        PdfRequirementDiscoveryStrategy(),
    )

    assert result.source == source
    assert isinstance(result.requirements, tuple)
    assert result.requirements
    assert all(requirement.source_id == source.id for requirement in result.requirements)


def test_user_oriented_result_does_not_require_knowledge_of_internal_resolution() -> None:
    source = Source(id=uuid4(), title="Call PDF", locator="call.pdf")
    repository = InMemoryRequirementRepository(
        (Requirement(title="Operating Systems", source_id=source.id),)
    )
    strategy: RequirementDiscoveryStrategy = StubRequirementDiscoveryStrategy(
        ("Operating Systems",)
    )

    result = get_study_requirements(source, repository, strategy)

    assert result.source.id == source.id
    assert result.requirements is not None
    assert all(isinstance(requirement, Requirement) for requirement in result.requirements)
