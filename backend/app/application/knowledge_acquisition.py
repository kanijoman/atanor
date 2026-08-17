from dataclasses import dataclass

from app.application.pdf_extraction import extract_pdf_text
from app.domain.models import Knowledge, KnowledgeNeed, Source


class KnowledgeAcquisitionStrategy:
    def acquire(self, need: KnowledgeNeed) -> Knowledge | None:
        raise NotImplementedError


@dataclass(frozen=True)
class BoeKnowledgeAcquisitionStrategy(KnowledgeAcquisitionStrategy):
    source: Source

    def acquire(self, need: KnowledgeNeed) -> Knowledge | None:
        text = extract_pdf_text(self.source).strip()
        if not text:
            return None

        return Knowledge(
            title=need.topic,
            description=text,
            sources=(self.source,),
        )


def acquire_knowledge(
    need: KnowledgeNeed,
    strategy: KnowledgeAcquisitionStrategy,
) -> Knowledge | None:
    """Acquire knowledge for a need without requiring candidate input."""
    return strategy.acquire(need)
