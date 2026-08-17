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
        assert "requirement_scopes" in inspector.get_table_names()
        assert "knowledge_needs" in inspector.get_table_names()
        assert "knowledge" in inspector.get_table_names()

        requirement_columns = inspector.get_columns("requirements")
        assert {column["name"] for column in requirement_columns} == {
            "id",
            "title",
            "description",
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

        scope_columns = inspector.get_columns("requirement_scopes")
        assert {column["name"] for column in scope_columns} == {
            "id",
            "requirement_id",
            "context",
        }

        knowledge_columns = inspector.get_columns("knowledge")
        assert {column["name"] for column in knowledge_columns} == {
            "id",
            "title",
            "description",
        }

        knowledge_need_columns = inspector.get_columns("knowledge_needs")
        assert {column["name"] for column in knowledge_need_columns} == {
            "id",
            "scope_id",
            "topic",
            "depth",
            "knowledge_id",
        }

        requirement_foreign_keys = inspector.get_foreign_keys("requirements")
        assert {
            (foreign_key["referred_table"], tuple(foreign_key["constrained_columns"]))
            for foreign_key in requirement_foreign_keys
        } == {("sources", ("source_id",))}

        scope_foreign_keys = inspector.get_foreign_keys("requirement_scopes")
        assert {
            (foreign_key["referred_table"], tuple(foreign_key["constrained_columns"]))
            for foreign_key in scope_foreign_keys
        } == {("requirements", ("requirement_id",))}
        assert scope_foreign_keys[0]["options"]["ondelete"] == "CASCADE"

        knowledge_need_foreign_keys = inspector.get_foreign_keys("knowledge_needs")
        assert {
            (foreign_key["referred_table"], tuple(foreign_key["constrained_columns"]))
            for foreign_key in knowledge_need_foreign_keys
        } == {
            ("requirement_scopes", ("scope_id",)),
            ("knowledge", ("knowledge_id",)),
        }
        assert next(
            foreign_key
            for foreign_key in knowledge_need_foreign_keys
            if foreign_key["referred_table"] == "requirement_scopes"
        )["options"]["ondelete"] == "CASCADE"

        command.downgrade(config, "base")

        assert "requirements" not in inspect(engine).get_table_names()
        assert "sources" not in inspect(engine).get_table_names()
        assert "requirement_scopes" not in inspect(engine).get_table_names()
        assert "knowledge_needs" not in inspect(engine).get_table_names()
        assert "knowledge" not in inspect(engine).get_table_names()
    finally:
        engine.dispose()
