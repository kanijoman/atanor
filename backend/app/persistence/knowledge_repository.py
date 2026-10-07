from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.models import Knowledge as DomainKnowledge
from app.domain.models import Source as DomainSource
from app.persistence.database import SessionFactory
from app.persistence.models.knowledge import Knowledge
from app.persistence.models.source import Source


class SqlAlchemyKnowledgeRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def save(self, knowledge: DomainKnowledge) -> DomainKnowledge:
        """Persist knowledge; concurrent saves of the same identity converge on one record."""
        identity_key = (
            None if knowledge.identity_key is None else self._identity_key(*knowledge.identity_key)
        )
        with self._session_factory() as session:
            try:
                return self._insert(session, knowledge, identity_key)
            except IntegrityError:
                session.rollback()
                existing = self._find_by_key(session, identity_key)
                if existing is None:
                    raise
                return self._to_domain(existing)

    def _insert(
        self, session: Session, knowledge: DomainKnowledge, identity_key: str | None
    ) -> DomainKnowledge:
        persisted = Knowledge(
            id=knowledge.id,
            title=knowledge.title,
            description=knowledge.description,
            identity_key=identity_key,
        )
        persisted.sources = [
            self._get_or_create_source(session, source) for source in knowledge.sources
        ]
        session.add(persisted)
        session.commit()
        session.refresh(persisted)
        return self._to_domain(persisted)

    @staticmethod
    def _find_by_key(session: Session, identity_key: str | None) -> Knowledge | None:
        if identity_key is None:
            return None
        return session.scalar(select(Knowledge).where(Knowledge.identity_key == identity_key))

    def get_by_id(self, knowledge_id: UUID) -> DomainKnowledge | None:
        with self._session_factory() as session:
            persisted = session.get(Knowledge, knowledge_id)
            if persisted is None:
                return None
            return self._to_domain(persisted)

    def get_by_identity(self, identity_key: tuple[str, int]) -> DomainKnowledge | None:
        key = self._identity_key(*identity_key)
        with self._session_factory() as session:
            persisted = self._find_by_key(session, key)
            if persisted is None:
                return None
            return self._to_domain(persisted)

    @staticmethod
    def _identity_key(topic: str, depth: int) -> str:
        return f"{topic}\x1f{depth}"

    @staticmethod
    def _get_or_create_source(session: Session, source: DomainSource) -> Source:
        persisted = session.scalar(select(Source).where(Source.locator == (source.locator or "")))
        if persisted is not None:
            return persisted

        persisted = Source(
            id=source.id,
            title=source.title,
            locator=source.locator or "",
        )
        session.add(persisted)
        session.flush()
        return persisted

    @staticmethod
    def _to_domain(knowledge: Knowledge) -> DomainKnowledge:
        identity_key = None
        if knowledge.identity_key is not None:
            topic, depth = knowledge.identity_key.rsplit("\x1f", maxsplit=1)
            identity_key = (topic, int(depth))

        return DomainKnowledge(
            id=knowledge.id,
            title=knowledge.title,
            description=knowledge.description,
            sources=tuple(
                DomainSource(
                    id=source.id,
                    title=source.title,
                    locator=source.locator or None,
                )
                for source in knowledge.sources
            ),
            identity_key=identity_key,
        )
