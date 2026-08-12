import argparse
from pathlib import Path
from uuid import UUID

from app.application.requirement import get_requirement, list_requirements
from app.application.source import get_source, import_pdf_source, list_sources
from app.persistence.database import SessionLocal
from app.persistence.requirement_repository import SqlAlchemyRequirementRepository
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

    get_requirement_parser = subparsers.add_parser(
        "get-requirement", help="Get a requirement by ID"
    )
    get_requirement_parser.add_argument(
        "requirement_id", type=int, help="Requirement ID"
    )

    subparsers.add_parser("list-requirements", help="List all requirements")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    source_repository = SqlAlchemySourceRepository(SessionLocal)
    requirement_repository = SqlAlchemyRequirementRepository(SessionLocal)

    if args.command == "import-source":
        try:
            source = import_pdf_source(args.pdf, source_repository)
        except (FileNotFoundError, ValueError) as exc:
            parser.error(str(exc))

        print("Source imported successfully:")
        print(f"  ID: {source.id}")
        print(f"  Title: {source.title}")
        print(f"  Locator: {source.locator}")
        return 0

    if args.command == "get-source":
        source = get_source(args.source_id, source_repository)
        if source is None:
            print(f"Source not found: {args.source_id}")
            return 1

        print("Source:")
        print(f"  ID: {source.id}")
        print(f"  Title: {source.title}")
        print(f"  Locator: {source.locator}")
        return 0

    if args.command == "list-sources":
        sources = list_sources(source_repository)
        if not sources:
            print("No sources found.")
            return 0

        print("Sources:")
        for index, source in enumerate(sources, start=1):
            print(f"  {index}. {source.id}")
            print(f"     {source.title}")
            print(f"     {source.locator}")
        return 0

    if args.command == "get-requirement":
        requirement = get_requirement(args.requirement_id, requirement_repository)
        if requirement is None:
            print(f"Requirement not found: {args.requirement_id}")
            return 1

        print("Requirement:")
        print(f"  ID: {requirement.id}")
        print(f"  Title: {requirement.title}")
        print(f"  Source ID: {requirement.source_id}")
        return 0

    if args.command == "list-requirements":
        requirements = list_requirements(requirement_repository)
        if not requirements:
            print("No requirements found.")
            return 0

        print("Requirements:")
        for index, requirement in enumerate(requirements, start=1):
            print(f"  {index}. {requirement.id}")
            print(f"     {requirement.title}")
            print(f"     Source: {requirement.source_id}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
