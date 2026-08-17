from dataclasses import dataclass

from app.application.requirement_workflow import (
    StudyRequirementSet,
    get_study_requirements,
)
from app.application.requirements import RequirementRepository
from app.domain.models import KnowledgeNeed, Requirement, Source


@dataclass(frozen=True)
class RequirementCoverage:
    requirement: Requirement
    covered: bool


@dataclass(frozen=True)
class StudyCoverage:
    study_requirements: StudyRequirementSet
    items: tuple[RequirementCoverage, ...]

    @property
    def total(self) -> int:
        return len(self.items)

    @property
    def covered(self) -> int:
        return sum(item.covered for item in self.items)

    @property
    def missing(self) -> int:
        return self.total - self.covered

    @property
    def coverage_percentage(self) -> float:
        if self.total == 0:
            return 0.0
        return self.covered / self.total * 100


def get_study_coverage(
    source: Source,
    repository: RequirementRepository,
) -> StudyCoverage:
    """Evaluate available knowledge for the requirements of a source."""
    study_requirements = get_study_requirements(source, repository)
    items = tuple(
        RequirementCoverage(
            requirement=requirement,
            covered=_is_covered(requirement),
        )
        for requirement in study_requirements.requirements
    )
    return StudyCoverage(
        study_requirements=study_requirements,
        items=items,
    )


def _is_covered(requirement: Requirement) -> bool:
    knowledge_needs = _knowledge_needs(requirement)
    return bool(knowledge_needs) and all(
        knowledge_need.knowledge is not None
        for knowledge_need in knowledge_needs
    )


def _knowledge_needs(requirement: Requirement) -> tuple[KnowledgeNeed, ...]:
    return tuple(
        knowledge_need
        for scope in requirement.scopes
        for knowledge_need in scope.knowledge_needs
    )
