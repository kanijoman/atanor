from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.application.source import get_source, import_pdf_source, list_sources
from app.cli import main
from app.persistence.database import Base
from app.persistence.models.source import Source as SourceModel
from app.persistence.source_repository import SqlAlchemySourceRepository


def _write_synthetic_pdf(path: Path) -> None:
    path.write_bytes(
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [] /Count 0 >>\nendobj\n"
        b"trailer\n<< /Root 1 0 R >>\n"
        b"%%EOF\n"
    )


def test_source_import_get_and_list_are_isolated(tmp_path, monkeypatch, capsys) -> None:
    database_path = tmp_path / "e2e.db"
    database_url = f"sqlite:///{database_path}"
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    repository = SqlAlchemySourceRepository(session_factory)
    pdf_path = tmp_path / "convocatoria.pdf"
    _write_synthetic_pdf(pdf_path)

    monkeypatch.setattr("app.cli.SessionLocal", session_factory)

    assert main(["import-source", str(pdf_path)]) == 0
    assert "Source imported successfully:" in capsys.readouterr().out

    imported = get_source(str(pdf_path), repository)
    assert imported is not None

    assert main(["get-source", str(pdf_path)]) == 0
    assert "convocatoria.pdf" in capsys.readouterr().out

    assert main(["list-sources"]) == 0
    output = capsys.readouterr().out
    assert "Sources:" in output
    assert "convocatoria.pdf" in output

    assert list_sources(repository) == [imported]

    with session_factory() as session:
        assert session.query(SourceModel).count() == 1
