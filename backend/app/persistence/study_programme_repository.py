from collections.abc import Iterable
from uuid import UUID

from sqlalchemy import select

from app.domain.models import Knowledge as DomainKnowledge
from app.domain.models import KnowledgeNeed as DomainKnowledgeNeed
from app.domain.models import StudyProgramme as DomainStudyProgramme
from app.domain.models import StudyProgrammeUnit as DomainStudyProgrammeUnit
from app.persistence.database import SessionFactory
from app.persistence.models.call import Call
from app.persistence.models.knowledge_need import KnowledgeNeed
from app.persistence.models.study_programme import StudyProgramme, StudyProgrammeUnit

_ROMAN_VALUES = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def _roman_to_int(value: str) -> int | None:
    if not value:
        return None

    total = 0
    previous = 0
    for character in reversed(value.upper()):
        current = _ROMAN_VALUES.get(character)
        if current is None:
            return None
        if current < previous:
            total -= current
        else:
            total += current
        previous = current
    return total


def _programme_sort_key(programme: DomainStudyProgramme) -> tuple[int, str]:
    roman_value = _roman_to_int(programme.identifier)
    if roman_value is not None:
        return (roman_value, programme.identifier)
    return (10**9, programme.identifier)


def _need_to_persistence(need: DomainKnowledgeNeed) -> KnowledgeNeed:
    return KnowledgeNeed(
        id=need.id,
        topic=need.topic,
        depth=need.depth,
        knowledge_id=need.knowledge_id,
    )


def _need_to_domain(need: KnowledgeNeed) -> DomainKnowledgeNeed:
    knowledge = need.knowledge
    return DomainKnowledgeNeed(
        id=need.id,
        topic=need.topic,
        depth=need.depth,
        knowledge=(
            None
            if knowledge is None
            else DomainKnowledge(
                id=knowledge.id, title=knowledge.title, description=knowledge.description
            )
        ),
    )


def _unit_to_persistence(unit: DomainStudyProgrammeUnit) -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        id=unit.id,
        number=unit.number,
        title=unit.title,
        section=unit.section,
        start_page=unit.start_page,
        start_order=unit.start_order,
        end_page=unit.end_page,
        end_order=unit.end_order,
        knowledge_needs=[_need_to_persistence(need) for need in unit.knowledge_needs],
    )


def _unit_to_domain(unit: StudyProgrammeUnit) -> DomainStudyProgrammeUnit:
    return DomainStudyProgrammeUnit(
        id=unit.id,
        number=unit.number,
        title=unit.title,
        section=unit.section,
        start_page=unit.start_page,
        start_order=unit.start_order,
        end_page=unit.end_page,
        end_order=unit.end_order,
        knowledge_needs=tuple(_need_to_domain(need) for need in unit.knowledge_needs),
    )


def _programme_to_domain(programme: StudyProgramme) -> DomainStudyProgramme:
    return DomainStudyProgramme(
        id=programme.id,
        call_id=programme.call_id,
        identifier=programme.identifier,
        title=programme.title,
        units=tuple(_unit_to_domain(unit) for unit in programme.units),
    )


class SqlAlchemyStudyProgrammeRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def save(self, programme: DomainStudyProgramme) -> DomainStudyProgramme:
        with self._session_factory() as session:
            persisted = StudyProgramme(
                id=programme.id,
                call_id=programme.call_id,
                identifier=programme.identifier,
                title=programme.title,
                units=[_unit_to_persistence(unit) for unit in programme.units],
            )
            session.add(persisted)
            session.commit()
            session.refresh(persisted)
            return _programme_to_domain(persisted)

    def get_by_id(self, programme_id: UUID) -> DomainStudyProgramme | None:
        with self._session_factory() as session:
            persisted = session.get(StudyProgramme, programme_id)
            return None if persisted is None else _programme_to_domain(persisted)

    def get_unit_by_id(self, unit_id: UUID) -> DomainStudyProgrammeUnit | None:
        with self._session_factory() as session:
            persisted = session.get(StudyProgrammeUnit, unit_id)
            return None if persisted is None else _unit_to_domain(persisted)

    def save_knowledge_needs(
        self, unit_id: UUID, needs: Iterable[DomainKnowledgeNeed]
    ) -> DomainStudyProgrammeUnit | None:
        """Store the needs of a unit that has none yet (units imported before needs existed)."""
        with self._session_factory() as session:
            unit = session.get(StudyProgrammeUnit, unit_id)
            if unit is None:
                return None
            if not unit.knowledge_needs:
                unit.knowledge_needs = [_need_to_persistence(need) for need in needs]
                session.commit()
                session.refresh(unit)
            return _unit_to_domain(unit)

    def link_knowledge(self, need_id: UUID, knowledge_id: UUID) -> None:
        """Record that knowledge is now available for a need."""
        with self._session_factory() as session:
            need = session.get(KnowledgeNeed, need_id)
            if need is not None and need.knowledge_id != knowledge_id:
                need.knowledge_id = knowledge_id
                session.commit()

    def list_by_call(self, call_id: UUID) -> list[DomainStudyProgramme]:
        with self._session_factory() as session:
            programmes = session.scalars(
                select(StudyProgramme).where(StudyProgramme.call_id == call_id)
            ).all()
            return sorted(
                (_programme_to_domain(programme) for programme in programmes),
                key=_programme_sort_key,
            )

    def list_by_source(self, source_id: UUID) -> list[DomainStudyProgramme]:
        """Return programmes for calls backed by a source (transition to call-first APIs)."""
        with self._session_factory() as session:
            programmes = session.scalars(
                select(StudyProgramme)
                .join(Call, StudyProgramme.call_id == Call.id)
                .where(Call.source_id == source_id)
            ).all()
            return sorted(
                (_programme_to_domain(programme) for programme in programmes),
                key=_programme_sort_key,
            )
