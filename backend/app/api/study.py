from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.api.dependencies import (
    KnowledgeRepositoryDep,
    SourceRepositoryDep,
    SourceRetrieverDep,
    StudyProgrammeRepositoryDep,
)
from app.application.programme_coverage import summarize_programme_coverage
from app.application.study_material import (
    MaterialProvenance,
    MaterialUnavailableError,
    StudyCoverageSummary,
    build_study_coverage_summary,
    derive_covered_aspects,
    derive_material_provenance,
    derive_required_aspects_for_programme_unit,
    generate_study_material_for_programme_unit,
    is_study_material_available_for_programme_unit,
)
from app.application.study_needs import ensure_knowledge_needs
from app.domain.models import Knowledge, KnowledgeNeed, StudyProgrammeUnit

router = APIRouter(prefix="/api/study", tags=["study"])


@router.get("/programmes")
def list_programmes(
    source_repository: SourceRepositoryDep,
    programme_repository: StudyProgrammeRepositoryDep,
) -> list[dict[str, object]]:
    return [
        {
            "id": str(programme.id),
            "identifier": programme.identifier,
            "title": programme.title,
        }
        for source in source_repository.list_all()
        for programme in programme_repository.list_by_source(source.id)
    ]


@router.get("/programmes/{programme_id}")
def get_programme(programme_id: UUID, repository: StudyProgrammeRepositoryDep) -> dict[str, object]:
    programme = repository.get_by_id(programme_id)
    if programme is None:
        raise HTTPException(status_code=404, detail="Study programme not found")

    coverage = summarize_programme_coverage(programme)
    return {
        "id": str(programme.id),
        "identifier": programme.identifier,
        "title": programme.title,
        "coverage": {
            "units_total": coverage.units_total,
            "units_with_material": coverage.units_with_material,
        },
        "units": [
            {
                "id": str(unit.id),
                "number": unit.number,
                "title": unit.title,
                "study_material_available": is_study_material_available_for_programme_unit(unit),
            }
            for unit in programme.units
        ],
    }


@router.get("/units/{unit_id}")
def get_study_material(
    unit_id: UUID,
    programme_repository: StudyProgrammeRepositoryDep,
    knowledge_repository: KnowledgeRepositoryDep,
    retriever: SourceRetrieverDep,
) -> dict[str, object]:
    programme_unit = programme_repository.get_unit_by_id(unit_id)
    if programme_unit is None:
        raise HTTPException(status_code=404, detail="Study programme unit not found")

    programme_unit = ensure_knowledge_needs(programme_unit, programme_repository)
    knowledge_need = _single_knowledge_need(programme_unit)
    try:
        knowledge = generate_study_material_for_programme_unit(
            programme_unit, knowledge_need, knowledge_repository, retriever
        )
    except MaterialUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail="Study material is temporarily unavailable; try again later",
        ) from exc
    programme_repository.link_knowledge(knowledge_need.id, knowledge.id)
    coverage = build_study_coverage_summary(
        knowledge_need=knowledge_need,
        required_aspects=derive_required_aspects_for_programme_unit(programme_unit),
        covered_aspects=derive_covered_aspects(programme_unit, knowledge),
    )
    return _study_material_response(
        programme_unit,
        knowledge_need,
        knowledge,
        coverage,
        derive_material_provenance(programme_unit),
    )


def _single_knowledge_need(programme_unit: StudyProgrammeUnit) -> KnowledgeNeed:
    if not is_study_material_available_for_programme_unit(programme_unit):
        raise HTTPException(
            status_code=422,
            detail="Study material is not available for this programme unit",
        )

    knowledge_needs = programme_unit.knowledge_needs
    if len(knowledge_needs) != 1:
        raise HTTPException(
            status_code=422,
            detail="Study material requires exactly one supported knowledge need",
        )
    return knowledge_needs[0]


def _study_material_response(
    programme_unit: StudyProgrammeUnit,
    knowledge_need: KnowledgeNeed,
    knowledge: Knowledge,
    coverage: StudyCoverageSummary,
    provenance: MaterialProvenance,
) -> dict[str, object]:
    return {
        "programme_unit": {
            "id": str(programme_unit.id),
            "number": programme_unit.number,
            "title": programme_unit.title,
        },
        "knowledge_need": {
            "title": knowledge_need.topic,
        },
        "provenance": {
            "origin": provenance.origin.value,
            "review_status": provenance.review_status.value,
        },
        "study_material": knowledge.description or "",
        "sources": [
            {
                "title": source.title,
                "locator": source.locator,
            }
            for source in knowledge.sources
        ],
        "coverage": {
            "status": coverage.status,
            "covered_count": coverage.covered_count,
            "required_count": coverage.required_count,
            "coverage_percentage": coverage.coverage_percentage,
            "required_aspects": list(coverage.required_aspects),
            "covered_aspects": list(coverage.covered_aspects),
            "pending_aspects": list(coverage.pending_aspects),
        },
    }
