from pathlib import Path
from uuid import uuid4

import pytest

from app.application.requirement_workflow import get_study_requirements
from app.domain.models import Requirement, Source


SAMPLE_NAMES = (
    "BOE-A-2024-14098.pdf",
    "Programa_Archiveros_0.pdf",
)


@pytest.fixture
def samples_dir() -> Path:
    return Path(__file__).parent / "samples"


def test_get_study_requirements_returns_resolved_requirements() -> None:
    source = Source(
        id=uuid4(),
        title="Call PDF",
        locator="call.pdf",
    )

    result = get_study_requirements(source)

    assert result.source == source
    assert all(isinstance(requirement, Requirement) for requirement in result.requirements)


def test_get_study_requirements_does_not_expose_resolution_details() -> None:
    source = Source(
        id=uuid4(),
        title="Call PDF",
        locator="call.pdf",
    )

    result = get_study_requirements(source)

    assert not hasattr(result, "resolutions")
    assert not hasattr(result, "candidates")
    assert not hasattr(result, "mentions")


def test_get_study_requirements_excludes_unresolved_candidates() -> None:
    source = Source(
        id=uuid4(),
        title="Call PDF",
        locator="call.pdf",
    )

    result = get_study_requirements(source)

    assert all(requirement.source_id == source.id for requirement in result.requirements)


def test_get_study_requirements_returns_empty_set_when_nothing_is_resolved() -> None:
    source = Source(
        id=uuid4(),
        title="Unsupported or unresolved source",
        locator="missing.pdf",
    )

    result = get_study_requirements(source)

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

    result = get_study_requirements(source)

    assert result.source == source
    assert isinstance(result.requirements, tuple)
    assert all(requirement.source_id == source.id for requirement in result.requirements)


def test_user_oriented_result_does_not_require_knowledge_of_internal_workflow() -> None:
    source = Source(
        id=uuid4(),
        title="Call PDF",
        locator="call.pdf",
    )

    result = get_study_requirements(source)

    # The consumer only needs the source and the study requirements.
    assert result.source.id == source.id
    assert result.requirements is not None
