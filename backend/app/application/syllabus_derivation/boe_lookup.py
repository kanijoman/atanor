"""Resolve a cited law that is not in the seed catalog through the BOE open-data service."""

import json
from collections.abc import Callable
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app.application.normative_source import NormativeSourceCandidate
from app.application.syllabus_derivation.references import LawReference
from app.application.syllabus_derivation.text import strip_accents
from app.domain.models import Source

API_URL = "https://www.boe.es/datosabiertos/api/legislacion-consolidada"
Fetch = Callable[[str], str]


def _fetch(url: str) -> str:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "Atanor/0.1"})
    with urlopen(request, timeout=30) as response:
        return str(response.read().decode("utf-8"))


class BoeLawLookup:
    """Finds the consolidated text of a law by its kind and number; never guesses."""

    def __init__(self, fetch: Fetch = _fetch) -> None:
        self._fetch = fetch

    def find(self, reference: LawReference) -> NormativeSourceCandidate | None:
        query = {"query": {"query_string": {"query": f'numero_oficial:"{reference.number}"'}}}
        url = f"{API_URL}?{urlencode({'query': json.dumps(query), 'limit': 50})}"
        matches = [
            entry
            for entry in json.loads(self._fetch(url)).get("data", [])
            if entry["numero_oficial"] == reference.number
            and strip_accents(entry["rango"]["texto"]) == reference.kind
        ]
        if len(matches) != 1:  # none, or ambiguous: leave it unresolved
            return None
        entry = matches[0]
        identifier = entry["identificador"]
        return NormativeSourceCandidate(
            source=Source(
                title=entry["titulo"],
                locator=f"https://www.boe.es/buscar/act.php?id={identifier}",
            ),
            authority="BOE",
            identifier=identifier,
            label=reference.designation,
        )
