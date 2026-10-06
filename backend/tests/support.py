from __future__ import annotations

from uuid import UUID

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
