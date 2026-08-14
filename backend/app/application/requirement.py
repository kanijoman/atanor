from dataclasses import dataclass
from pathlib import Path
import re
from typing import Protocol
from uuid import UUID

from app.application.pdf_extraction import extract_pdf_text
from app.application.requirement_structure import discover_numbered_candidates_in_context
from app.domain.models import Requirement, Source
from app.domain.requirement_resolution import (
    RequirementCandidate,
    RequirementResolution,
    resolve_requirement,
)


@dataclass(frozen=True)
class RequirementMention:
    """A requirement expression discovered in a source."""

    expression: str
    source_id: UUID
    locator: str | None = None


class RequirementDiscoveryStrategy(Protocol):
    def discover(self, source: Source) -> list[RequirementMention]: ...


class RequirementRepository(Protocol):
    def save(self, requirement: Requirement) -> Requirement: ...
    def get_by_id(self, requirement_id: int) -> Requirement | None: ...
    def list_all(self) -> list[Requirement]: ...


def discover_requirements(source: Source, strategy: RequirementDiscoveryStrategy) -> list[RequirementMention]:
    return strategy.discover(source)


def persist_requirement_mentions(mentions: list[RequirementMention], repository: RequirementRepository) -> list[Requirement]:
    return [
        repository.save(Requirement(title=mention.expression, source_id=mention.source_id))
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


def get_requirement(requirement_id: int, repository: RequirementRepository) -> Requirement | None:
    return repository.get_by_id(requirement_id)


def list_requirements(repository: RequirementRepository) -> list[Requirement]:
    return repository.list_all()


_REQUIREMENT_MARKER = re.compile(r"^\s*\d+(?:\.\d+)*[.)]\s+(.+?)\s*$")


def discover_numbered_requirement_mentions(text: str, source_id: UUID) -> list[RequirementMention]:
    """Discover numbered requirement mentions without structural filtering."""
    mentions: list[RequirementMention] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = _REQUIREMENT_MARKER.match(line)
        if not match:
            continue
        expression = " ".join(match.group(1).split())
        if expression:
            mentions.append(
                RequirementMention(
                    expression=expression,
                    source_id=source_id,
                    locator=f"line:{line_number}",
                )
            )
    return mentions


class PdfRequirementDiscoveryStrategy:
    """Discover requirement mentions from textual PDF content."""

    def discover(self, source: Source) -> list[RequirementMention]:
        if not source.locator:
            raise ValueError("PDF source must have a locator")
        if Path(source.locator).suffix.lower() != ".pdf":
            raise ValueError("Requirement discovery source must be a PDF")

        text = extract_pdf_text(source)
        candidates = discover_numbered_candidates_in_context(text)
        return [
            RequirementMention(
                expression=candidate.expression,
                source_id=source.id,
                locator=f"line:{candidate.line_number}",
            )
            for candidate in candidates
        ]
