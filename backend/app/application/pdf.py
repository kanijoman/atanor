from pathlib import Path

from pypdf import PdfReader

from app.domain.models import Source


def extract_pdf_text(source: Source) -> str:
    """Extract textual content from a PDF source in page order."""
    if not source.locator:
        raise ValueError("PDF source must have a locator")

    pdf_path = Path(source.locator)
    if not pdf_path.is_file():
        raise FileNotFoundError(f"Source file not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Source file must be a PDF")

    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)
