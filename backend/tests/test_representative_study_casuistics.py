from app.application.study_material import (
    derive_covered_aspects,
    derive_knowledge_needs_for_programme_unit,
    derive_required_aspects_for_programme_unit,
    generate_study_material_for_programme_unit,
)
from app.domain.models import StudyProgrammeUnit


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


def real_ley_39_2015_programme_unit() -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        number=1,
        title=(
            "La Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo "
            "Común de las Administraciones Públicas. Objeto y ámbito de aplicación"
        ),
        start_page=1,
        start_order=1,
        end_page=1,
        end_order=2,
    )


def real_identity_and_electronic_signature_programme_unit() -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        number=1,
        title=(
            "La sociedad de la información. Identidad y firma electrónica: "
            "régimen jurídico. El DNI electrónico. La Agenda Digital para España."
        ),
        start_page=1,
        start_order=1,
        end_page=1,
        end_order=2,
    )


def real_personal_data_protection_programme_unit() -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        number=12,
        title=(
            "La protección de datos personales y su régimen Jurídico: principios, "
            "derechos y obligaciones."
        ),
        start_page=1,
        start_order=1,
        end_page=1,
        end_order=2,
    )


def test_ley_39_2015_casuistic_exercises_partial_coverage() -> None:
    programme_unit = real_ley_39_2015_programme_unit()
    repository = InMemoryKnowledgeRepository()

    needs = derive_knowledge_needs_for_programme_unit(programme_unit)
    assert len(needs) == 1
    assert needs[0].topic == "Procedimiento administrativo común"
    assert needs[0].depth == 1
    assert needs[0].identity_key == (
        "Procedimiento administrativo común",
        1,
    )

    knowledge = generate_study_material_for_programme_unit(
        programme_unit,
        needs[0],
        repository,
    )

    assert knowledge.title == needs[0].topic
    assert knowledge.identity_key == needs[0].identity_key
    assert knowledge.description
    assert len(knowledge.sources) == 1
    assert knowledge.sources[0].locator == (
        "https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565"
    )
    assert repository.get_by_identity(needs[0].identity_key) is knowledge

    required_aspects = derive_required_aspects_for_programme_unit(programme_unit)
    covered_aspects = derive_covered_aspects(programme_unit, knowledge)

    assert len(required_aspects) == 8
    assert covered_aspects == required_aspects[:2]
    assert covered_aspects != required_aspects


def test_identity_and_electronic_signature_casuistic_uses_multiple_canonical_sources() -> None:
    programme_unit = real_identity_and_electronic_signature_programme_unit()
    repository = InMemoryKnowledgeRepository()

    needs = derive_knowledge_needs_for_programme_unit(programme_unit)
    assert len(needs) == 1
    assert needs[0].topic == "Identidad y firma electrónica"
    assert needs[0].depth == 1
    assert needs[0].identity_key == (
        "Identidad y firma electrónica",
        1,
    )

    knowledge = generate_study_material_for_programme_unit(
        programme_unit,
        needs[0],
        repository,
    )

    assert knowledge.title == needs[0].topic
    assert knowledge.identity_key == needs[0].identity_key
    assert knowledge.description
    assert len(knowledge.sources) == 4
    assert {source.locator for source in knowledge.sources} == {
        "https://eur-lex.europa.eu/eli/reg/2014/910/oj/spa",
        "https://www.boe.es/buscar/act.php?id=BOE-A-2020-14046",
        "https://www.boe.es/eli/es/rd/2025/04/01/255",
        "https://www.boe.es/buscar/act.php?id=BOE-A-2021-5032",
    }
    assert repository.get_by_identity(needs[0].identity_key) is knowledge

    required_aspects = derive_required_aspects_for_programme_unit(programme_unit)
    covered_aspects = derive_covered_aspects(programme_unit, knowledge)

    assert len(required_aspects) == 6
    assert covered_aspects == required_aspects


def test_personal_data_protection_casuistic_requires_principles_rights_and_obligations() -> None:
    programme_unit = real_personal_data_protection_programme_unit()
    repository = InMemoryKnowledgeRepository()

    needs = derive_knowledge_needs_for_programme_unit(programme_unit)
    assert len(needs) == 1
    assert needs[0].topic == "Protección de datos personales"
    assert needs[0].depth == 1
    assert needs[0].identity_key == (
        "Protección de datos personales",
        1,
    )

    knowledge = generate_study_material_for_programme_unit(
        programme_unit,
        needs[0],
        repository,
    )

    assert knowledge.title == needs[0].topic
    assert knowledge.identity_key == needs[0].identity_key
    assert knowledge.description
    assert len(knowledge.sources) == 2
    assert {source.locator for source in knowledge.sources} == {
        "https://eur-lex.europa.eu/eli/reg/2016/679/oj/spa",
        "https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673",
    }
    assert repository.get_by_identity(needs[0].identity_key) is knowledge

    required_aspects = derive_required_aspects_for_programme_unit(programme_unit)
    covered_aspects = derive_covered_aspects(programme_unit, knowledge)

    assert required_aspects == (
        "Principios del tratamiento de datos personales",
        "Derechos de las personas",
        "Obligaciones y responsabilidad del responsable y encargado del tratamiento",
    )
    assert covered_aspects == required_aspects


def real_data_modelling_programme_unit() -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        number=1,
        title=(
            "Modelado de datos, metodologías y reglas. Entidades, atributos y relaciones."
        ),
        start_page=1,
        start_order=1,
        end_page=1,
        end_order=2,
    )


def test_data_modelling_casuistic_represents_structured_technical_concepts() -> None:
    programme_unit = real_data_modelling_programme_unit()
    repository = InMemoryKnowledgeRepository()

    needs = derive_knowledge_needs_for_programme_unit(programme_unit)
    assert len(needs) == 1
    assert needs[0].topic == "Modelado de datos"
    assert needs[0].depth == 1
    assert needs[0].identity_key == (
        "Modelado de datos",
        1,
    )

    knowledge = generate_study_material_for_programme_unit(
        programme_unit,
        needs[0],
        repository,
    )

    assert knowledge.title == needs[0].topic
    assert knowledge.identity_key == needs[0].identity_key
    assert knowledge.description
    assert len(knowledge.sources) >= 1
    assert repository.get_by_identity(needs[0].identity_key) is knowledge

    required_aspects = derive_required_aspects_for_programme_unit(programme_unit)
    covered_aspects = derive_covered_aspects(programme_unit, knowledge)

    assert required_aspects == (
        "Entidades",
        "Atributos",
        "Relaciones",
        "Metodologías y reglas de modelado",
    )
    assert covered_aspects == required_aspects


def test_data_modelling_study_content_explains_required_technical_concepts() -> None:
    programme_unit = real_data_modelling_programme_unit()
    repository = InMemoryKnowledgeRepository()
    need = derive_knowledge_needs_for_programme_unit(programme_unit)[0]

    knowledge = generate_study_material_for_programme_unit(
        programme_unit,
        need,
        repository,
    )

    content = knowledge.description.casefold()

    assert "entidad" in content
    assert "tipo de entidad" in content

    assert "atributo" in content
    assert "propiedad" in content

    assert "relación" in content
    assert "cardinalidad" in content

    assert "metodología" in content
    assert "regla" in content
    assert "consistencia" in content
