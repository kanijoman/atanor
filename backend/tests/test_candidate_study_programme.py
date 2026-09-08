from app.application.candidate_study_programme import get_candidate_study_map
from app.domain.models import (
    Knowledge,
    KnowledgeNeed,
    Requirement,
    RequirementScope,
    Source,
    StudyProgramme,
    StudyProgrammeUnit,
)


def test_build_candidate_study_map_preserves_programme_units_and_knowledge_coverage() -> None:
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
                start_order=130,
                end_page=15,
                end_order=150,
            ),
        ),
    )

    constitutional_need = KnowledgeNeed(
        topic="Constitutional principles",
        depth=2,
        knowledge=Knowledge(
            title="Constitutional principles",
            description="Knowledge about constitutional principles",
            sources=(source,),
        ),
    )
    administrative_need = KnowledgeNeed(
        topic="Administrative organization",
        depth=1,
    )

    requirements = (
        Requirement(
            title="Constitutional law",
            source_id=source.id,
            scopes=(
                RequirementScope(
                    context="Constitutional law",
                    knowledge_needs=(constitutional_need,),
                ),
            ),
        ),
        Requirement(
            title="Administrative law",
            source_id=source.id,
            scopes=(
                RequirementScope(
                    context="Administrative law",
                    knowledge_needs=(administrative_need,),
                ),
            ),
        ),
    )

    result = get_candidate_study_map(programme, requirements)

    assert [unit.number for unit in result] == [1, 2]
    assert [unit.title for unit in result] == [
        "Constitutional law",
        "Administrative law",
    ]
    assert [need.topic for need in result[0].covered_knowledge_needs] == [
        "Constitutional principles",
    ]
    assert [need.topic for need in result[0].missing_knowledge_needs] == []
    assert [need.topic for need in result[1].covered_knowledge_needs] == []
    assert [need.topic for need in result[1].missing_knowledge_needs] == [
        "Administrative organization",
    ]


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


def test_build_candidate_study_map_allows_one_requirement_to_cover_multiple_units() -> None:
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
                title="Administrative acts",
                start_page=10,
                start_order=100,
                end_page=12,
                end_order=120,
            ),
            StudyProgrammeUnit(
                number=2,
                title="Administrative appeals",
                start_page=13,
                start_order=130,
                end_page=15,
                end_order=150,
            ),
        ),
    )

    acts_need = KnowledgeNeed(
        topic="Administrative acts",
        depth=2,
        knowledge=Knowledge(
            title="Administrative acts",
            description="Knowledge about administrative acts",
            sources=(source,),
        ),
    )
    appeals_need = KnowledgeNeed(
        topic="Administrative appeals",
        depth=2,
    )

    requirement = Requirement(
        title="Law 39/2015",
        source_id=source.id,
        scopes=(
            RequirementScope(
                context="Administrative acts",
                knowledge_needs=(acts_need,),
            ),
            RequirementScope(
                context="Administrative appeals",
                knowledge_needs=(appeals_need,),
            ),
        ),
    )

    result = get_candidate_study_map(
        programme,
        (requirement,),
    )

    assert [need.topic for need in result[0].knowledge_needs] == [
        "Administrative acts",
    ]
    assert [need.topic for need in result[0].covered_knowledge_needs] == [
        "Administrative acts",
    ]
    assert result[0].missing_knowledge_needs == ()

    assert [need.topic for need in result[1].knowledge_needs] == [
        "Administrative appeals",
    ]
    assert result[1].covered_knowledge_needs == ()
    assert [need.topic for need in result[1].missing_knowledge_needs] == [
        "Administrative appeals",
    ]


def test_build_candidate_study_map_preserves_units_without_matching_knowledge_needs() -> None:
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
                title="Unmapped subject",
                start_page=13,
                start_order=130,
                end_page=15,
                end_order=150,
            ),
        ),
    )

    constitutional_need = KnowledgeNeed(
        topic="Constitutional principles",
        depth=2,
        knowledge=Knowledge(
            title="Constitutional principles",
            description="Knowledge about constitutional principles",
            sources=(source,),
        ),
    )
    requirement = Requirement(
        title="Constitutional law",
        source_id=source.id,
        scopes=(
            RequirementScope(
                context="Constitutional law",
                knowledge_needs=(constitutional_need,),
            ),
        ),
    )

    result = get_candidate_study_map(programme, (requirement,))

    assert [unit.title for unit in result] == [
        "Constitutional law",
        "Unmapped subject",
    ]
    assert result[1].knowledge_needs == ()
    assert result[1].covered_knowledge_needs == ()
    assert result[1].missing_knowledge_needs == ()


def test_build_candidate_study_map_deduplicates_repeated_knowledge_needs() -> None:
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

    shared_need = KnowledgeNeed(
        topic="Administrative deadlines",
        depth=1,
    )
    requirements = (
        Requirement(
            title="Law 39/2015",
            source_id=source.id,
            scopes=(
                RequirementScope(
                    context="Administrative procedure",
                    knowledge_needs=(shared_need,),
                ),
            ),
        ),
        Requirement(
            title="Regulatory deadlines",
            source_id=source.id,
            scopes=(
                RequirementScope(
                    context="Administrative procedure",
                    knowledge_needs=(shared_need,),
                ),
            ),
        ),
    )

    result = get_candidate_study_map(programme, requirements)

    assert [need.topic for need in result[0].knowledge_needs] == [
        "Administrative deadlines",
    ]
    assert [need.topic for need in result[0].missing_knowledge_needs] == [
        "Administrative deadlines",
    ]


def test_build_candidate_study_map_deduplicates_equivalent_knowledge_needs() -> None:
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

    first_need = KnowledgeNeed(
        topic="Administrative deadlines",
        depth=1,
    )
    second_need = KnowledgeNeed(
        topic="Administrative deadlines",
        depth=1,
    )
    requirements = (
        Requirement(
            title="Law 39/2015",
            source_id=source.id,
            scopes=(
                RequirementScope(
                    context="Administrative procedure",
                    knowledge_needs=(first_need,),
                ),
            ),
        ),
        Requirement(
            title="Regulatory deadlines",
            source_id=source.id,
            scopes=(
                RequirementScope(
                    context="Administrative procedure",
                    knowledge_needs=(second_need,),
                ),
            ),
        ),
    )

    result = get_candidate_study_map(programme, requirements)

    assert [need.topic for need in result[0].knowledge_needs] == [
        "Administrative deadlines",
    ]
