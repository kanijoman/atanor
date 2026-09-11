from pathlib import Path
from uuid import UUID

from app.application.study_material import prepare_programme_unit_for_study
from app.application.study_programmes import discover_programmes
from app.domain.models import Call, Knowledge, Source


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
    """The product vertical should work from a real call to candidate material."""
    source = Source(title=CALL.name, locator=str(CALL))
    call = Call(title="Real BOE examination call", source_id=source.id)
    programmes = discover_programmes(call, source)
    programme = next(programme for programme in programmes if programme.identifier == "I")
    programme_unit = next(
        unit for unit in programme.units if "Ley 19/2013" in unit.title
    )
    repository = InMemoryKnowledgeRepository()

    material = prepare_programme_unit_for_study(programme_unit, repository)
    retrieved = repository.get_by_id(material.id)

    assert programme.call_id == call.id
    assert "Ley 19/2013" in programme_unit.title
    assert material.title == "Derecho de acceso a la información pública"
    assert material.description
    assert material.sources
    assert retrieved == material
    assert "Artículo 12" in material.description
