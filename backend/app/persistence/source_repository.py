from app.domain.models import Source as DomainSource
from app.persistence.models.source import Source


class SqlAlchemySourceRepository:
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    def save(self, source: DomainSource) -> None:
        with self._session_factory() as session:
            session.add(Source(title=source.title, locator=source.locator or ""))
            session.commit()

    def get_by_locator(self, locator: str) -> DomainSource | None:
        from sqlalchemy import select

        with self._session_factory() as session:
            persisted = session.scalar(select(Source).where(Source.locator == locator))

        if persisted is None:
            return None

        return DomainSource(title=persisted.title, locator=persisted.locator)
