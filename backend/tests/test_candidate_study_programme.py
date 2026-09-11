from app.application.candidate_study_programme import get_candidate_study_map
from app.domain.models import (
    Call,
    Knowledge,
    KnowledgeNeed,
    Requirement,
    RequirementScope,
    Source,
    StudyProgramme,
    StudyProgrammeUnit,
)


def test_build_candidate_study_map_preserves_programme_units_and_knowledge_coverage() -> None:
    source = Source(title="Examination call", locator="call.pdf")
    call = Call(title="Examination call", source_id=source.id)
    programme = StudyProgramme(
        call_id=call.id,
        identifier="I",
        title="Study programme",
        units=(
            StudyProgrammeUnit(1, "Constitutional law", 10, 100, 12, 120),
            StudyProgrammeUnit(2, "Administrative law", 13, 130, 15, 150),
        ),
    )
    constitutional_need = KnowledgeNeed(
        topic="Constitutional principles", depth=2,
        knowledge=Knowledge(title="Constitutional principles", description="Knowledge about constitutional principles", sources=(source,)),
    )
    administrative_need = KnowledgeNeed(topic="Administrative organization", depth=1)
    requirements = (
        Requirement(title="Constitutional law", source_id=source.id, scopes=(RequirementScope(context="Constitutional law", knowledge_needs=(constitutional_need,)),)),
        Requirement(title="Administrative law", source_id=source.id, scopes=(RequirementScope(context="Administrative law", knowledge_needs=(administrative_need,)),)),
    )
    result = get_candidate_study_map(programme, requirements)
    assert [unit.number for unit in result] == [1, 2]
    assert [unit.title for unit in result] == ["Constitutional law", "Administrative law"]
    assert [need.topic for need in result[0].covered_knowledge_needs] == ["Constitutional principles"]
    assert result[0].missing_knowledge_needs == ()
    assert result[1].covered_knowledge_needs == ()
    assert [need.topic for need in result[1].missing_knowledge_needs] == ["Administrative organization"]


def test_build_candidate_study_map_aggregates_requirements_by_scope_context() -> None:
    source = Source(title="Examination call", locator="call.pdf")
    call = Call(title="Examination call", source_id=source.id)
    programme = StudyProgramme(call_id=call.id, identifier="I", title="Study programme", units=(StudyProgrammeUnit(1, "Administrative procedure", 10, 100, 12, 120),))
    procedure_need = KnowledgeNeed(topic="Administrative procedure acts", depth=2, knowledge=Knowledge(title="Administrative procedure acts", description="Knowledge about administrative procedure acts", sources=(source,)))
    deadlines_need = KnowledgeNeed(topic="Administrative deadlines", depth=1)
    result = get_candidate_study_map(programme, (
        Requirement(title="Law 39/2015", source_id=source.id, scopes=(RequirementScope(context="Administrative procedure", knowledge_needs=(procedure_need,)),)),
        Requirement(title="Regulatory deadlines", source_id=source.id, scopes=(RequirementScope(context="Administrative procedure", knowledge_needs=(deadlines_need,)),)),
    ))
    assert [need.topic for need in result[0].knowledge_needs] == ["Administrative procedure acts", "Administrative deadlines"]
    assert [need.topic for need in result[0].covered_knowledge_needs] == ["Administrative procedure acts"]
    assert [need.topic for need in result[0].missing_knowledge_needs] == ["Administrative deadlines"]


def test_build_candidate_study_map_allows_one_requirement_to_cover_multiple_units() -> None:
    source = Source(title="Examination call", locator="call.pdf")
    call = Call(title="Examination call", source_id=source.id)
    programme = StudyProgramme(call_id=call.id, identifier="I", title="Study programme", units=(StudyProgrammeUnit(1, "Administrative acts", 10, 100, 12, 120), StudyProgrammeUnit(2, "Administrative appeals", 13, 130, 15, 150)))
    acts_need = KnowledgeNeed(topic="Administrative acts", depth=2, knowledge=Knowledge(title="Administrative acts", description="Knowledge about administrative acts", sources=(source,)))
    appeals_need = KnowledgeNeed(topic="Administrative appeals", depth=2)
    result = get_candidate_study_map(programme, (Requirement(title="Law 39/2015", source_id=source.id, scopes=(RequirementScope(context="Administrative acts", knowledge_needs=(acts_need,)), RequirementScope(context="Administrative appeals", knowledge_needs=(appeals_need,)))),))
    assert [need.topic for need in result[0].knowledge_needs] == ["Administrative acts"]
    assert [need.topic for need in result[0].covered_knowledge_needs] == ["Administrative acts"]
    assert result[0].missing_knowledge_needs == ()
    assert [need.topic for need in result[1].knowledge_needs] == ["Administrative appeals"]
    assert result[1].covered_knowledge_needs == ()
    assert [need.topic for need in result[1].missing_knowledge_needs] == ["Administrative appeals"]


def test_build_candidate_study_map_preserves_units_without_matching_knowledge_needs() -> None:
    source = Source(title="Examination call", locator="call.pdf")
    call = Call(title="Examination call", source_id=source.id)
    programme = StudyProgramme(call_id=call.id, identifier="I", title="Study programme", units=(StudyProgrammeUnit(1, "Constitutional law", 10, 100, 12, 120), StudyProgrammeUnit(2, "Unmapped subject", 13, 130, 15, 150)))
    need = KnowledgeNeed(topic="Constitutional principles", depth=2, knowledge=Knowledge(title="Constitutional principles", description="Knowledge about constitutional principles", sources=(source,)))
    result = get_candidate_study_map(programme, (Requirement(title="Constitutional law", source_id=source.id, scopes=(RequirementScope(context="Constitutional law", knowledge_needs=(need,)),)),))
    assert [unit.title for unit in result] == ["Constitutional law", "Unmapped subject"]
    assert result[1].knowledge_needs == ()
    assert result[1].covered_knowledge_needs == ()
    assert result[1].missing_knowledge_needs == ()


def test_build_candidate_study_map_deduplicates_repeated_knowledge_needs() -> None:
    source = Source(title="Examination call", locator="call.pdf")
    call = Call(title="Examination call", source_id=source.id)
    programme = StudyProgramme(call_id=call.id, identifier="I", title="Study programme", units=(StudyProgrammeUnit(1, "Administrative procedure", 10, 100, 12, 120),))
    need = KnowledgeNeed(topic="Administrative deadlines", depth=1)
    result = get_candidate_study_map(programme, (
        Requirement(title="Law 39/2015", source_id=source.id, scopes=(RequirementScope(context="Administrative procedure", knowledge_needs=(need,)),)),
        Requirement(title="Regulatory deadlines", source_id=source.id, scopes=(RequirementScope(context="Administrative procedure", knowledge_needs=(need,)),)),
    ))
    assert [item.topic for item in result[0].knowledge_needs] == ["Administrative deadlines"]
    assert [item.topic for item in result[0].missing_knowledge_needs] == ["Administrative deadlines"]


def test_build_candidate_study_map_deduplicates_equivalent_knowledge_needs() -> None:
    source = Source(title="Examination call", locator="call.pdf")
    call = Call(title="Examination call", source_id=source.id)
    programme = StudyProgramme(call_id=call.id, identifier="I", title="Study programme", units=(StudyProgrammeUnit(1, "Administrative procedure", 10, 100, 12, 120),))
    first = KnowledgeNeed(topic="Administrative deadlines", depth=1)
    second = KnowledgeNeed(topic="Administrative deadlines", depth=1)
    result = get_candidate_study_map(programme, (
        Requirement(title="Law 39/2015", source_id=source.id, scopes=(RequirementScope(context="Administrative procedure", knowledge_needs=(first,)),)),
        Requirement(title="Regulatory deadlines", source_id=source.id, scopes=(RequirementScope(context="Administrative procedure", knowledge_needs=(second,)),)),
    ))
    assert [item.topic for item in result[0].knowledge_needs] == ["Administrative deadlines"]
