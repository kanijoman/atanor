from dataclasses import dataclass, field


@dataclass(frozen=True)
class Source:
    title: str
    locator: str | None = None


@dataclass(frozen=True)
class Knowledge:
    title: str
    description: str | None = None
    sources: tuple[Source, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class KnowledgeRequirement:
    knowledge: Knowledge


@dataclass(frozen=True)
class Blueprint:
    knowledge_requirements: tuple[KnowledgeRequirement, ...] = field(
        default_factory=tuple
    )

    def requires(self, knowledge: Knowledge) -> "Blueprint":
        return Blueprint(
            knowledge_requirements=(
                *self.knowledge_requirements,
                KnowledgeRequirement(knowledge=knowledge),
            )
        )


@dataclass(frozen=True)
class Requirement:
    title: str
    description: str | None = None
    blueprint: Blueprint | None = None

    def with_blueprint(self, blueprint: Blueprint) -> "Requirement":
        return Requirement(
            title=self.title,
            description=self.description,
            blueprint=blueprint,
        )
