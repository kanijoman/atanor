from pathlib import Path
from uuid import UUID

import pytest

from app.application.source import get_source, import_pdf_source, list_sources
from app.domain.models import Source


class InMemorySourceRepository:
    def __init__(self) -> None:
        self.sources: dict[UUID, Source] = {}

    def save(self, source: Source) -> None:
        self.sources[source.id] = source

    def get_by_id(self, source_id: UUID) -> Source | None:
        return self.sources.get(source_id)

    def list_all(self) -> list[Source]:
        return list(self.sources.values())


def _write_synthetic_pdf(path: Path) -> None:
    path.write_bytes(
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [] /Count 0 >>\nendobj\n"
        b"trailer\n<< /Root 1 0 R >>\n"
        b"%%EOF\n"
    )


def test_import_pdf_source_creates_source_from_synthetic_pdf(tmp_path) -> None:
    pdf_path = tmp_path / "official-call.pdf"
    _write_synthetic_pdf(pdf_path)
    repository = InMemorySourceRepository()

    source = import_pdf_source(pdf_path, repository)

    assert isinstance(source.id, UUID)
    assert source.title == "official-call.pdf"
    assert source.locator == str(pdf_path)
    assert repository.get_by_id(source.id) == source
    assert pdf_path.read_bytes().startswith(b"%PDF-")


def test_import_pdf_source_rejects_missing_file(tmp_path) -> None:
    repository = InMemorySourceRepository()

    with pytest.raises(FileNotFoundError):
        import_pdf_source(tmp_path / "missing.pdf", repository)


def test_import_pdf_source_rejects_non_pdf_file(tmp_path) -> None:
    document_path = tmp_path / "official-call.txt"
    document_path.write_text("not a pdf", encoding="utf-8")
    repository = InMemorySourceRepository()

    with pytest.raises(ValueError, match="must be a PDF"):
        import_pdf_source(document_path, repository)


def test_get_source_returns_persisted_source_by_id(tmp_path) -> None:
    pdf_path = tmp_path / "official-call.pdf"
    _write_synthetic_pdf(pdf_path)
    repository = InMemorySourceRepository()
    source = import_pdf_source(pdf_path, repository)

    assert get_source(source.id, repository) == source
    assert get_source(UUID(int=0), repository) is None


def test_list_sources_returns_persisted_sources(tmp_path) -> None:
    first_pdf = tmp_path / "first.pdf"
    second_pdf = tmp_path / "second.pdf"
    _write_synthetic_pdf(first_pdf)
    _write_synthetic_pdf(second_pdf)
    repository = InMemorySourceRepository()

    first = import_pdf_source(first_pdf, repository)
    second = import_pdf_source(second_pdf, repository)

    assert list_sources(repository) == [first, second]
