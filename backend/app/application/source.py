import hashlib
from pathlib import Path
from typing import Protocol
from uuid import UUID

from app.domain.models import Source


class SourceRepository(Protocol):
    def save(self, source: Source) -> None: ...

    def get_by_id(self, source_id: UUID) -> Source | None: ...

    def get_by_content_hash(self, content_hash: str) -> Source | None: ...

    def list_all(self) -> list[Source]: ...


def content_hash_of(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def new_pdf_source(path: str | Path, title: str | None = None) -> Source:
    """Describe a local PDF as a (not yet persisted) source identified by its content hash."""
    pdf_path = Path(path)
    if not pdf_path.is_file():
        raise FileNotFoundError(f"Source file not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Source file must be a PDF")

    return Source(
        title=title or pdf_path.name,
        locator=str(pdf_path),
        content_hash=content_hash_of(pdf_path.read_bytes()),
    )


def import_pdf_source(
    path: str | Path, repository: SourceRepository, title: str | None = None
) -> Source:
    source = new_pdf_source(path, title)
    repository.save(source)
    return source


def get_source(source_id: UUID, repository: SourceRepository) -> Source | None:
    return repository.get_by_id(source_id)


def list_sources(repository: SourceRepository) -> list[Source]:
    return repository.list_all()
