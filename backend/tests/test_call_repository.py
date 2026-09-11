from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.models import Call
from app.persistence.call_repository import SqlAlchemyCallRepository
from app.persistence.database import Base
from app.persistence.models.call import Call as CallModel
from app.persistence.models.source import Source as SourceModel


def test_call_repository_persists_and_retrieves_calls(tmp_path) -> None:
    database_url = f"sqlite:///{tmp_path / 'calls.db'}"
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    source_id = __import__('uuid').uuid4()
    with session_factory() as session:
        session.add(
            SourceModel(
                id=source_id,
                title="Official examination notice",
                locator="call.pdf",
            )
        )
        session.commit()

    repository = SqlAlchemyCallRepository(session_factory)
    call = Call(title="Administrative Management Corps", source_id=source_id)

    saved = repository.save(call)
    retrieved = repository.get_by_id(call.id)

    assert saved == call
    assert retrieved == call
    assert repository.list_all() == [call]

    engine.dispose()
