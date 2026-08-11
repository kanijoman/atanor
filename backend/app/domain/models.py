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
class Blueprint:
    requirements: tuple[Knowledge, ...] = field(default_factory=tuple)

    def requires(self, knowledge: Knowledge) -> "Blueprint":
        return Blueprint(requirements=(*self.requirements, knowledge))


@dataclass(frozen=True)
class Requirement:
    title: str
    description: str | None = None
    sources: tuple[Source, ...] = field(default_factory=tuple)
    blueprint: Blueprint | None = None

    def with_source(self, source: Source) -> "Requirement":
        return Requirement(
            title=self.title,
            description=self.description,
            sources=(*self.sources, source),
            blueprint=self.blueprint,
        )

    def with_blueprint(self, blueprint: Blueprint) -> "Requirement":
        return Requirement(
            title=self.title,
            description=self.description,
            sources=self.sources,
            blueprint=blueprint,
        )
