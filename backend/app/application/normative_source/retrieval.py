"""Retrieval of authoritative normative source content."""

from dataclasses import dataclass
from typing import Protocol
from urllib.request import Request, urlopen

from app.application.normative_source.catalog import (
    NormativeSourceCandidate,
    NormativeSourceResolver,
)


@dataclass(frozen=True)
class RetrievedSource:
    candidate: NormativeSourceCandidate
    content: str


class SourceRetriever(Protocol):
    def retrieve(self, candidate: NormativeSourceCandidate) -> RetrievedSource: ...


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
