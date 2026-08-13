from uuid import uuid4

import pytest

from app.domain.models import Knowledge, KnowledgeNeed, Requirement, RequirementScope, Source


def test_requirement_can_define_multiple_contextual_scopes() -> None:
    source = Source(title="Examination call")
    requirement = Requirement(title="Operating Systems", source_id=source.id)
    general_scope = RequirementScope(context="General Administration")
    technical_scope = RequirementScope(context="Information Technology")

    requirement = requirement.with_scope(general_scope).with_scope(technical_scope)

    assert requirement.scopes == (general_scope, technical_scope)


def test_same_requirement_can_have_different_scopes() -> None:
    source = Source(title="Examination call")
    requirement = Requirement(title="Operating Systems", source_id=source.id)
    general_scope = RequirementScope(context="General Administration")
    technical_scope = RequirementScope(context="Information Technology")

    assert general_scope != technical_scope
    assert requirement.with_scope(general_scope).scopes != requirement.with_scope(technical_scope).scopes


def test_knowledge_need_can_require_different_depths() -> None:
    processes = Knowledge(title="Processes")
    basic_scope = RequirementScope(context="General Administration")
    technical_scope = RequirementScope(context="Information Technology")

    basic_need = KnowledgeNeed(topic="Processes", depth=2, knowledge=processes)
    technical_need = KnowledgeNeed(topic="Processes", depth=4, knowledge=processes)
    basic_scope = basic_scope.requires(basic_need)
    technical_scope = technical_scope.requires(technical_need)

    assert basic_scope.knowledge_needs[0].depth == 2
    assert technical_scope.knowledge_needs[0].depth == 4
    assert basic_scope.knowledge_needs[0].knowledge is technical_scope.knowledge_needs[0].knowledge


def test_knowledge_need_can_exist_without_available_knowledge() -> None:
    need = KnowledgeNeed(topic="Process synchronization", depth=4)

    assert need.knowledge is None


def test_knowledge_need_does_not_require_a_persisted_knowledge_identifier() -> None:
    need = KnowledgeNeed(topic="Process synchronization", depth=4)

    assert need.knowledge_id is None
    assert need.id is not None


def test_requirement_scopes_are_independent_of_available_knowledge() -> None:
    source = Source(title="Examination call")
    requirement = Requirement(title="Operating Systems", source_id=source.id)
    scope = RequirementScope(context="Information Technology").requires(
        KnowledgeNeed(topic="Process synchronization", depth=4)
    )

    requirement = requirement.with_scope(scope)
    assert requirement.scopes[0].knowledge_needs[0].knowledge is None


def test_scope_ids_are_unique() -> None:
    first = RequirementScope(context="Information Technology")
    second = RequirementScope(context="Information Technology")

    assert first.id != second.id
    assert first.id != uuid4()


@pytest.mark.parametrize("depth", [0, -1])
def test_knowledge_need_depth_must_be_positive(depth: int) -> None:
    with pytest.raises(ValueError):
        KnowledgeNeed(topic="Processes", depth=depth)
