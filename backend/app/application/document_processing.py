from dataclasses import dataclass

from app.application.document_structure import (
    DocumentStructureMarker,
    analyze_document_structure,
)
from app.application.pdf_extraction import extract_pdf_text
from app.domain.models import Source


@dataclass(frozen=True)
class DocumentProcessingResult:
    """Result of processing a source through extraction and structure analysis."""

    source: Source
    text: str
    structure: tuple[DocumentStructureMarker, ...]


def process_document(source: Source) -> DocumentProcessingResult:
    """Extract and analyze a document without persisting the processing result."""
    text = extract_pdf_text(source)
    structure = () if not text.strip() else tuple(analyze_document_structure(text))

    return DocumentProcessingResult(
        source=source,
        text=text,
        structure=structure,
    )
