from pathlib import Path

import pytest

from app.application import document_processing
from app.application.document_structure import DocumentStructureMarker
from app.domain.models import Source


def test_process_document_extracts_text_and_analyzes_structure(monkeypatch):
    source = Source(title="sample.pdf", locator="sample.pdf")
    calls = []

    def fake_extract_pdf_text(received_source):
        calls.append(("extract", received_source))
        return "1 First section.\n2 Second section."

    def fake_analyze_document_structure(text):
        calls.append(("analyze", text))
        return [
            DocumentStructureMarker(
                line_number=1,
                marker="1",
                title="First section.",
                kind="numeric",
                level=1,
                continuation=(),
            )
        ]

    monkeypatch.setattr(document_processing, "extract_pdf_text", fake_extract_pdf_text)
    monkeypatch.setattr(document_processing, "analyze_document_structure", fake_analyze_document_structure)

    result = document_processing.process_document(source)

    assert result.source is source
    assert result.text == "1 First section.\n2 Second section."
    assert len(result.structure) == 1
    assert calls == [
        ("extract", source),
        ("analyze", "1 First section.\n2 Second section."),
    ]


def test_process_document_returns_empty_structure_for_textless_source(monkeypatch):
    source = Source(title="image-only.pdf", locator="image-only.pdf")

    monkeypatch.setattr(document_processing, "extract_pdf_text", lambda _: "")
    monkeypatch.setattr(
        document_processing,
        "analyze_document_structure",
        lambda _: pytest.fail("Structure analysis must not run without extracted text"),
    )

    result = document_processing.process_document(source)

    assert result.source is source
    assert result.text == ""
    assert result.structure == ()


def test_process_document_propagates_extraction_errors(monkeypatch):
    source = Source(title="missing.pdf", locator="missing.pdf")

    def fail_extraction(_):
        raise FileNotFoundError("Source file not found")

    monkeypatch.setattr(document_processing, "extract_pdf_text", fail_extraction)

    with pytest.raises(FileNotFoundError, match="Source file not found"):
        document_processing.process_document(source)


def test_real_pdf_can_be_processed_through_application_pipeline():
    sample = Path(__file__).parent / "samples" / "Programa_Archiveros_0.pdf"
    source = Source(title=sample.name, locator=str(sample))

    result = document_processing.process_document(source)

    assert result.text
    assert len(result.structure) == 25
    assert result.structure[0].marker == "Tema 1"
