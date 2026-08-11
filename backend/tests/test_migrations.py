from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect


def test_initial_migration_round_trip(tmp_path) -> None:
    database_path = tmp_path / "migration-test.db"
    database_url = f"sqlite:///{database_path}"
    config = Config(str(Path(__file__).parents[1] / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", database_url)

    engine = create_engine(database_url)
    try:
        command.upgrade(config, "head")

        inspector = inspect(engine)
        assert "alembic_version" in inspector.get_table_names()
        assert "requirements" in inspector.get_table_names()
        assert {
            column["name"] for column in inspector.get_columns("requirements")
        } == {
            "id",
            "title",
            "description",
            "context",
            "created_at",
            "updated_at",
        }

        command.downgrade(config, "base")

        assert "requirements" not in inspect(engine).get_table_names()
    finally:
        engine.dispose()
