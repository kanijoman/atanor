from dataclasses import dataclass

import pytest

from app.application.normative_source import (
    OfficialNormativeSourceCatalog,
    RetrievedSource,
    acquire_normative_source,
)
from app.domain.models import Source


@dataclass(frozen=True)
class FakeRetriever:
    content: str

    def retrieve(self, candidate):
        return RetrievedSource(candidate=candidate, content=self.content)


def test_catalog_resolves_ley_39_2015_from_programme_requirement() -> None:
    resolver = OfficialNormativeSourceCatalog()

    candidate = resolver.resolve(
        "Las Leyes del Procedimiento Administrativo Común de las Administraciones"
    )

    assert candidate is not None
    assert candidate.authority == "BOE"
    assert candidate.identifier == "BOE-A-2015-10565"
    assert candidate.source == Source(
        title=(
            "Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo "
            "Común de las Administraciones Públicas"
        ),
        locator="https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565",
    )


def test_catalog_resolves_ley_19_2013_from_knowledge_need() -> None:
    resolver = OfficialNormativeSourceCatalog()

    candidate = resolver.resolve("Derecho de acceso a la información pública")

    assert candidate is not None
    assert candidate.identifier == "BOE-A-2013-12887"


def test_catalog_returns_no_candidate_for_unsupported_open_knowledge() -> None:
    resolver = OfficialNormativeSourceCatalog()

    assert resolver.resolve("Programación orientada a objetos") is None


def test_acquisition_retrieves_content_after_source_resolution() -> None:
    retrieved = acquire_normative_source(
        "Las Leyes del Procedimiento Administrativo Común de las Administraciones",
        OfficialNormativeSourceCatalog(),
        FakeRetriever("<html>Artículo 1. Objeto de la Ley.</html>"),
    )

    assert retrieved.candidate.identifier == "BOE-A-2015-10565"
    assert "Artículo 1" in retrieved.content


def test_acquisition_requires_a_supported_source() -> None:
    with pytest.raises(ValueError, match="No supported normative source"):
        acquire_normative_source(
            "Programación orientada a objetos",
            OfficialNormativeSourceCatalog(),
            FakeRetriever("unused"),
        )
