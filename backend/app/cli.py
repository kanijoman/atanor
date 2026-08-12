import argparse
from pathlib import Path
from uuid import UUID

from app.application.source import get_source, import_pdf_source, list_sources
from app.persistence.database import SessionLocal
from app.persistence.source_repository import SqlAlchemySourceRepository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="atanor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    import_source = subparsers.add_parser(
        "import-source", help="Import a local PDF as a source"
    )
    import_source.add_argument("pdf", type=Path, help="Path to the PDF file")

    get_source_parser = subparsers.add_parser(
        "get-source", help="Get a source by ID"
    )
    get_source_parser.add_argument("source_id", type=UUID, help="Source UUID")

    subparsers.add_parser("list-sources", help="List all sources")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repository = SqlAlchemySourceRepository(SessionLocal)

    if args.command == "import-source":
        try:
            source = import_pdf_source(args.pdf, repository)
        except (FileNotFoundError, ValueError) as exc:
            parser.error(str(exc))

        print("Source imported successfully:")
        print(f"  ID: {source.id}")
        print(f"  Title: {source.title}")
        print(f"  Locator: {source.locator}")
        return 0

    if args.command == "get-source":
        source = get_source(args.source_id, repository)
        if source is None:
            print(f"Source not found: {args.source_id}")
            return 1

        print("Source:")
        print(f"  ID: {source.id}")
        print(f"  Title: {source.title}")
        print(f"  Locator: {source.locator}")
        return 0

    if args.command == "list-sources":
        sources = list_sources(repository)
        if not sources:
            print("No sources found.")
            return 0

        print("Sources:")
        for index, source in enumerate(sources, start=1):
            print(f"  {index}. {source.id}")
            print(f"     {source.title}")
            print(f"     {source.locator}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
