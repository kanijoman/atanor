from dataclasses import dataclass

from app.application.knowledge_acquisition import KnowledgeAcquisitionStrategy
from app.application.knowledge_construction import construct_knowledge
from app.application.knowledge_extraction import KnowledgeExtractionStrategy
from app.domain.models import Knowledge, KnowledgeNeed, Source


@dataclass(frozen=True)
class FakeAcquisitionStrategy(KnowledgeAcquisitionStrategy):
    knowledge: Knowledge

    def acquire(self, need: KnowledgeNeed) -> Knowledge | None:
        return self.knowledge


@dataclass(frozen=True)
class FakeExtractionStrategy(KnowledgeExtractionStrategy):
    knowledge: Knowledge

    def extract(self, need: KnowledgeNeed, text: str) -> Knowledge | None:
        return self.knowledge


def test_construct_knowledge_combines_acquisition_and_extraction() -> None:
    source = Source(
        title="Constitución Española",
        locator="https://www.boe.es/",
    )
    need = KnowledgeNeed(
        topic="Constitución Española",
        depth=1,
    )

    acquired = Knowledge(
        title=need.topic,
        description="Full authoritative source material.",
        sources=(source,),
    )
    extracted = Knowledge(
        title=need.topic,
        description="Relevant knowledge extracted from source material.",
    )

    knowledge = construct_knowledge(
        need,
        FakeAcquisitionStrategy(acquired),
        FakeExtractionStrategy(extracted),
    )

    assert knowledge is not None
    assert knowledge.title == need.topic
    assert knowledge.description == extracted.description
    assert knowledge.sources == (source,)
