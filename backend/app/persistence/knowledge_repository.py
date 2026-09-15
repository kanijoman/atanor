from uuid import UUID

from sqlalchemy import select

from app.domain.models import Knowledge as DomainKnowledge
from app.persistence.models.knowledge import Knowledge


class SqlAlchemyKnowledgeRepository:
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    def save(self, knowledge: DomainKnowledge) -> DomainKnowledge:
        if knowledge.identity_key is None:
            raise ValueError("Knowledge identity key is required")

        with self._session_factory() as session:
            persisted = Knowledge(
                id=knowledge.id,
                title=knowledge.title,
                description=knowledge.description,
                identity_key=self._identity_key(*knowledge.identity_key),
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

    def get_by_identity(self, identity_key: tuple[str, int]) -> DomainKnowledge | None:
        key = self._identity_key(*identity_key)
        with self._session_factory() as session:
            persisted = session.scalar(
                select(Knowledge).where(Knowledge.identity_key == key)
            )
            if persisted is None:
                return None
            return self._to_domain(persisted)

    @staticmethod
    def _identity_key(topic: str, depth: int) -> str:
        return f"{topic}\x1f{depth}"

    @staticmethod
    def _to_domain(knowledge: Knowledge) -> DomainKnowledge:
        topic, depth = knowledge.identity_key.rsplit("\x1f", maxsplit=1)
        return DomainKnowledge(
            id=knowledge.id,
            title=knowledge.title,
            description=knowledge.description,
            identity_key=(topic, int(depth)),
        )
