from __future__ import annotations

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from support import FixtureSourceRetriever

from app.persistence.database import Base, SessionLocal


@pytest.fixture(scope="session", autouse=True)
def isolate_database_session() -> Generator[None]:
    """Bind application sessions to a disposable database during pytest runs.

    Tests may still create their own engines and session factories explicitly,
    but any accidental use of the application's SessionLocal must never touch
    the developer database at backend/atanor.db.
    """
    with tempfile.TemporaryDirectory(prefix="atanor-pytest-") as directory:
        database_path = Path(directory) / "test.db"
        engine = create_engine(
            f"sqlite:///{database_path}",
            connect_args={"check_same_thread": False},
        )
        Base.metadata.create_all(engine)
        SessionLocal.configure(bind=engine)

        try:
            yield
        finally:
            SessionLocal.remove() if hasattr(SessionLocal, "remove") else None
            engine.dispose()


@pytest.fixture(autouse=True)
def offline_normative_sources(monkeypatch: pytest.MonkeyPatch) -> None:
    """Never reach the live BOE from tests: acquired material uses saved fixtures.

    Tests that need the real service are marked `network` and build their own
    HttpSourceRetriever explicitly.
    """
    monkeypatch.setattr(
        "app.application.study_material.providers.HttpSourceRetriever", FixtureSourceRetriever
    )
    monkeypatch.setattr("app.api.dependencies.HttpSourceRetriever", FixtureSourceRetriever)
