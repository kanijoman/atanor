from urllib.error import URLError

import pytest
from support import FixtureSourceRetriever, InMemoryKnowledgeRepository

from app.application.normative_source import NormativeSourceCandidate, RetrievedSource
from app.application.study_material import (
    MaterialOrigin,
    MaterialUnavailableError,
    derive_covered_aspects,
    derive_knowledge_needs_for_programme_unit,
    derive_material_provenance,
    derive_required_aspects_for_programme_unit,
    generate_study_material_for_programme_unit,
)
from app.domain.models import StudyProgrammeUnit

LEY_39_UNIT = StudyProgrammeUnit(
    number=11,
    title="Las Leyes del Procedimiento Administrativo Común de las Administraciones",
    start_page=1,
    start_order=1,
    end_page=1,
    end_order=2,
)


class OfflineRetriever:
    def retrieve(self, candidate: NormativeSourceCandidate) -> RetrievedSource:
        raise URLError("no network")


class StubRetriever:
    """Serves one fixed HTML document for any source."""

    def __init__(self, html: str) -> None:
        self._html = html

    def retrieve(self, candidate: NormativeSourceCandidate) -> RetrievedSource:
        return RetrievedSource(candidate=candidate, content=self._html)


def _material(retriever):
    need = derive_knowledge_needs_for_programme_unit(LEY_39_UNIT)[0]
    return generate_study_material_for_programme_unit(
        LEY_39_UNIT, need, InMemoryKnowledgeRepository(), retriever
    )


def test_acquired_material_is_assembled_from_authoritative_articles() -> None:
    knowledge = _material(FixtureSourceRetriever())

    assert "1. Objeto y finalidad del procedimiento administrativo común" in knowledge.description
    assert "  Artículo 1. Objeto de la Ley." in knowledge.description
    assert "  Artículo 127. " in knowledge.description
    assert knowledge.sources[0].locator == "https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565"


def test_material_for_ley_39_2015_is_labelled_as_acquired_and_unreviewed() -> None:
    provenance = derive_material_provenance(LEY_39_UNIT)

    assert provenance.origin is MaterialOrigin.ACQUIRED
    assert provenance.review_status.value == "unreviewed"


def test_aspect_whose_articles_were_not_acquired_stays_pending() -> None:
    html = (
        "<h5>Artículo 1. Objeto de la Ley.</h5>"
        f"<p>{' '.join(['texto'] * 20)}</p>"
        "<h5>Artículo 2. Ámbito subjetivo de aplicación.</h5>"
        f"<p>{' '.join(['texto'] * 20)}</p>"
    )
    knowledge = _material(StubRetriever(html))

    covered = derive_covered_aspects(LEY_39_UNIT, knowledge)
    required = derive_required_aspects_for_programme_unit(LEY_39_UNIT)

    assert covered == required[:2]


def test_unreachable_source_is_reported_instead_of_inventing_material() -> None:
    with pytest.raises(MaterialUnavailableError):
        _material(OfflineRetriever())


def test_source_without_any_expected_article_is_reported() -> None:
    with pytest.raises(MaterialUnavailableError):
        _material(StubRetriever("<html><body><p>Página sin artículos</p></body></html>"))


def test_acquired_material_is_persisted_so_later_requests_need_no_network() -> None:
    repository = InMemoryKnowledgeRepository()
    need = derive_knowledge_needs_for_programme_unit(LEY_39_UNIT)[0]
    first = generate_study_material_for_programme_unit(
        LEY_39_UNIT, need, repository, FixtureSourceRetriever()
    )

    second = generate_study_material_for_programme_unit(
        LEY_39_UNIT, need, repository, OfflineRetriever()
    )

    assert second is first
