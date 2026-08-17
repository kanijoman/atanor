from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Source:
    title: str
    locator: str | None = None
    id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True)
class Knowledge:
    title: str
    description: str | None = None
    sources: tuple[Source, ...] = field(default_factory=tuple)
    id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True)
class KnowledgeNeed:
    topic: str
    depth: int
    knowledge: Knowledge | None = None
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if self.depth <= 0:
            raise ValueError("Knowledge need depth must be positive")

    @property
    def knowledge_id(self) -> UUID | None:
        return None if self.knowledge is None else self.knowledge.id


@dataclass(frozen=True)
class RequirementScope:
    context: str
    knowledge_needs: tuple[KnowledgeNeed, ...] = field(default_factory=tuple)
    id: UUID = field(default_factory=uuid4)

    def requires(self, knowledge_need: KnowledgeNeed) -> "RequirementScope":
        return RequirementScope(
            context=self.context,
            knowledge_needs=(*self.knowledge_needs, knowledge_need),
            id=self.id,
        )


@dataclass(frozen=True)
class Requirement:
    title: str
    source_id: UUID
    description: str | None = None
    scopes: tuple[RequirementScope, ...] = field(default_factory=tuple)
    id: int | None = None

    def with_scope(self, scope: RequirementScope) -> "Requirement":
        return Requirement(
            title=self.title,
            source_id=self.source_id,
            description=self.description,
            scopes=(*self.scopes, scope),
            id=self.id,
        )
