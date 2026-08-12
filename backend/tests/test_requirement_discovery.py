import pytest

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


def test_pdf_strategy_accepts_pdf_sources(monkeypatch: pytest.MonkeyPatch) -> None:
    source = Source(title="call.pdf", locator="/tmp/call.pdf")
    monkeypatch.setattr(
        "app.application.requirement.extract_pdf_text",
        lambda _: "1. Constitución Española",
    )

    result = PdfRequirementDiscoveryStrategy().discover(source)

    assert result == [
        RequirementMention(
            expression="Constitución Española",
            source_id=source.id,
            locator="line:1",
        )
    ]


def test_pdf_strategy_rejects_non_pdf_sources() -> None:
    source = Source(title="call.docx", locator="/tmp/call.docx")

    try:
        PdfRequirementDiscoveryStrategy().discover(source)
    except ValueError as exc:
        assert str(exc) == "Requirement discovery source must be a PDF"
    else:
        raise AssertionError("Expected ValueError")
