from dataclasses import dataclass
from typing import Protocol
from urllib.request import Request, urlopen

from app.domain.models import Source


@dataclass(frozen=True)
class NormativeSourceCandidate:
    source: Source
    authority: str
    identifier: str


@dataclass(frozen=True)
class RetrievedSource:
    candidate: NormativeSourceCandidate
    content: str


class NormativeSourceResolver(Protocol):
    def resolve(self, text: str) -> NormativeSourceCandidate | None: ...


class SourceRetriever(Protocol):
    def retrieve(self, candidate: NormativeSourceCandidate) -> RetrievedSource: ...


class OfficialNormativeSourceCatalog:
    """Resolve supported normative references to authoritative source locators."""

    _ENTRIES = (
        (
            (
                "ley 39/2015",
                "procedimiento administrativo comun",
                "procedimiento administrativo común",
            ),
            NormativeSourceCandidate(
                source=Source(
                    title=(
                        "Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo "
                        "Común de las Administraciones Públicas"
                    ),
                    locator="https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565",
                ),
                authority="BOE",
                identifier="BOE-A-2015-10565",
            ),
        ),
        (
            (
                "ley 19/2013",
                "transparencia",
                "acceso a la informacion publica",
                "acceso a la información pública",
            ),
            NormativeSourceCandidate(
                source=Source(
                    title=(
                        "Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la "
                        "información pública y buen gobierno"
                    ),
                    locator="https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887",
                ),
                authority="BOE",
                identifier="BOE-A-2013-12887",
            ),
        ),
    )

    def resolve(self, text: str) -> NormativeSourceCandidate | None:
        normalized_text = _normalize(text)
        for aliases, candidate in self._ENTRIES:
            if any(_normalize(alias) in normalized_text for alias in aliases):
                return candidate
        return None


class HttpSourceRetriever:
    """Retrieve authoritative source content without knowing its content in advance."""

    def __init__(self, timeout: float = 20.0) -> None:
        self._timeout = timeout

    def retrieve(self, candidate: NormativeSourceCandidate) -> RetrievedSource:
        if candidate.source.locator is None:
            raise ValueError("Normative source must have a locator")

        request = Request(
            candidate.source.locator,
            headers={"User-Agent": "Atanor/0.1"},
        )
        with urlopen(request, timeout=self._timeout) as response:
            content = response.read().decode(response.headers.get_content_charset() or "utf-8")

        return RetrievedSource(candidate=candidate, content=content)


def acquire_normative_source(
    text: str,
    resolver: NormativeSourceResolver,
    retriever: SourceRetriever,
) -> RetrievedSource:
    """Resolve and retrieve an authoritative normative source."""
    candidate = resolver.resolve(text)
    if candidate is None:
        raise ValueError("No supported normative source could be identified")

    return retriever.retrieve(candidate)


def _normalize(value: str) -> str:
    return " ".join(value.casefold().split())
