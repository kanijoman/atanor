from app.application.candidate_study_programme import (
    get_candidate_study_map,
)
from app.domain.models import (
    Knowledge,
    KnowledgeNeed,
    Requirement,
    RequirementScope,
    Source,
    StudyProgramme,
    StudyProgrammeUnit,
)


def test_build_candidate_study_map_from_programme_requirements() -> None:
    source = Source(
        title="Examination call",
        locator="call.pdf",
    )

    programme = StudyProgramme(
        source_id=source.id,
        identifier="I",
        title="Study programme",
        units=(
            StudyProgrammeUnit(
                number=1,
                title="Constitutional law",
                start_page=10,
                start_order=100,
                end_page=12,
                end_order=120,
            ),
            StudyProgrammeUnit(
                number=2,
                title="Administrative law",
                start_page=13,
                start_order=121,
                end_page=15,
                end_order=140,
            ),
        ),
    )

    covered_knowledge = Knowledge(
        title="Spanish Constitution",
        description="Knowledge about the Spanish Constitution",
        sources=(source,),
    )

    constitutional_need = KnowledgeNeed(
        topic="Spanish Constitution",
        depth=2,
        knowledge=covered_knowledge,
    )
    constitutional_missing_need = KnowledgeNeed(
        topic="Constitutional guarantees",
        depth=2,
    )
    administrative_need = KnowledgeNeed(
        topic="Administrative procedure",
        depth=1,
        knowledge=Knowledge(
            title="Administrative procedure",
            description="Knowledge about administrative procedure",
            sources=(source,),
        ),
    )

    constitutional_requirement = Requirement(
        title="Constitutional law",
        source_id=source.id,
        scopes=(
            RequirementScope(
                context="Constitutional law",
                knowledge_needs=(
                    constitutional_need,
                    constitutional_missing_need,
                ),
            ),
        ),
    )
    administrative_requirement = Requirement(
        title="Administrative law",
        source_id=source.id,
        scopes=(
            RequirementScope(
                context="Administrative law",
                knowledge_needs=(administrative_need,),
            ),
        ),
    )

    result = get_candidate_study_map(
        programme,
        (
            constitutional_requirement,
            administrative_requirement,
        ),
    )

    assert [unit.number for unit in result] == [1, 2]

    assert result[0].title == "Constitutional law"
    assert [need.topic for need in result[0].knowledge_needs] == [
        "Spanish Constitution",
        "Constitutional guarantees",
    ]
    assert [need.topic for need in result[0].covered_knowledge_needs] == [
        "Spanish Constitution",
    ]
    assert [need.topic for need in result[0].missing_knowledge_needs] == [
        "Constitutional guarantees",
    ]

    assert result[1].title == "Administrative law"
    assert [need.topic for need in result[1].knowledge_needs] == [
        "Administrative procedure",
    ]
    assert [need.topic for need in result[1].covered_knowledge_needs] == [
        "Administrative procedure",
    ]
    assert result[1].missing_knowledge_needs == ()


def test_build_candidate_study_map_aggregates_requirements_by_scope_context() -> None:
    source = Source(
        title="Examination call",
        locator="call.pdf",
    )

    programme = StudyProgramme(
        source_id=source.id,
        identifier="I",
        title="Study programme",
        units=(
            StudyProgrammeUnit(
                number=1,
                title="Administrative procedure",
                start_page=10,
                start_order=100,
                end_page=12,
                end_order=120,
            ),
        ),
    )

    procedure_need = KnowledgeNeed(
        topic="Administrative procedure acts",
        depth=2,
        knowledge=Knowledge(
            title="Administrative procedure acts",
            description="Knowledge about administrative procedure acts",
            sources=(source,),
        ),
    )
    deadlines_need = KnowledgeNeed(
        topic="Administrative deadlines",
        depth=1,
    )

    procedure_requirement = Requirement(
        title="Law 39/2015",
        source_id=source.id,
        scopes=(
            RequirementScope(
                context="Administrative procedure",
                knowledge_needs=(procedure_need,),
            ),
        ),
    )
    deadlines_requirement = Requirement(
        title="Regulatory deadlines",
        source_id=source.id,
        scopes=(
            RequirementScope(
                context="Administrative procedure",
                knowledge_needs=(deadlines_need,),
            ),
        ),
    )

    result = get_candidate_study_map(
        programme,
        (
            procedure_requirement,
            deadlines_requirement,
        ),
    )

    assert [need.topic for need in result[0].knowledge_needs] == [
        "Administrative procedure acts",
        "Administrative deadlines",
    ]
    assert [need.topic for need in result[0].covered_knowledge_needs] == [
        "Administrative procedure acts",
    ]
    assert [need.topic for need in result[0].missing_knowledge_needs] == [
        "Administrative deadlines",
    ]
