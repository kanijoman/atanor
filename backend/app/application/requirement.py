from dataclasses import dataclass
from pathlib import Path
import re
from typing import Protocol
from uuid import UUID

from app.application.pdf import extract_pdf_text
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


_REQUIREMENT_MARKER = re.compile(r"^\s*\d+(?:\.\d+)*[.)]\s+(.+?)\s*$")


def discover_numbered_requirement_mentions(
    text: str,
    source_id: UUID,
) -> list[RequirementMention]:
    """Discover requirement mentions from simple numbered headings.

    This intentionally implements only a small deterministic heuristic. More
    source-specific structures and semantic normalization are handled later.
    """
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
    """Discover requirement mentions from PDF text using basic structure."""

    def discover(self, source: Source) -> list[RequirementMention]:
        if not source.locator:
            raise ValueError("PDF source must have a locator")
        if Path(source.locator).suffix.lower() != ".pdf":
            raise ValueError("Requirement discovery source must be a PDF")

        text = extract_pdf_text(source)
        return discover_numbered_requirement_mentions(text, source.id)
