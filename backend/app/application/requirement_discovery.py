from dataclasses import dataclass
import re
from typing import Protocol
from uuid import UUID

from app.application.document_processing import DocumentProcessingResult
from app.domain.models import Source


@dataclass(frozen=True)
class RequirementMention:
    """A requirement expression discovered in a source."""

    expression: str
    source_id: UUID
    locator: str | None = None


class RequirementDiscoveryStrategy(Protocol):
    def discover(
        self, processing_result: DocumentProcessingResult
    ) -> list[RequirementMention]: ...


def discover_requirements(
    source: Source,
    strategy: RequirementDiscoveryStrategy,
) -> list[RequirementMention]:
    """Process a source once and discover requirements from the shared result."""
    from app.application.document_processing import process_document

    return strategy.discover(process_document(source))


_REQUIREMENT_MARKER = re.compile(r"^\s*\d+(?:\.\d+)*[.)]\s+(.+?)\s*$")
_PROGRAM_MARKER = re.compile(r"\bprograma\b", re.IGNORECASE)


def discover_numbered_requirement_mentions(
    text: str,
    source_id: UUID,
) -> list[RequirementMention]:
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


def _program_start(text: str) -> int | None:
    for index, line in enumerate(text.splitlines()):
        if _PROGRAM_MARKER.search(line):
            return index
    return None


class PdfRequirementDiscoveryStrategy:
    """Discover requirement mentions from a processed PDF document."""

    def discover(
        self, processing_result: DocumentProcessingResult
    ) -> list[RequirementMention]:
        source = processing_result.source
        if not source.locator:
            raise ValueError("PDF source must have a locator")
        if not source.locator.lower().endswith(".pdf"):
            raise ValueError("Requirement discovery source must be a PDF")

        program_start = _program_start(processing_result.text)
        if program_start is None:
            return []

        mentions: list[RequirementMention] = []
        for marker in processing_result.structure:
            if marker.line_number <= program_start:
                continue
            if marker.classification != "STRUCTURAL":
                continue
            if marker.kind not in {"numeric", "topic"}:
                continue

            if marker.kind == "topic":
                expression = f"{marker.marker} {marker.title}"
            else:
                expression = marker.title
            expression = " ".join(expression.split())

            if expression:
                mentions.append(
                    RequirementMention(
                        expression=expression,
                        source_id=source.id,
                        locator=f"line:{marker.line_number}",
                    )
                )

        return mentions
