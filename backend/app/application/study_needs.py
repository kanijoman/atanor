"""Knowledge needs of programme units: what a candidate must know for each unit.

A programme unit is the requirement as the convocatoria states it. Its knowledge
need is valid even when no study material exists for it: supported units get the
topic Atanor can prepare material for, any other unit keeps its official wording
as the topic and stays without knowledge until material is available.
"""

from collections.abc import Iterable
from dataclasses import replace
from typing import Protocol
from uuid import UUID

from app.application.study_material import derive_knowledge_needs_for_programme_unit
from app.domain.models import KnowledgeNeed, StudyProgramme, StudyProgrammeUnit


class KnowledgeNeedRepository(Protocol):
    def save_knowledge_needs(
        self, unit_id: UUID, needs: Iterable[KnowledgeNeed]
    ) -> StudyProgrammeUnit | None: ...


def needs_for_unit(unit: StudyProgrammeUnit) -> tuple[KnowledgeNeed, ...]:
    try:
        return derive_knowledge_needs_for_programme_unit(unit)
    except ValueError:
        return (KnowledgeNeed(topic=unit.title, depth=1),)


def attach_knowledge_needs(programme: StudyProgramme) -> StudyProgramme:
    """Give every unit of a freshly discovered programme its knowledge need."""
    units = tuple(
        unit if unit.knowledge_needs else replace(unit, knowledge_needs=needs_for_unit(unit))
        for unit in programme.units
    )
    return replace(programme, units=units)


def ensure_knowledge_needs(
    unit: StudyProgrammeUnit, repository: KnowledgeNeedRepository
) -> StudyProgrammeUnit:
    """Create the needs of a unit imported before needs were stored."""
    if unit.knowledge_needs:
        return unit
    return repository.save_knowledge_needs(unit.id, needs_for_unit(unit)) or unit
