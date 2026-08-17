from app.application.knowledge_extraction import DeterministicKnowledgeExtractionStrategy
from app.domain.models import KnowledgeNeed


def test_extracts_relevant_context_around_topic() -> None:
    text = "\n".join(
        [
            "Preámbulo",
            "Artículo irrelevante",
            "Constitución Española",
            "La Constitución establece los principios fundamentales.",
            "Los ciudadanos tienen derechos y deberes.",
            "Contenido posterior",
        ]
    )

    result = DeterministicKnowledgeExtractionStrategy(context_lines=1).extract(
        KnowledgeNeed(topic="Constitución Española", depth=1),
        text,
    )

    assert result is not None
    assert result.title == "Constitución Española"
    assert "Constitución Española" in result.description
    assert "La Constitución establece los principios fundamentales." in result.description
    assert "Los ciudadanos tienen derechos y deberes." not in result.description


def test_returns_no_knowledge_when_topic_is_absent() -> None:
    result = DeterministicKnowledgeExtractionStrategy().extract(
        KnowledgeNeed(topic="Tema inexistente", depth=1),
        "Constitución Española\nDerechos fundamentales",
    )

    assert result is None
