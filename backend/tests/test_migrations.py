from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import CHAR, create_engine, inspect


def test_migrations_round_trip(tmp_path) -> None:
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
        assert "sources" in inspector.get_table_names()
        assert {
            column["name"] for column in inspector.get_columns("requirements")
        } == {
            "id",
            "title",
            "description",
            "context",
            "source_id",
            "created_at",
            "updated_at",
        }
        source_columns = inspector.get_columns("sources")
        assert {column["name"] for column in source_columns} == {
            "id",
            "title",
            "locator",
            "created_at",
            "updated_at",
        }
        source_id = next(column for column in source_columns if column["name"] == "id")
        assert isinstance(source_id["type"], CHAR)
        assert source_id["type"].length == 32

        foreign_keys = inspector.get_foreign_keys("requirements")
        assert {
            (foreign_key["referred_table"], tuple(foreign_key["constrained_columns"]))
            for foreign_key in foreign_keys
        } == {("sources", ("source_id",))}

        command.downgrade(config, "base")

        assert "requirements" not in inspect(engine).get_table_names()
        assert "sources" not in inspect(engine).get_table_names()
    finally:
        engine.dispose()
