from dataclasses import dataclass
from pathlib import Path
import re
from typing import Protocol
from uuid import UUID

from app.application.document_structure import analyze_document_structure
from app.application.pdf_extraction import extract_pdf_text
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
    return strategy.discover(source)


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


def _program_context(text: str) -> tuple[str, int] | None:
    """Return programme text and its zero-based starting line."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if _PROGRAM_MARKER.search(line):
            return "\n".join(lines[index:]), index
    return None


class PdfRequirementDiscoveryStrategy:
    """Discover requirement mentions from textual PDF programme content."""

    def discover(self, source: Source) -> list[RequirementMention]:
        if not source.locator:
            raise ValueError("PDF source must have a locator")
        if Path(source.locator).suffix.lower() != ".pdf":
            raise ValueError("Requirement discovery source must be a PDF")

        text = extract_pdf_text(source)
        context = _program_context(text)
        if context is None:
            return []

        program_text, program_start = context
        markers = analyze_document_structure(program_text)
        mentions: list[RequirementMention] = []

        for marker in markers:
            if marker.classification != "STRUCTURAL":
                continue
            if marker.kind not in {"numeric", "topic"}:
                continue

            line_number = program_start + marker.line_number
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
                        locator=f"line:{line_number}",
                    )
                )

        return mentions
