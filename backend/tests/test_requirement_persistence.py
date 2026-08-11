from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.persistence.database import Base
from app.persistence.models.requirement import Requirement


def test_requirement_can_be_persisted_and_retrieved(tmp_path) -> None:
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
    )
    session_factory = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)

    try:
        with session_factory() as session:
            requirement = Requirement(
                title="Spanish Constitution Article 1",
                description="The first article of the Spanish Constitution.",
                context="Public administration examination",
            )
            session.add(requirement)
            session.commit()
            requirement_id = requirement.id

        with session_factory() as session:
            persisted_requirement = session.scalar(
                select(Requirement).where(Requirement.id == requirement_id)
            )

        assert persisted_requirement is not None
        assert persisted_requirement.id == requirement_id
        assert persisted_requirement.title == "Spanish Constitution Article 1"
        assert (
            persisted_requirement.description
            == "The first article of the Spanish Constitution."
        )
        assert persisted_requirement.context == "Public administration examination"
        assert persisted_requirement.created_at is not None
        assert persisted_requirement.updated_at is not None
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
