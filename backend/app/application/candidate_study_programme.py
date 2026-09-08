"""Candidate-oriented study programme application services."""


class CandidateStudyProgrammeUnit:
    """Candidate-oriented view of a study programme unit."""

    def __init__(self, unit, knowledge_needs):
        self.number = unit.number
        self.title = unit.title
        self.knowledge_needs = knowledge_needs
        self.covered_knowledge_needs = tuple(
            need for need in knowledge_needs if need.knowledge is not None
        )
        self.missing_knowledge_needs = tuple(
            need for need in knowledge_needs if need.knowledge is None
        )


def get_candidate_study_map(programme, requirements):
    result = []
    for unit in programme.units:
        knowledge_needs = []
        for requirement in requirements:
            for scope in requirement.scopes:
                if scope.context == unit.title:
                    for need in scope.knowledge_needs:
                        if need not in knowledge_needs:
                            knowledge_needs.append(need)
        result.append(
            CandidateStudyProgrammeUnit(unit, tuple(knowledge_needs))
        )

    return tuple(result)
