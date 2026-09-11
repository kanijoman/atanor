from pathlib import Path

from app.config import DEFAULT_DATABASE_PATH, settings


def test_default_database_path_is_relative_to_backend_directory() -> None:
    expected_path = Path(__file__).resolve().parents[1] / "atanor.db"

    assert DEFAULT_DATABASE_PATH == expected_path
    assert settings.database_url == f"sqlite:///{expected_path.as_posix()}"
