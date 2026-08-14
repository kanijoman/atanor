from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

from app.domain.models import Requirement


class RequirementResolutionStatus(StrEnum):
    RESOLVED = "RESOLVED"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class RequirementCandidate:
    title: str
    source_id: UUID


@dataclass(frozen=True)
class RequirementResolution:
    candidate: RequirementCandidate
    status: RequirementResolutionStatus
    requirement: Requirement | None = None


def resolve_requirement(candidate: RequirementCandidate, requirements: tuple[Requirement, ...]) -> RequirementResolution:
    matches = tuple(requirement for requirement in requirements if requirement.title == candidate.title)
    if len(matches) == 1:
        return RequirementResolution(candidate=candidate, status=RequirementResolutionStatus.RESOLVED, requirement=matches[0])
    return RequirementResolution(candidate=candidate, status=RequirementResolutionStatus.UNRESOLVED)
