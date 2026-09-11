from uuid import UUID

from sqlalchemy import select

from app.domain.models import (
    StudyProgramme as DomainStudyProgramme,
    StudyProgrammeUnit as DomainStudyProgrammeUnit,
)
from app.persistence.models.call import Call
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


class SqlAlchemyStudyProgrammeRepository:
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    def save(self, programme: DomainStudyProgramme) -> DomainStudyProgramme:
        with self._session_factory() as session:
            persisted = StudyProgramme(
                id=programme.id,
                call_id=programme.call_id,
                identifier=programme.identifier,
                title=programme.title,
                units=[
                    StudyProgrammeUnit(
                        id=unit.id,
                        number=unit.number,
                        title=unit.title,
                        start_page=unit.start_page,
                        start_order=unit.start_order,
                        end_page=unit.end_page,
                        end_order=unit.end_order,
                    )
                    for unit in programme.units
                ],
            )
            session.add(persisted)
            session.commit()
            session.refresh(persisted)
            return self._to_domain(persisted)

    def get_by_id(self, programme_id: UUID) -> DomainStudyProgramme | None:
        with self._session_factory() as session:
            persisted = session.get(StudyProgramme, programme_id)
            if persisted is None:
                return None
            return self._to_domain(persisted)

    def list_by_call(self, call_id: UUID) -> list[DomainStudyProgramme]:
        with self._session_factory() as session:
            programmes = session.scalars(
                select(StudyProgramme).where(StudyProgramme.call_id == call_id)
            ).all()
        return sorted(
            (self._to_domain(programme) for programme in programmes),
            key=_programme_sort_key,
        )

    def list_by_source(self, source_id: UUID) -> list[DomainStudyProgramme]:
        """Return programmes for calls backed by a source during the transition to call-first APIs."""
        with self._session_factory() as session:
            programmes = session.scalars(
                select(StudyProgramme)
                .join(Call, StudyProgramme.call_id == Call.id)
                .where(Call.source_id == source_id)
            ).all()
        return sorted(
            (self._to_domain(programme) for programme in programmes),
            key=_programme_sort_key,
        )

    @staticmethod
    def _to_domain(programme: StudyProgramme) -> DomainStudyProgramme:
        return DomainStudyProgramme(
            id=programme.id,
            call_id=programme.call_id,
            identifier=programme.identifier,
            title=programme.title,
            units=tuple(
                DomainStudyProgrammeUnit(
                    id=unit.id,
                    number=unit.number,
                    title=unit.title,
                    start_page=unit.start_page,
                    start_order=unit.start_order,
                    end_page=unit.end_page,
                    end_order=unit.end_order,
                )
                for unit in programme.units
            ),
        )
