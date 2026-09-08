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
    requirement_by_title = {requirement.title: requirement for requirement in requirements}

    result = []
    for unit in programme.units:
        requirement = requirement_by_title.get(unit.title)
        if requirement is None:
            knowledge_needs = ()
        else:
            knowledge_needs = tuple(
                need
                for scope in requirement.scopes
                for need in scope.knowledge_needs
            )
        result.append(CandidateStudyProgrammeUnit(unit, knowledge_needs))

    return tuple(result)
