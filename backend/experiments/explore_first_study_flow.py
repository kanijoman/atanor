from pathlib import Path

from app.application.knowledge_acquisition import BoeKnowledgeAcquisitionStrategy
from app.application.knowledge_construction import construct_knowledge
from app.application.knowledge_extraction import DeterministicKnowledgeExtractionStrategy
from app.application.pdf_extraction import extract_pdf_text
from app.application.document_processing import process_document
from app.domain.models import KnowledgeNeed, Requirement, RequirementScope, Source


SAMPLES_DIR = Path("tests/samples")
TARGET_SAMPLE = "BOE-A-2024-14098.pdf"

# Experimental fixture taken from the real BOE programme. It is deliberately
# kept outside the product model: this experiment evaluates the current flow
# and must not turn this document's structure into an application rule.
PROCESS_TITLE = "Cuerpo de Técnicos Auxiliares de Informática"
KNOWLEDGE_TOPIC = "La Constitución Española de 1978"
KNOWLEDGE_DEPTH = 1

CONTEXT_LINES = 2


def build_experimental_fixture(pdf_path: Path) -> tuple[Source, Requirement, KnowledgeNeed]:
    source = Source(title=pdf_path.name, locator=str(pdf_path))
    need = KnowledgeNeed(topic=KNOWLEDGE_TOPIC, depth=KNOWLEDGE_DEPTH)
    requirement = Requirement(
        title=PROCESS_TITLE,
        source_id=source.id,
        scopes=(
            RequirementScope(
                context="Programme III — study topic selected from the real BOE programme",
                knowledge_needs=(need,),
            ),
        ),
    )
    return source, requirement, need


def evaluate(pdf_path: Path) -> None:
    source, requirement, need = build_experimental_fixture(pdf_path)
    processing = process_document(source)

    knowledge = construct_knowledge(
        need=need,
        acquisition_strategy=BoeKnowledgeAcquisitionStrategy(source=source),
        extraction_strategy=DeterministicKnowledgeExtractionStrategy(
            context_lines=CONTEXT_LINES
        ),
    )

    source_text = extract_pdf_text(source)
    normalized_topic = " ".join(need.topic.casefold().split())
    match_count = sum(
        normalized_topic in " ".join(line.casefold().split())
        for line in source_text.splitlines()
        if line.strip()
    )

    print("FIRST END-TO-END STUDY FLOW")
    print(f"  sample: {pdf_path.name}")
    print(f"  process: {requirement.title}")
    print(f"  context: {requirement.scopes[0].context}")
    print(f"  knowledge need: {need.topic}")
    print(f"  depth: {need.depth}")
    print(f"  extracted characters: {len(processing.text):,}")
    print(f"  structure markers: {len(processing.structure):,}")
    print(f"  topic line matches: {match_count:,}")
    print(f"  source: {source.title}")
    print()

    if knowledge is None:
        print("RESULT: no knowledge constructed")
        return

    description = knowledge.description or ""
    print("GENERATED KNOWLEDGE")
    print("------------------")
    print(description)
    print()
    print("BASELINE EVALUATION")
    print("-------------------")
    print(f"  generated characters: {len(description):,}")
    print(f"  generated lines: {len([line for line in description.splitlines() if line.strip()]):,}")
    print(f"  provenance sources: {len(knowledge.sources):,}")
    print()
    print("Evaluate manually:")
    print("  relevance:       does the content address the knowledge need?")
    print("  completeness:    does it cover what the programme demands?")
    print("  noise:            how much content is incidental or irrelevant?")
    print("  traceability:     can the content be traced to the source?")
    print("  study usefulness: could an oppositor use this to study?")


def main() -> None:
    pdf_path = SAMPLES_DIR / TARGET_SAMPLE
    if not pdf_path.exists():
        raise FileNotFoundError(f"Sample not found: {pdf_path}")

    evaluate(pdf_path)


if __name__ == "__main__":
    main()
