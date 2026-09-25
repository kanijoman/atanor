from app.application.study_material import (
    build_study_coverage_summary,
    derive_covered_aspects,
    derive_knowledge_needs_for_programme_unit,
    derive_required_aspects_for_programme_unit,
    generate_study_material_for_programme_unit,
)
from app.domain.models import KnowledgeNeed, StudyProgrammeUnit


class InMemoryKnowledgeRepository:
    def __init__(self) -> None:
        self.items = {}

    def save(self, knowledge):
        self.items[knowledge.id] = knowledge
        return knowledge

    def get_by_identity(self, identity_key: tuple[str, int]):
        return next(
            (
                knowledge
                for knowledge in self.items.values()
                if knowledge.identity_key == identity_key
            ),
            None,
        )


def real_electronic_identity_programme_unit() -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        number=6,
        title=(
            "La sociedad de la información. Identidad y firma electrónica: "
            "régimen jurídico. El DNI electrónico. La Agenda Digital para España."
        ),
        start_page=86778,
        start_order=1,
        end_page=86778,
        end_order=2,
    )


def test_derives_knowledge_need_for_real_electronic_identity_programme_unit() -> None:
    programme_unit = real_electronic_identity_programme_unit()

    needs = derive_knowledge_needs_for_programme_unit(programme_unit)

    assert len(needs) == 1
    assert needs[0].topic == "Identidad y firma electrónica"
    assert needs[0].depth == 1
    assert needs[0].identity_key == ("Identidad y firma electrónica", 1)


def test_generates_hybrid_electronic_identity_material_with_multiple_canonical_sources() -> None:
    programme_unit = real_electronic_identity_programme_unit()
    repository = InMemoryKnowledgeRepository()

    needs = derive_knowledge_needs_for_programme_unit(programme_unit)
    knowledge = generate_study_material_for_programme_unit(
        programme_unit,
        needs[0],
        repository,
    )

    assert knowledge.title == "Identidad y firma electrónica"
    assert knowledge.description
    assert "Marco jurídico" in knowledge.description
    assert "Identificación electrónica y autenticación" in knowledge.description
    assert "Firma electrónica y efectos jurídicos" in knowledge.description
    assert "Documento Nacional de Identidad" in knowledge.description

    assert len(knowledge.sources) == 4
    assert any("910/2014" in source.title for source in knowledge.sources)
    assert any("Ley 6/2020" in source.title for source in knowledge.sources)
    assert any("Real Decreto 255/2025" in source.title for source in knowledge.sources)
    assert any("Real Decreto 203/2021" in source.title for source in knowledge.sources)


def test_electronic_identity_material_covers_all_required_aspects() -> None:
    programme_unit = real_electronic_identity_programme_unit()
    repository = InMemoryKnowledgeRepository()

    needs = derive_knowledge_needs_for_programme_unit(programme_unit)
    knowledge = generate_study_material_for_programme_unit(
        programme_unit,
        needs[0],
        repository,
    )

    required_aspects = derive_required_aspects_for_programme_unit(programme_unit)
    covered_aspects = derive_covered_aspects(programme_unit, knowledge)
    summary = build_study_coverage_summary(
        KnowledgeNeed(topic="Identidad y firma electrónica", depth=1),
        required_aspects,
        covered_aspects,
    )

    assert required_aspects == (
        "Marco jurídico de la identificación y firma electrónica",
        "Identificación electrónica y autenticación",
        "Firma electrónica y efectos jurídicos",
        "Servicios electrónicos de confianza y certificados",
        "Documento Nacional de Identidad físico y digital",
        "Identificación y firma ante las Administraciones Públicas",
    )
    assert covered_aspects == required_aspects
    assert summary.status == "covered"
    assert summary.covered_count == 6
    assert summary.required_count == 6
    assert summary.pending_aspects == ()
    assert summary.coverage_percentage == 100.0
