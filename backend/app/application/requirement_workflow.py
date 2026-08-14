from app.application.requirement_discovery import (
    RequirementDiscoveryStrategy,
    discover_requirements,
)
from app.domain.models import Requirement, Source
from app.domain.requirement_resolution import (
    RequirementCandidate,
    RequirementResolution,
    resolve_requirement,
)


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
