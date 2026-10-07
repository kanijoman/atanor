from __future__ import annotations

from pathlib import Path
from uuid import UUID

from app.application.normative_source import NormativeSourceCandidate, RetrievedSource
from app.domain.models import Knowledge


class InMemoryKnowledgeRepository:
    """Shared in-memory KnowledgeRepository fake for application-level tests."""

    def __init__(self) -> None:
        self.items: dict[UUID, Knowledge] = {}

    def save(self, knowledge: Knowledge) -> Knowledge:
        self.items[knowledge.id] = knowledge
        return knowledge

    def get_by_id(self, knowledge_id: UUID) -> Knowledge | None:
        return self.items.get(knowledge_id)

    def get_by_identity(self, identity_key: tuple[str, int]) -> Knowledge | None:
        return next(
            (
                knowledge
                for knowledge in self.items.values()
                if knowledge.identity_key == identity_key
            ),
            None,
        )


FIXTURES_DIR = Path(__file__).parent / "fixtures"


class FixtureSourceRetriever:
    """Serve saved BOE HTML instead of calling the live service (offline, deterministic)."""

    def retrieve(self, candidate: NormativeSourceCandidate) -> RetrievedSource:
        html = (FIXTURES_DIR / "boe" / f"{candidate.identifier}.html").read_text(encoding="utf-8")
        return RetrievedSource(candidate=candidate, content=html)
