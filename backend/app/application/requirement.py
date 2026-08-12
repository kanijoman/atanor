from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
from uuid import UUID

from app.domain.models import Source


@dataclass(frozen=True)
class RequirementMention:
    """A requirement expression discovered in a source."""

    expression: str
    source_id: UUID
    locator: str | None = None


class RequirementDiscoveryStrategy(Protocol):
    def discover(self, source: Source) -> list[RequirementMention]: ...


def discover_requirements(
    source: Source,
    strategy: RequirementDiscoveryStrategy,
) -> list[RequirementMention]:
    """Discover requirement mentions from a source using the supplied strategy."""
    return strategy.discover(source)


class PdfRequirementDiscoveryStrategy:
    """Placeholder strategy for PDF sources.

    PDF content extraction is intentionally implemented in AT-025.
    """

    def discover(self, source: Source) -> list[RequirementMention]:
        if Path(source.locator).suffix.lower() != ".pdf":
            raise ValueError("Requirement discovery source must be a PDF")
        return []
