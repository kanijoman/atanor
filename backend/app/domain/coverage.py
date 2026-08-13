from enum import Enum

from app.domain.models import KnowledgeNeed


class CoverageStatus(Enum):
    COVERED = "covered"
    MISSING = "missing"


def evaluate_coverage(knowledge_need: KnowledgeNeed) -> CoverageStatus:
    if knowledge_need.knowledge is None:
        return CoverageStatus.MISSING

    return CoverageStatus.COVERED
