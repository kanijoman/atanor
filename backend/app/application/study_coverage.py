from dataclasses import dataclass

from app.application.requirement_workflow import StudyRequirementSet
from app.domain.models import KnowledgeNeed, Requirement


@dataclass(frozen=True)
class RequirementCoverage:
    requirement: Requirement
    covered: bool


@dataclass(frozen=True)
class StudyCoverage:
    study_requirements: StudyRequirementSet
    covered: tuple[RequirementCoverage, ...]
    missing: tuple[RequirementCoverage, ...]

    @property
    def total(self) -> int:
        return len(self.covered) + len(self.missing)

    @property
    def coverage_percentage(self) -> float:
        if self.total == 0:
            return 0.0
        return len(self.covered) / self.total * 100


def get_study_coverage(study_requirements: StudyRequirementSet) -> StudyCoverage:
    """Evaluate available knowledge for each study requirement."""
    covered: list[RequirementCoverage] = []
    missing: list[RequirementCoverage] = []

    for requirement in study_requirements.requirements:
        knowledge_needs = _knowledge_needs(requirement)
        is_covered = bool(knowledge_needs) and all(
            knowledge_need.knowledge is not None
            for knowledge_need in knowledge_needs
        )
        coverage = RequirementCoverage(requirement=requirement, covered=is_covered)

        if is_covered:
            covered.append(coverage)
        else:
            missing.append(coverage)

    return StudyCoverage(
        study_requirements=study_requirements,
        covered=tuple(covered),
        missing=tuple(missing),
    )


def _knowledge_needs(requirement: Requirement) -> tuple[KnowledgeNeed, ...]:
    return tuple(
        knowledge_need
        for scope in requirement.scopes
        for knowledge_need in scope.knowledge_needs
    )
