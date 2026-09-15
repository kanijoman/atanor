from __future__ import annotations

from collections.abc import Generator
from pathlib import Path
import tempfile

import pytest
from sqlalchemy import create_engine

from app.persistence.database import Base, SessionLocal


@pytest.fixture(scope="session", autouse=True)
def isolate_database_session() -> Generator[None, None, None]:
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
