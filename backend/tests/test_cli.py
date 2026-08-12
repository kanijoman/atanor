from pathlib import Path

from app.cli import main


def _write_synthetic_pdf(path: Path) -> None:
    path.write_bytes(
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [] /Count 0 >>\nendobj\n"
        b"trailer\n<< /Root 1 0 R >>\n"
        b"%%EOF\n"
    )


def test_import_source_command_imports_pdf(tmp_path, monkeypatch, capsys) -> None:
    pdf_path = tmp_path / "call.pdf"
    _write_synthetic_pdf(pdf_path)
    database_path = tmp_path / "cli.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")

    assert main(["import-source", str(pdf_path)]) == 0

    output = capsys.readouterr().out
    assert "Source imported successfully:" in output
    assert "Title: call.pdf" in output
    assert f"Locator: {pdf_path}" in output


def test_import_source_command_returns_error_for_missing_pdf(tmp_path, monkeypatch) -> None:
    database_path = tmp_path / "cli.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")

    try:
        main(["import-source", str(tmp_path / "missing.pdf")])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("CLI should reject a missing PDF")
