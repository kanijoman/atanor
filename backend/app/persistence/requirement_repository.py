from sqlalchemy import select

from app.domain.models import Requirement as DomainRequirement
from app.persistence.models.requirement import Requirement


class SqlAlchemyRequirementRepository:
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    def save(self, requirement: DomainRequirement) -> DomainRequirement:
        with self._session_factory() as session:
            persisted = Requirement(
                id=requirement.id,
                title=requirement.title,
                description=requirement.description,
                source_id=requirement.source_id,
            )
            session.add(persisted)
            session.commit()
            session.refresh(persisted)

            return DomainRequirement(
                id=persisted.id,
                title=persisted.title,
                description=persisted.description,
                source_id=persisted.source_id,
            )

    def get_by_id(self, requirement_id: int) -> DomainRequirement | None:
        with self._session_factory() as session:
            persisted = session.get(Requirement, requirement_id)

        if persisted is None:
            return None

        return DomainRequirement(
            id=persisted.id,
            title=persisted.title,
            description=persisted.description,
            source_id=persisted.source_id,
        )

    def list_all(self) -> list[DomainRequirement]:
        with self._session_factory() as session:
            requirements = session.scalars(
                select(Requirement).order_by(Requirement.id)
            ).all()

        return [
            DomainRequirement(
                id=requirement.id,
                title=requirement.title,
                description=requirement.description,
                source_id=requirement.source_id,
            )
            for requirement in requirements
        ]

    def list_by_source(self, source_id) -> list[DomainRequirement]:
        with self._session_factory() as session:
            requirements = session.scalars(
                select(Requirement)
                .where(Requirement.source_id == source_id)
                .order_by(Requirement.id)
            ).all()

        return [
            DomainRequirement(
                id=requirement.id,
                title=requirement.title,
                description=requirement.description,
                source_id=requirement.source_id,
            )
            for requirement in requirements
        ]
