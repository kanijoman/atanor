"""Composition root of the HTTP interface: wires persistence into the endpoints.

Endpoints depend on the aliases below instead of building repositories
themselves. Tests (and other deployments) replace `get_session_factory` through
`app.dependency_overrides`.
"""

from typing import Annotated

from fastapi import Depends

from app.persistence.call_repository import SqlAlchemyCallRepository
from app.persistence.database import SessionFactory, SessionLocal
from app.persistence.knowledge_repository import SqlAlchemyKnowledgeRepository
from app.persistence.source_repository import SqlAlchemySourceRepository
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository


def get_session_factory() -> SessionFactory:
    return SessionLocal


SessionFactoryDep = Annotated[SessionFactory, Depends(get_session_factory)]


def get_call_repository(session_factory: SessionFactoryDep) -> SqlAlchemyCallRepository:
    return SqlAlchemyCallRepository(session_factory)


def get_study_programme_repository(
    session_factory: SessionFactoryDep,
) -> SqlAlchemyStudyProgrammeRepository:
    return SqlAlchemyStudyProgrammeRepository(session_factory)


def get_knowledge_repository(session_factory: SessionFactoryDep) -> SqlAlchemyKnowledgeRepository:
    return SqlAlchemyKnowledgeRepository(session_factory)


def get_source_repository(session_factory: SessionFactoryDep) -> SqlAlchemySourceRepository:
    return SqlAlchemySourceRepository(session_factory)


CallRepositoryDep = Annotated[SqlAlchemyCallRepository, Depends(get_call_repository)]
StudyProgrammeRepositoryDep = Annotated[
    SqlAlchemyStudyProgrammeRepository, Depends(get_study_programme_repository)
]
KnowledgeRepositoryDep = Annotated[SqlAlchemyKnowledgeRepository, Depends(get_knowledge_repository)]
SourceRepositoryDep = Annotated[SqlAlchemySourceRepository, Depends(get_source_repository)]
