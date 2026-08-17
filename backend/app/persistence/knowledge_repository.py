from uuid import UUID

from app.domain.models import Knowledge as DomainKnowledge
from app.persistence.models.knowledge import Knowledge


class SqlAlchemyKnowledgeRepository:
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    def save(self, knowledge: DomainKnowledge) -> DomainKnowledge:
        with self._session_factory() as session:
            persisted = Knowledge(
                id=knowledge.id,
                title=knowledge.title,
                description=knowledge.description,
            )
            session.add(persisted)
            session.commit()
            session.refresh(persisted)
            return self._to_domain(persisted)

    def get_by_id(self, knowledge_id: UUID) -> DomainKnowledge | None:
        with self._session_factory() as session:
            persisted = session.get(Knowledge, knowledge_id)
            if persisted is None:
                return None
            return self._to_domain(persisted)

    @staticmethod
    def _to_domain(knowledge: Knowledge) -> DomainKnowledge:
        return DomainKnowledge(
            id=knowledge.id,
            title=knowledge.title,
            description=knowledge.description,
        )
