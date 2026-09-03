from app.application.knowledge_acquisition import (
    KnowledgeAcquisitionStrategy,
    acquire_knowledge,
)
from app.application.knowledge_extraction import KnowledgeExtractionStrategy
from app.domain.models import Knowledge, KnowledgeNeed


def construct_knowledge(
    need: KnowledgeNeed,
    acquisition_strategy: KnowledgeAcquisitionStrategy,
    extraction_strategy: KnowledgeExtractionStrategy,
) -> Knowledge | None:
    """Construct relevant knowledge for a need from acquired source material."""
    acquired = acquire_knowledge(need, acquisition_strategy)

    if acquired is None or not acquired.description:
        return None

    extracted = extraction_strategy.extract(need, acquired.description)

    if extracted is None:
        return None

    return Knowledge(
        title=extracted.title,
        description=extracted.description,
        sources=acquired.sources,
        id=extracted.id,
    )
