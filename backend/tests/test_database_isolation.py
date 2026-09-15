from pathlib import Path

from app.config import DEFAULT_DATABASE_PATH
from app.persistence.database import SessionLocal


def test_pytest_session_local_does_not_use_developer_database() -> None:
    bind = SessionLocal.kw.get("bind")
    database_path = Path(str(bind.url).removeprefix("sqlite:///"))

    assert database_path.resolve() != DEFAULT_DATABASE_PATH.resolve()
