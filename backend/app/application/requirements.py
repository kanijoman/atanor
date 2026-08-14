from typing import Protocol

from app.application.requirement_discovery import (
    RequirementDiscoveryStrategy,
    RequirementMention,
    discover_requirements,
)
from app.domain.models import Requirement, Source


class RequirementRepository(Protocol):
    def save(self, requirement: Requirement) -> Requirement: ...
    def get_by_id(self, requirement_id: int) -> Requirement | None: ...
    def list_all(self) -> list[Requirement]: ...
    def list_by_source(self, source_id) -> list[Requirement]: ...


def persist_requirement_mentions(
    mentions: list[RequirementMention],
    repository: RequirementRepository,
) -> list[Requirement]:
    return [
        repository.save(
            Requirement(title=mention.expression, source_id=mention.source_id)
        )
        for mention in mentions
    ]


def discover_and_persist_requirements(
    source: Source,
    strategy: RequirementDiscoveryStrategy,
    repository: RequirementRepository,
) -> list[Requirement]:
    """Discover requirements from a source and persist the discovered mentions."""
    mentions = discover_requirements(source, strategy)
    return persist_requirement_mentions(mentions, repository)


def get_requirement(
    requirement_id: int,
    repository: RequirementRepository,
) -> Requirement | None:
    return repository.get_by_id(requirement_id)


def list_requirements(repository: RequirementRepository) -> list[Requirement]:
    return repository.list_all()
