from pathlib import Path
from typing import Protocol
from uuid import UUID

from app.domain.models import Source


class SourceRepository(Protocol):
    def save(self, source: Source) -> None: ...

    def get_by_id(self, source_id: UUID) -> Source | None: ...

    def list_all(self) -> list[Source]: ...


def import_pdf_source(path: str | Path, repository: SourceRepository) -> Source:
    pdf_path = Path(path)
    if not pdf_path.is_file():
        raise FileNotFoundError(f"Source file not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Source file must be a PDF")

    source = Source(title=pdf_path.name, locator=str(pdf_path))
    repository.save(source)
    return source


def get_source(source_id: UUID, repository: SourceRepository) -> Source | None:
    return repository.get_by_id(source_id)


def list_sources(repository: SourceRepository) -> list[Source]:
    return repository.list_all()
