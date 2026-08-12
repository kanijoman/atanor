import pytest

from app.application.source import get_source, import_pdf_source
from app.domain.models import Source


class InMemorySourceRepository:
    def __init__(self) -> None:
        self.sources: dict[str, Source] = {}

    def save(self, source: Source) -> None:
        self.sources[source.locator or ""] = source

    def get_by_locator(self, locator: str) -> Source | None:
        return self.sources.get(locator)


def test_import_pdf_source_creates_source(tmp_path) -> None:
    pdf_path = tmp_path / "official-call.pdf"
    pdf_path.write_bytes(b"%PDF-test")
    repository = InMemorySourceRepository()

    source = import_pdf_source(pdf_path, repository)

    assert source == Source(title="official-call.pdf", locator=str(pdf_path))
    assert repository.get_by_locator(str(pdf_path)) == source


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


def test_get_source_returns_persisted_source(tmp_path) -> None:
    pdf_path = tmp_path / "official-call.pdf"
    pdf_path.write_bytes(b"%PDF-test")
    repository = InMemorySourceRepository()
    source = import_pdf_source(pdf_path, repository)

    assert get_source(str(pdf_path), repository) == source
    assert get_source(str(tmp_path / "other.pdf"), repository) is None
