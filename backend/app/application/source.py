from pathlib import Path
from typing import Protocol

from app.domain.models import Source


class SourceRepository(Protocol):
    def save(self, source: Source) -> None: ...

    def get_by_locator(self, locator: str) -> Source | None: ...


def import_pdf_source(path: str | Path, repository: SourceRepository) -> Source:
    pdf_path = Path(path)
    if not pdf_path.is_file():
        raise FileNotFoundError(f"Source file not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Source file must be a PDF")

    source = Source(title=pdf_path.name, locator=str(pdf_path))
    repository.save(source)
    return source


def get_source(locator: str, repository: SourceRepository) -> Source | None:
    return repository.get_by_locator(locator)
