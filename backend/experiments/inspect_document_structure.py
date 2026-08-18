from pathlib import Path

from app.application.pdf_extraction import extract_pdf_text
from app.application.source import import_pdf_source
from app.domain.models import KnowledgeNeed


SAMPLES = [
    (
        "BOE",
        Path("tests/samples/BOE-A-2024-14098.pdf"),
        "Constitución Española",
    ),
    (
        "BOJA",
        Path("tests/samples/BOJA24-138-00046-48048-01_00304998.pdf"),
        "Constitución Española",
    ),
    (
        "Programa Archiveros",
        Path("tests/samples/Programa_Archiveros_0.pdf"),
        "archivos",
    ),
    (
        "Ayuntamiento de León",
        Path("tests/samples/OPOS_AYTO_LEON_INFORMATICA_B.pdf"),
        "informática",
    ),
]

NEGATIVE_NEED = "Constitución de Marte"
CONTEXT_LINES = 2


class _InMemorySourceRepository:
    def save(self, source):
        return source


def inspect_document(name: str, path: Path, topic: str) -> None:
    source = import_pdf_source(path, _InMemorySourceRepository())
    text = extract_pdf_text(source)
    lines = text.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]

    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)
    print(f"File: {path}")
    print(f"Pages: {source.metadata.get('pages') if source.metadata else 'unknown'}")
    print(f"Characters: {len(text)}")
    print(f"Lines: {len(lines)}")
    print(f"Non-empty lines: {len(non_empty_lines)}")

    for label, need_topic in (
        ("PRESENT", topic),
        ("NEGATIVE", NEGATIVE_NEED),
    ):
        need = KnowledgeNeed(topic=need_topic, depth=1)
        normalized_topic = need.topic.casefold()
        matches = [
            index
            for index, line in enumerate(lines)
            if normalized_topic in line.casefold()
        ]

        print(f"\n--- {label}: {need_topic!r} ---")
        print(f"Occurrences: {len(matches)}")

        for occurrence, index in enumerate(matches, start=1):
            start = max(0, index - CONTEXT_LINES)
            end = min(len(lines), index + CONTEXT_LINES + 1)
            print(f"\nOccurrence {occurrence} (line {index + 1})")
            for context_index in range(start, end):
                marker = ">" if context_index == index else " "
                print(f"{marker} {context_index + 1:6}: {lines[context_index]}")


def main() -> None:
    for name, path, topic in SAMPLES:
        inspect_document(name, path, topic)


if __name__ == "__main__":
    main()
