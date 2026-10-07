from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text

STALE_KEY = "Procedimiento administrativo común\x1f1"
KEPT_KEY = "Modelado de datos\x1f1"


def test_migration_removes_only_cached_material_of_topics_that_are_now_acquired(tmp_path) -> None:
    database_url = f"sqlite:///{tmp_path / 'reset.db'}"
    config = Config(str(Path(__file__).parents[1] / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", database_url)
    engine = create_engine(database_url)
    try:
        command.upgrade(config, "0010_knowledge_identity_optional")
        with engine.begin() as connection:
            for key, ident in ((STALE_KEY, "1" * 32), (KEPT_KEY, "2" * 32)):
                connection.execute(
                    text(
                        "INSERT INTO knowledge (id, title, description, identity_key) "
                        "VALUES (:id, 'Tema', 'texto', :key)"
                    ),
                    {"id": ident, "key": key},
                )

        command.upgrade(config, "head")

        with engine.connect() as connection:
            keys = connection.execute(text("SELECT identity_key FROM knowledge")).scalars().all()
        assert keys == [KEPT_KEY]
    finally:
        engine.dispose()
