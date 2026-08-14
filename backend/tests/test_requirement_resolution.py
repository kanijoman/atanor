from uuid import uuid4

from app.domain.models import Requirement
from app.domain.requirement_resolution import (
    RequirementCandidate,
    RequirementResolutionStatus,
    resolve_requirement,
)


def test_requirement_candidate_can_be_resolved_against_known_requirement() -> None:
    source_id = uuid4()
    known_requirement = Requirement(
        title="Spanish Constitution Article 1",
        description="The first article of the Spanish Constitution.",
        source_id=source_id,
    )
    candidate = RequirementCandidate(
        title="Spanish Constitution Article 1",
        source_id=source_id,
    )

    resolution = resolve_requirement(candidate, (known_requirement,))

    assert resolution.status is RequirementResolutionStatus.RESOLVED
    assert resolution.requirement is known_requirement
    assert resolution.candidate == candidate


def test_requirement_candidate_is_unresolved_when_no_known_requirement_matches() -> None:
    source_id = uuid4()
    candidate = RequirementCandidate(
        title="Spanish Constitution Article 2",
        source_id=source_id,
    )
    known_requirement = Requirement(
        title="Spanish Constitution Article 1",
        source_id=source_id,
    )

    resolution = resolve_requirement(candidate, (known_requirement,))

    assert resolution.status is RequirementResolutionStatus.UNRESOLVED
    assert resolution.requirement is None
    assert resolution.candidate == candidate


def test_requirement_resolution_preserves_source_provenance() -> None:
    candidate_source_id = uuid4()
    known_source_id = uuid4()
    candidate = RequirementCandidate(
        title="Spanish Constitution Article 1",
        source_id=candidate_source_id,
    )
    known_requirement = Requirement(
        title="Spanish Constitution Article 1",
        source_id=known_source_id,
    )

    resolution = resolve_requirement(candidate, (known_requirement,))

    assert resolution.status is RequirementResolutionStatus.RESOLVED
    assert resolution.requirement is known_requirement
    assert resolution.candidate.source_id == candidate_source_id


def test_requirement_candidate_is_unresolved_when_multiple_known_requirements_match() -> None:
    source_id = uuid4()
    candidate = RequirementCandidate(
        title="Operating Systems",
        source_id=source_id,
    )
    first = Requirement(title="Operating Systems", source_id=source_id)
    second = Requirement(title="Operating Systems", source_id=source_id)

    resolution = resolve_requirement(candidate, (first, second))

    assert resolution.status is RequirementResolutionStatus.UNRESOLVED
    assert resolution.requirement is None
    assert resolution.candidate == candidate
