from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.dependencies import get_session_factory, get_uploads_dir
from app.main import app
from app.persistence.database import Base
from app.persistence.models import Source as PersistenceSource  # noqa: F401  (register tables)
from app.persistence.source_repository import SqlAlchemySourceRepository

SAMPLES = Path(__file__).parent / "samples"
BOE_SAMPLE = SAMPLES / "BOE-A-2024-14098.pdf"
BOJA_SAMPLE = SAMPLES / "BOJA24-138-00046-48048-01_00304998.pdf"
ARCHIVEROS_SAMPLE = SAMPLES / "Programa_Archiveros_0.pdf"


@pytest.fixture
def uploads_dir(tmp_path: Path) -> Path:
    return tmp_path / "uploads"


@pytest.fixture
def session_factory(tmp_path: Path):
    engine = create_engine(f"sqlite:///{tmp_path / 'upload.db'}")
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine)
    engine.dispose()


@pytest.fixture
def client(session_factory, uploads_dir: Path):
    app.dependency_overrides[get_session_factory] = lambda: session_factory
    app.dependency_overrides[get_uploads_dir] = lambda: uploads_dir
    yield TestClient(app)
    app.dependency_overrides.clear()


def _upload(client: TestClient, content: bytes, filename: str = "convocatoria.pdf"):
    return client.post(
        "/api/calls",
        params={"filename": filename},
        content=content,
        headers={"Content-Type": "application/pdf"},
    )


def test_uploading_a_convocatoria_imports_the_call_and_its_programmes(client) -> None:
    response = _upload(client, BOE_SAMPLE.read_bytes(), "Mi convocatoria.pdf")

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Mi convocatoria.pdf"
    programmes = client.get(f"/api/calls/{body['id']}/programmes").json()
    assert [programme["identifier"] for programme in programmes][:2] == ["I", "II"]
    assert client.get("/api/calls").json() == [{"id": body["id"], "title": "Mi convocatoria.pdf"}]


def test_uploading_the_same_document_again_returns_the_existing_call(client) -> None:
    content = BOE_SAMPLE.read_bytes()
    first = _upload(client, content, "primera.pdf")

    second = _upload(client, content, "otra-copia.pdf")

    assert first.status_code == 201
    assert second.status_code == 200
    assert second.json() == first.json()
    assert len(client.get("/api/calls").json()) == 1


def test_uploaded_document_is_stored_by_content_hash(client, uploads_dir: Path) -> None:
    _upload(client, BOE_SAMPLE.read_bytes())

    stored = list(uploads_dir.glob("*.pdf"))

    assert len(stored) == 1
    assert len(stored[0].stem) == 64


def test_the_source_is_identified_by_its_content_hash(client, session_factory) -> None:
    _upload(client, BOJA_SAMPLE.read_bytes())

    [source] = SqlAlchemySourceRepository(session_factory).list_all()

    assert source.content_hash is not None
    assert SqlAlchemySourceRepository(session_factory).get_by_content_hash(source.content_hash)


def test_a_document_that_is_not_a_convocatoria_is_rejected_and_not_stored(
    client, uploads_dir: Path, session_factory
) -> None:
    response = _upload(client, ARCHIVEROS_SAMPLE.read_bytes())

    assert response.status_code == 422
    assert "convocatoria" in response.json()["detail"]
    assert not list(uploads_dir.glob("*.pdf"))
    assert SqlAlchemySourceRepository(session_factory).list_all() == []
    assert client.get("/api/calls").json() == []


def test_content_that_is_not_a_pdf_is_rejected(client) -> None:
    response = _upload(client, b"just some text")

    assert response.status_code == 422
    assert response.json()["detail"] == "The uploaded file is not a PDF document."


def test_an_empty_upload_is_rejected(client) -> None:
    response = _upload(client, b"")

    assert response.status_code == 422
    assert response.json()["detail"] == "The uploaded file is empty."


def test_an_oversized_upload_is_rejected(client, monkeypatch) -> None:
    monkeypatch.setattr("app.api.calls.MAX_UPLOAD_BYTES", 10)
    monkeypatch.setattr("app.application.call_upload.MAX_UPLOAD_BYTES", 10)

    response = _upload(client, b"%PDF-" + b"0" * 100)

    assert response.status_code == 413


def test_a_filename_is_required(client) -> None:
    response = client.post(
        "/api/calls", content=b"%PDF-1.4", headers={"Content-Type": "application/pdf"}
    )

    assert response.status_code == 422
