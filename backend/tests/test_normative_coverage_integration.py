from app.application.normative_source import (
    HttpSourceRetriever,
    OfficialNormativeSourceCatalog,
    extract_article,
    reconstruct_knowledge_from_article,
)
from app.application.study_material import (
    build_study_coverage_summary,
    derive_covered_aspects,
    derive_required_aspects_for_programme_unit,
)
from app.domain.models import KnowledgeNeed, StudyProgrammeUnit


def test_acquired_normative_content_feeds_programme_coverage() -> None:
    programme_unit = StudyProgrammeUnit(
        number=11,
        title="Las Leyes del Procedimiento Administrativo Común de las Administraciones",
        start_page=1,
        start_order=1,
        end_page=1,
        end_order=1,
    )

    candidate = OfficialNormativeSourceCatalog().resolve("Ley 39/2015")
    assert candidate is not None

    retrieved = HttpSourceRetriever().retrieve(candidate)
    article = extract_article(retrieved, 1)
    assert article is not None

    acquired = reconstruct_knowledge_from_article(retrieved, article)

    required_aspects = derive_required_aspects_for_programme_unit(programme_unit)
    covered_aspects = derive_covered_aspects(programme_unit, acquired)
    summary = build_study_coverage_summary(
        KnowledgeNeed(topic="Procedimiento administrativo común", depth=1),
        required_aspects,
        covered_aspects,
    )

    assert summary.required_count == 8
    assert summary.covered_aspects == (
        "Objeto y finalidad del procedimiento administrativo común",
    )
    assert summary.covered_count == 1
    assert summary.pending_aspects == required_aspects[1:]
    assert summary.coverage_percentage == 12.5
