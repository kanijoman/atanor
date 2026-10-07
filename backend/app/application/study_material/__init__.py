"""Candidate study material: curated topics, coverage contract and application services."""

from app.application.study_material.coverage import (
    StudyCoverageSummary,
    build_study_coverage_summary,
)
from app.application.study_material.providers import (
    MaterialOrigin,
    MaterialProvenance,
    MaterialUnavailableError,
    ReviewStatus,
)
from app.application.study_material.service import (
    KnowledgeRepository,
    derive_covered_aspects,
    derive_knowledge_needs_for_programme_unit,
    derive_material_provenance,
    derive_required_aspects_for_programme_unit,
    generate_material_for_need,
    generate_study_material_for_programme_unit,
    is_study_material_available_for_programme_unit,
    prepare_programme_unit_for_study,
)

__all__ = [
    "KnowledgeRepository",
    "MaterialOrigin",
    "MaterialProvenance",
    "MaterialUnavailableError",
    "ReviewStatus",
    "StudyCoverageSummary",
    "build_study_coverage_summary",
    "derive_covered_aspects",
    "derive_knowledge_needs_for_programme_unit",
    "derive_material_provenance",
    "derive_required_aspects_for_programme_unit",
    "generate_material_for_need",
    "generate_study_material_for_programme_unit",
    "is_study_material_available_for_programme_unit",
    "prepare_programme_unit_for_study",
]
