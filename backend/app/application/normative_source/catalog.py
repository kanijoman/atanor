"""Authoritative normative sources Atanor knows how to resolve."""

from dataclasses import dataclass
from typing import Protocol

from app.domain.models import Source


@dataclass(frozen=True)
class NormativeSourceCandidate:
    source: Source
    authority: str
    identifier: str


class NormativeSourceResolver(Protocol):
    def resolve(self, text: str) -> NormativeSourceCandidate | None: ...


LEY_39_2015 = NormativeSourceCandidate(
    source=Source(
        title=(
            "Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo "
            "Común de las Administraciones Públicas"
        ),
        locator="https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565",
    ),
    authority="BOE",
    identifier="BOE-A-2015-10565",
)

LEY_19_2013 = NormativeSourceCandidate(
    source=Source(
        title=(
            "Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la "
            "información pública y buen gobierno"
        ),
        locator="https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887",
    ),
    authority="BOE",
    identifier="BOE-A-2013-12887",
)


CONSTITUCION_ESPANOLA = NormativeSourceCandidate(
    source=Source(
        title="Constitución Española",
        locator="https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229",
    ),
    authority="BOE",
    identifier="BOE-A-1978-31229",
)


def normalize(value: str) -> str:
    return " ".join(value.casefold().split())


class OfficialNormativeSourceCatalog:
    """Resolve supported normative references to authoritative source locators."""

    _ENTRIES = (
        (
            (
                "ley 39/2015",
                "procedimiento administrativo comun",
                "procedimiento administrativo común",
            ),
            LEY_39_2015,
        ),
        (
            (
                "ley 19/2013",
                "transparencia",
                "acceso a la informacion publica",
                "acceso a la información pública",
            ),
            LEY_19_2013,
        ),
        (("constitución española", "constitucion espanola"), CONSTITUCION_ESPANOLA),
    )

    def resolve(self, text: str) -> NormativeSourceCandidate | None:
        normalized_text = normalize(text)
        for aliases, candidate in self._ENTRIES:
            if any(normalize(alias) in normalized_text for alias in aliases):
                return candidate
        return None
