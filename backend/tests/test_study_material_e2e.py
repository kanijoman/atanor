from pathlib import Path
from uuid import UUID

from app.application.study_material import generate_study_material_for_programme_unit
from app.application.study_programmes import discover_programmes
from app.domain.models import Knowledge, KnowledgeNeed, Source, StudyProgrammeUnit


SAMPLES = Path(__file__).parent / "samples"
CALL = SAMPLES / "BOE-A-2024-14098.pdf"


class InMemoryKnowledgeRepository:
    def __init__(self) -> None:
        self.items: dict[UUID, Knowledge] = {}

    def save(self, knowledge: Knowledge) -> Knowledge:
        self.items[knowledge.id] = knowledge
        return knowledge

    def get_by_id(self, knowledge_id: UUID) -> Knowledge | None:
        return self.items.get(knowledge_id)


def test_real_call_to_persisted_candidate_study_material() -> None:
    # Start from the actual examination call used by the programme discovery
    # integration tests rather than a synthetic programme fixture.
    call = Source(title=CALL.name, locator=str(CALL))
    programmes = discover_programmes(call)

    programme = next(programme for programme in programmes if programme.identifier == "I")
    programme_unit = next(
        unit
        for unit in programme.units
        if "Ley 19/2013" in unit.title
    )

    # The real programme point is broader than the first supported Knowledge
    # Need. The candidate-facing material currently delivered by AT-086 covers
    # the access-to-public-information part of that programme point.
    need = KnowledgeNeed(
        topic="Derecho de acceso a la información pública",
        depth=1,
    )
    repository = InMemoryKnowledgeRepository()

    material = generate_study_material_for_programme_unit(
        StudyProgrammeUnit(
            number=programme_unit.number,
            title=need.topic,
            start_page=programme_unit.start_page,
            start_order=programme_unit.start_order,
            end_page=programme_unit.end_page,
            end_order=programme_unit.end_order,
        ),
        need,
        repository,
    )

    retrieved = repository.get_by_id(material.id)

    assert programme.source_id == call.id
    assert "Ley 19/2013" in programme_unit.title
    assert material.title == need.topic
    assert material.description
    assert "Artículo 12" in material.description
    assert material.sources
    assert retrieved == material
