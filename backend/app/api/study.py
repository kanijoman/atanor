from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.application.study_material import (
    build_study_coverage_summary,
    derive_covered_aspects,
    derive_knowledge_needs_for_programme_unit,
    derive_required_aspects_for_programme_unit,
    generate_study_material_for_programme_unit,
    is_study_material_available_for_programme_unit,
)
from app.persistence.database import SessionLocal
from app.persistence.knowledge_repository import SqlAlchemyKnowledgeRepository
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository


router = APIRouter(prefix="/api/study", tags=["study"])


@router.get("/programmes")
def list_programmes() -> list[dict[str, object]]:
    repository = SqlAlchemyStudyProgrammeRepository(SessionLocal)
    programmes = []
    for source in _list_sources():
        for programme in repository.list_by_source(source):
            programmes.append(
                {
                    "id": str(programme.id),
                    "identifier": programme.identifier,
                    "title": programme.title,
                }
            )
    return programmes


@router.get("/programmes/{programme_id}")
def get_programme(programme_id: UUID) -> dict[str, object]:
    repository = SqlAlchemyStudyProgrammeRepository(SessionLocal)
    programme = repository.get_by_id(programme_id)
    if programme is None:
        raise HTTPException(status_code=404, detail="Study programme not found")

    return {
        "id": str(programme.id),
        "identifier": programme.identifier,
        "title": programme.title,
        "units": [
            {
                "id": str(unit.id),
                "number": unit.number,
                "title": unit.title,
                "study_material_available": is_study_material_available_for_programme_unit(
                    unit
                ),
            }
            for unit in programme.units
        ],
    }


@router.get("/units/{unit_id}")
def get_study_material(unit_id: UUID) -> dict[str, object]:
    programme_repository = SqlAlchemyStudyProgrammeRepository(SessionLocal)
    programme_unit = programme_repository.get_unit_by_id(unit_id)
    if programme_unit is None:
        raise HTTPException(status_code=404, detail="Study programme unit not found")

    try:
        knowledge_needs = derive_knowledge_needs_for_programme_unit(programme_unit)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail="Study material is not available for this programme unit",
        ) from exc

    if len(knowledge_needs) != 1:
        raise HTTPException(
            status_code=422,
            detail="Study material requires exactly one supported knowledge need",
        )

    knowledge_need = knowledge_needs[0]
    knowledge_repository = SqlAlchemyKnowledgeRepository(SessionLocal)
    knowledge = generate_study_material_for_programme_unit(
        programme_unit,
        knowledge_need,
        knowledge_repository,
    )

    required_aspects = derive_required_aspects_for_programme_unit(programme_unit)
    covered_aspects = derive_covered_aspects(programme_unit, knowledge)
    coverage = build_study_coverage_summary(
        knowledge_need=knowledge_need,
        required_aspects=required_aspects,
        covered_aspects=covered_aspects,
    )

    return {
        "programme_unit": {
            "id": str(programme_unit.id),
            "number": programme_unit.number,
            "title": programme_unit.title,
        },
        "knowledge_need": {
            "title": knowledge_need.topic,
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
            "covered_aspects": list(coverage.covered_aspects),
            "pending_aspects": list(coverage.pending_aspects),
        },
    }


def _list_sources() -> list[UUID]:
    from app.persistence.source_repository import SqlAlchemySourceRepository

    repository = SqlAlchemySourceRepository(SessionLocal)
    return [source.id for source in repository.list_all()]
