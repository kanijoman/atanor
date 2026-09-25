from app.domain.models import Knowledge, Source
from app.persistence.knowledge_repository import SqlAlchemyKnowledgeRepository
from app.persistence.database import SessionLocal


def test_knowledge_repository_round_trips_sources() -> None:
    repository = SqlAlchemyKnowledgeRepository(SessionLocal)
    source = Source(
        title="Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las Administraciones Públicas",
        locator="https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565",
    )
    knowledge = Knowledge(
        title="Procedimiento administrativo común",
        description="Study material",
        sources=(source,),
        identity_key=("Procedimiento administrativo común", 1),
    )

    repository.save(knowledge)

    restored = repository.get_by_identity(("Procedimiento administrativo común", 1))

    assert restored is not None
    assert restored.sources == (source,)
