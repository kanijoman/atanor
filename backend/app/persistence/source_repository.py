from uuid import UUID

from sqlalchemy import select

from app.domain.models import Source as DomainSource
from app.persistence.database import SessionFactory
from app.persistence.models.source import Source


def _to_domain(source: Source) -> DomainSource:
    return DomainSource(
        id=source.id,
        title=source.title,
        locator=source.locator,
        content_hash=source.content_hash,
    )


class SqlAlchemySourceRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def save(self, source: DomainSource) -> None:
        with self._session_factory() as session:
            session.add(
                Source(
                    id=source.id,
                    title=source.title,
                    locator=source.locator or "",
                    content_hash=source.content_hash,
                )
            )
            session.commit()

    def get_by_id(self, source_id: UUID) -> DomainSource | None:
        with self._session_factory() as session:
            persisted = session.get(Source, source_id)
            return None if persisted is None else _to_domain(persisted)

    def get_by_content_hash(self, content_hash: str) -> DomainSource | None:
        with self._session_factory() as session:
            persisted = session.scalar(select(Source).where(Source.content_hash == content_hash))
            return None if persisted is None else _to_domain(persisted)

    def list_all(self) -> list[DomainSource]:
        with self._session_factory() as session:
            persisted_sources = session.scalars(select(Source).order_by(Source.id)).all()
            return [_to_domain(source) for source in persisted_sources]
