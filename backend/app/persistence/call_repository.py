from uuid import UUID

from sqlalchemy import select

from app.domain.models import Call as DomainCall
from app.persistence.models.call import Call


class SqlAlchemyCallRepository:
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    def save(self, call: DomainCall) -> DomainCall:
        with self._session_factory() as session:
            persisted = Call(
                id=call.id,
                source_id=call.source_id,
                title=call.title,
            )
            session.add(persisted)
            session.commit()
            session.refresh(persisted)
            return self._to_domain(persisted)

    def get_by_id(self, call_id: UUID) -> DomainCall | None:
        with self._session_factory() as session:
            persisted = session.get(Call, call_id)

        if persisted is None:
            return None

        return self._to_domain(persisted)

    def list_all(self) -> list[DomainCall]:
        with self._session_factory() as session:
            calls = session.scalars(select(Call).order_by(Call.title, Call.id)).all()

        return [self._to_domain(call) for call in calls]

    @staticmethod
    def _to_domain(call: Call) -> DomainCall:
        return DomainCall(
            id=call.id,
            source_id=call.source_id,
            title=call.title,
        )
