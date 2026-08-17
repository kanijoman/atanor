from pathlib import Path

from app.application.knowledge_acquisition import BoeKnowledgeAcquisitionStrategy
from app.application.knowledge_extraction import DeterministicKnowledgeExtractionStrategy
from app.application.pdf_extraction import extract_pdf_text
from app.application.source import import_pdf_source
from app.domain.models import KnowledgeNeed


SAMPLE_PATH = Path("tests/samples/BOE-A-2024-14098.pdf")


def main() -> None:
    source = import_pdf_source(SAMPLE_PATH, _InMemorySourceRepository())
    need = KnowledgeNeed(topic="Constitución Española", depth=1)

    acquired = BoeKnowledgeAcquisitionStrategy(source).acquire(need)
    if acquired is None:
        print("No content was acquired from the BOE source.")
        return

    raw_text = acquired.description or ""
    extracted = DeterministicKnowledgeExtractionStrategy().extract(need, raw_text)

    print(f"Source characters: {len(raw_text)}")
    if extracted is None:
        print("No relevant knowledge was extracted.")
        return

    print(f"Extracted characters: {len(extracted.description or '')}")
    print("\n=== EXTRACTED KNOWLEDGE ===")
    print(extracted.description)
    print("=== END EXTRACTED KNOWLEDGE ===")


class _InMemorySourceRepository:
    def save(self, source):
        return source


if __name__ == "__main__":
    main()
