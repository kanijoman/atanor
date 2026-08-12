from pathlib import Path

from app.application.requirement import (
    PdfRequirementDiscoveryStrategy,
    RequirementMention,
    discover_requirements,
)
from app.domain.models import Source


class FakeRequirementDiscoveryStrategy:
    def __init__(self, mentions: list[RequirementMention]) -> None:
        self.mentions = mentions
        self.received_source: Source | None = None

    def discover(self, source: Source) -> list[RequirementMention]:
        self.received_source = source
        return self.mentions


def test_discover_requirements_delegates_to_strategy() -> None:
    source = Source(title="call.pdf", locator="/tmp/call.pdf")
    mentions = [
        RequirementMention(
            expression="Constitución Española",
            source_id=source.id,
            locator="page:1",
        )
    ]
    strategy = FakeRequirementDiscoveryStrategy(mentions)

    result = discover_requirements(source, strategy)

    assert result == mentions
    assert strategy.received_source is source


def test_pdf_strategy_accepts_pdf_sources() -> None:
    source = Source(title="call.pdf", locator=str(Path("/tmp/call.pdf")))

    assert PdfRequirementDiscoveryStrategy().discover(source) == []


def test_pdf_strategy_rejects_non_pdf_sources() -> None:
    source = Source(title="call.docx", locator="/tmp/call.docx")

    try:
        PdfRequirementDiscoveryStrategy().discover(source)
    except ValueError as exc:
        assert str(exc) == "Requirement discovery source must be a PDF"
    else:
        raise AssertionError("Expected ValueError")
