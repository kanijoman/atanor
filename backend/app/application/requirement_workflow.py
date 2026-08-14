from dataclasses import dataclass

from app.application.requirement_discovery import (
    PdfRequirementDiscoveryStrategy,
    RequirementDiscoveryStrategy,
    discover_requirements,
)
from app.application.requirements import RequirementRepository
from app.domain.models import Requirement, Source
from app.domain.requirement_resolution import (
    RequirementCandidate,
    RequirementResolution,
    RequirementResolutionStatus,
    resolve_requirement,
)


@dataclass(frozen=True)
class StudyRequirementSet:
    source: Source
    requirements: tuple[Requirement, ...]


def discover_and_resolve_requirements(
    source: Source,
    strategy: RequirementDiscoveryStrategy,
    requirements: tuple[Requirement, ...],
) -> list[RequirementResolution]:
    """Discover requirement mentions from a source and resolve them automatically."""
    mentions = discover_requirements(source, strategy)
    return [
        resolve_requirement(
            RequirementCandidate(
                title=mention.expression,
                source_id=mention.source_id,
            ),
            requirements,
        )
        for mention in mentions
    ]


def get_study_requirements(
    source: Source,
    repository: RequirementRepository,
    strategy: RequirementDiscoveryStrategy | None = None,
) -> StudyRequirementSet:
    """Return requirements that the user should study for a source."""
    if strategy is None:
        strategy = PdfRequirementDiscoveryStrategy()

    requirements = tuple(repository.list_by_source(source.id))
    resolutions = discover_and_resolve_requirements(source, strategy, requirements)
    resolved_requirements = tuple(
        resolution.requirement
        for resolution in resolutions
        if resolution.status is RequirementResolutionStatus.RESOLVED
        and resolution.requirement is not None
    )
    return StudyRequirementSet(
        source=source,
        requirements=resolved_requirements,
    )
