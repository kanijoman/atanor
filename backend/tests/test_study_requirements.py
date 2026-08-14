from pathlib import Path
from uuid import uuid4

import pytest

from app.domain.models import Requirement, Source
from app.domain.requirement_resolution import (
    RequirementCandidate,
    RequirementResolutionStatus,
    RequirementResolution,
)
from app.application.requirement_workflow import discover_and_resolve_requirements
from app.application.requirement_discovery import PdfRequirementDiscoveryStrategy


SAMPLE_NAMES = (
    "BOE-A-2024-14098.pdf",
    "Programa_Archiveros_0.pdf",
)


@pytest.fixture
def samples_dir() -> Path:
    return Path(__file__).parent / "samples"


def test_study_requirement_set_contains_resolved_requirements_without_internal_resolution_state() -> None:
    source_id = uuid4()
    requirement = Requirement(
        title="Operating Systems",
        description="Knowledge required by the examination context.",
        source_id=source_id,
    )
    resolution = RequirementResolution(
        candidate=RequirementCandidate(
            title=requirement.title,
            source_id=source_id,
        ),
        status=RequirementResolutionStatus.RESOLVED,
        requirement=requirement,
    )

    resolved_requirements = tuple(
        result.requirement
        for result in (resolution,)
        if result.status is RequirementResolutionStatus.RESOLVED
        and result.requirement is not None
    )

    assert resolved_requirements == (requirement,)
    assert resolved_requirements[0].title == "Operating Systems"
    assert not hasattr(resolved_requirements[0], "status")


def test_unresolved_requirements_are_excluded_from_user_output() -> None:
    source_id = uuid4()
    resolved = Requirement(
        title="Operating Systems",
        source_id=source_id,
    )
    unresolved_candidate = RequirementCandidate(
        title="Unknown requirement",
        source_id=source_id,
    )

    resolutions = (
        RequirementResolution(
            candidate=RequirementCandidate(
                title=resolved.title,
                source_id=source_id,
            ),
            status=RequirementResolutionStatus.RESOLVED,
            requirement=resolved,
        ),
        RequirementResolution(
            candidate=unresolved_candidate,
            status=RequirementResolutionStatus.UNRESOLVED,
            requirement=None,
        ),
    )

    user_requirements = tuple(
        result.requirement
        for result in resolutions
        if result.status is RequirementResolutionStatus.RESOLVED
        and result.requirement is not None
    )

    assert user_requirements == (resolved,)
    assert all(item.title != unresolved_candidate.title for item in user_requirements)


def test_all_unresolved_candidates_produce_an_empty_user_requirement_set() -> None:
    source_id = uuid4()
    resolutions = (
        RequirementResolution(
            candidate=RequirementCandidate(
                title="Unknown requirement",
                source_id=source_id,
            ),
            status=RequirementResolutionStatus.UNRESOLVED,
            requirement=None,
        ),
    )

    user_requirements = tuple(
        result.requirement
        for result in resolutions
        if result.status is RequirementResolutionStatus.RESOLVED
        and result.requirement is not None
    )

    assert user_requirements == ()


def test_user_requirement_output_preserves_requirement_provenance() -> None:
    source_id = uuid4()
    requirement = Requirement(
        title="Constitution",
        source_id=source_id,
    )
    resolution = RequirementResolution(
        candidate=RequirementCandidate(
            title=requirement.title,
            source_id=source_id,
        ),
        status=RequirementResolutionStatus.RESOLVED,
        requirement=requirement,
    )

    user_requirements = tuple(
        result.requirement
        for result in (resolution,)
        if result.status is RequirementResolutionStatus.RESOLVED
        and result.requirement is not None
    )

    assert user_requirements[0].source_id == source_id


@pytest.mark.parametrize("sample_name", SAMPLE_NAMES)
def test_real_supported_samples_can_feed_the_user_requirement_flow(
    samples_dir: Path,
    sample_name: str,
) -> None:
    source_id = uuid4()
    source = Source(
        id=source_id,
        title=sample_name,
        locator=str(samples_dir / sample_name),
    )

    mentions = PdfRequirementDiscoveryStrategy().discover(source)
    assert mentions

    requirements = tuple(
        Requirement(title=mention.expression, source_id=source_id)
        for mention in mentions
    )
    resolutions = discover_and_resolve_requirements(
        source,
        PdfRequirementDiscoveryStrategy(),
        requirements,
    )

    user_requirements = tuple(
        result.requirement
        for result in resolutions
        if result.status is RequirementResolutionStatus.RESOLVED
        and result.requirement is not None
    )

    assert len(user_requirements) <= len(mentions)
    assert all(requirement.source_id == source_id for requirement in user_requirements)
