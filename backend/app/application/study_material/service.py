"""Application services that prepare study material for programme units."""

from typing import Protocol

from app.application.normative_source import SourceRetriever
from app.application.study_material.providers import MaterialProvenance
from app.application.study_material.registry import find_topic_by_name, find_topic_for_title
from app.application.study_material.topic import StudyTopic
from app.domain.models import Knowledge, KnowledgeNeed, StudyProgrammeUnit


class KnowledgeRepository(Protocol):
    def save(self, knowledge: Knowledge) -> Knowledge: ...

    def get_by_identity(self, identity_key: tuple[str, int]) -> Knowledge | None: ...


def _topic_for_unit(programme_unit: StudyProgrammeUnit) -> StudyTopic:
    topic = find_topic_for_title(programme_unit.title)
    if topic is None:
        raise ValueError(
            "No supported knowledge need can be derived from programme item "
            f"'{programme_unit.title}'"
        )
    return topic


def derive_knowledge_needs_for_programme_unit(
    programme_unit: StudyProgrammeUnit,
) -> tuple[KnowledgeNeed, ...]:
    return (KnowledgeNeed(topic=_topic_for_unit(programme_unit).name, depth=1),)


def derive_required_aspects_for_programme_unit(
    programme_unit: StudyProgrammeUnit,
) -> tuple[str, ...]:
    return _topic_for_unit(programme_unit).required_aspects


def derive_covered_aspects(
    programme_unit: StudyProgrammeUnit, knowledge: Knowledge
) -> tuple[str, ...]:
    topic = _topic_for_unit(programme_unit)
    return topic.covered_aspects(knowledge, topic.required_aspects)


def derive_material_provenance(programme_unit: StudyProgrammeUnit) -> MaterialProvenance:
    """Return how the study material for a programme unit was produced and reviewed."""
    return _topic_for_unit(programme_unit).provider.provenance


def generate_material_for_need(
    need: KnowledgeNeed,
    repository: KnowledgeRepository,
    retriever: SourceRetriever | None = None,
) -> Knowledge:
    """Return the material for a supported need, reusing persisted knowledge.

    Acquiring providers fetch their source through `retriever` (the live default
    when omitted); the result is persisted so later requests need no network.
    """
    topic = find_topic_by_name(need.topic)
    if topic is None:
        raise ValueError(f"Unsupported study topic: {need.topic}")
    existing = repository.get_by_identity(need.identity_key)
    if existing is not None:
        return existing
    return repository.save(
        Knowledge(
            title=need.topic,
            description=topic.provider.description(retriever),
            sources=topic.provider.sources,
            identity_key=need.identity_key,
        )
    )


def generate_study_material_for_programme_unit(
    programme_unit: StudyProgrammeUnit,
    need: KnowledgeNeed,
    repository: KnowledgeRepository,
    retriever: SourceRetriever | None = None,
) -> Knowledge:
    topic = find_topic_for_title(programme_unit.title)
    if topic is None or topic.name != need.topic:
        raise ValueError(
            f"Knowledge need '{need.topic}' does not match programme item '{programme_unit.title}'"
        )
    return generate_material_for_need(need, repository, retriever)


def is_study_material_available_for_programme_unit(programme_unit: StudyProgrammeUnit) -> bool:
    return find_topic_for_title(programme_unit.title) is not None


def prepare_programme_unit_for_study(
    programme_unit: StudyProgrammeUnit,
    repository: KnowledgeRepository,
    retriever: SourceRetriever | None = None,
) -> Knowledge:
    need = derive_knowledge_needs_for_programme_unit(programme_unit)[0]
    return generate_study_material_for_programme_unit(programme_unit, need, repository, retriever)
