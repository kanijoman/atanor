"""Candidate-oriented study programme application services."""

from collections.abc import Sequence

from app.domain.models import KnowledgeNeed, Requirement, StudyProgramme, StudyProgrammeUnit


class CandidateStudyProgrammeUnit:
    """Candidate-oriented view of a study programme unit."""

    def __init__(self, unit: StudyProgrammeUnit, knowledge_needs: Sequence[KnowledgeNeed]) -> None:
        self.number = unit.number
        self.title = unit.title
        self.knowledge_needs = knowledge_needs
        self.covered_knowledge_needs = tuple(
            need for need in knowledge_needs if need.knowledge is not None
        )
        self.missing_knowledge_needs = tuple(
            need for need in knowledge_needs if need.knowledge is None
        )


def get_candidate_study_map(
    programme: StudyProgramme, requirements: Sequence[Requirement]
) -> tuple[CandidateStudyProgrammeUnit, ...]:
    result = []
    for unit in programme.units:
        knowledge_needs: list[KnowledgeNeed] = []
        knowledge_need_keys: set[tuple[str, int]] = set()
        for requirement in requirements:
            for scope in requirement.scopes:
                if scope.context == unit.title:
                    for need in scope.knowledge_needs:
                        key = (need.topic, need.depth)
                        if key not in knowledge_need_keys:
                            knowledge_need_keys.add(key)
                            knowledge_needs.append(need)
        result.append(CandidateStudyProgrammeUnit(unit, tuple(knowledge_needs)))

    return tuple(result)
