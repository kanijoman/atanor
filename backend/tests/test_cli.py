from pathlib import Path
from uuid import UUID

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.cli import main
from app.persistence.database import Base


def _write_synthetic_pdf(path: Path) -> None:
    path.write_bytes(
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [] /Count 0 >>\nendobj\n"
        b"trailer\n<< /Root 1 0 R >>\n"
        b"%%EOF\n"
    )


def _patch_database(monkeypatch, database_path: Path) -> None:
    engine = create_engine(f"sqlite:///{database_path}")
    Base.metadata.create_all(engine)
    monkeypatch.setattr("app.cli.SessionLocal", sessionmaker(bind=engine))


def test_source_cli_end_to_end_import_get_and_list(
    tmp_path, monkeypatch, capsys
) -> None:
    pdf_path = tmp_path / "call.pdf"
    _write_synthetic_pdf(pdf_path)
    _patch_database(monkeypatch, tmp_path / "cli.db")

    assert main(["import-source", str(pdf_path)]) == 0
    import_output = capsys.readouterr().out
    assert "Source imported successfully:" in import_output
    assert "Title: call.pdf" in import_output
    assert f"Locator: {pdf_path}" in import_output

    source_id = UUID(import_output.split("ID: ", 1)[1].splitlines()[0])

    assert main(["get-source", str(source_id)]) == 0
    get_output = capsys.readouterr().out
    assert f"ID: {source_id}" in get_output
    assert "Title: call.pdf" in get_output
    assert f"Locator: {pdf_path}" in get_output

    assert main(["list-sources"]) == 0
    list_output = capsys.readouterr().out
    assert f"{source_id}" in list_output
    assert "call.pdf" in list_output
    assert str(pdf_path) in list_output


def test_get_source_command_returns_not_found_for_unknown_uuid(
    tmp_path, monkeypatch, capsys
) -> None:
    _patch_database(monkeypatch, tmp_path / "cli.db")
    source_id = UUID(int=0)

    assert main(["get-source", str(source_id)]) == 1

    output = capsys.readouterr().out
    assert f"Source not found: {source_id}" in output


def test_import_source_command_returns_error_for_missing_pdf(tmp_path, monkeypatch) -> None:
    _patch_database(monkeypatch, tmp_path / "cli.db")

    try:
        main(["import-source", str(tmp_path / "missing.pdf")])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("CLI should reject a missing PDF")
