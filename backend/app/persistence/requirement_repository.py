from sqlalchemy import select

from app.domain.models import (
    KnowledgeNeed as DomainKnowledgeNeed,
    Requirement as DomainRequirement,
    RequirementScope as DomainRequirementScope,
)
from app.persistence.models.knowledge_need import KnowledgeNeed
from app.persistence.models.requirement import Requirement
from app.persistence.models.requirement_scope import RequirementScope


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
                scopes=[
                    RequirementScope(
                        context=scope.context,
                        knowledge_needs=[
                            KnowledgeNeed(
                                topic=knowledge_need.topic,
                                depth=knowledge_need.depth,
                                knowledge_id=None,
                            )
                            for knowledge_need in scope.knowledge_needs
                        ],
                    )
                    for scope in requirement.scopes
                ],
            )
            session.add(persisted)
            session.commit()
            session.refresh(persisted)

            return self._to_domain(persisted)

    def get_by_id(self, requirement_id: int) -> DomainRequirement | None:
        with self._session_factory() as session:
            persisted = session.get(Requirement, requirement_id)
            if persisted is None:
                return None

            return self._to_domain(persisted)

    def list_all(self) -> list[DomainRequirement]:
        with self._session_factory() as session:
            requirements = session.scalars(
                select(Requirement).order_by(Requirement.id)
            ).all()
            return [self._to_domain(requirement) for requirement in requirements]

    def list_by_source(self, source_id) -> list[DomainRequirement]:
        with self._session_factory() as session:
            requirements = session.scalars(
                select(Requirement)
                .where(Requirement.source_id == source_id)
                .order_by(Requirement.id)
            ).all()
            return [self._to_domain(requirement) for requirement in requirements]

    @staticmethod
    def _to_domain(requirement: Requirement) -> DomainRequirement:
        return DomainRequirement(
            id=requirement.id,
            title=requirement.title,
            description=requirement.description,
            source_id=requirement.source_id,
            scopes=tuple(
                DomainRequirementScope(
                    context=scope.context,
                    knowledge_needs=tuple(
                        DomainKnowledgeNeed(
                            topic=knowledge_need.topic,
                            depth=knowledge_need.depth,
                            knowledge=None,
                        )
                        for knowledge_need in scope.knowledge_needs
                    ),
                )
                for scope in requirement.scopes
            ),
        )
