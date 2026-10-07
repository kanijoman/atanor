import argparse
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from app.application.call_import import import_call_from_pdf
from app.application.requirements import get_requirement, list_requirements
from app.application.source import get_source, import_pdf_source, list_sources
from app.application.study_support_report import build_support_report, format_support_report
from app.persistence.call_repository import SqlAlchemyCallRepository
from app.persistence.database import SessionLocal
from app.persistence.requirement_repository import SqlAlchemyRequirementRepository
from app.persistence.source_repository import SqlAlchemySourceRepository
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository


@dataclass(frozen=True)
class Repositories:
    """Persistence adapters used by the CLI commands."""

    sources: SqlAlchemySourceRepository
    requirements: SqlAlchemyRequirementRepository
    calls: SqlAlchemyCallRepository
    programmes: SqlAlchemyStudyProgrammeRepository


REPORT_SEPARATOR = "\n\n"
CommandHandler = Callable[[argparse.Namespace, argparse.ArgumentParser, Repositories], int]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="atanor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    import_source = subparsers.add_parser("import-source", help="Import a local PDF as a source")
    import_source.add_argument("pdf", type=Path, help="Path to the PDF file")

    import_call = subparsers.add_parser(
        "import-call", help="Import a competitive-exam call from a PDF"
    )
    import_call.add_argument("pdf", type=Path, help="Path to the call PDF")

    get_source_parser = subparsers.add_parser("get-source", help="Get a source by ID")
    get_source_parser.add_argument("source_id", type=UUID, help="Source UUID")

    subparsers.add_parser("list-sources", help="List all sources")

    get_requirement_parser = subparsers.add_parser(
        "get-requirement", help="Get a requirement by ID"
    )
    get_requirement_parser.add_argument("requirement_id", type=int, help="Requirement ID")

    subparsers.add_parser("list-requirements", help="List all requirements")

    report_parser = subparsers.add_parser(
        "study-support-report",
        help="Report which programme units of call PDFs have study material (no persistence)",
    )
    report_parser.add_argument("pdfs", type=Path, nargs="+", help="Paths to call PDFs")
    return parser


def _import_source(
    args: argparse.Namespace, parser: argparse.ArgumentParser, repositories: Repositories
) -> int:
    try:
        source = import_pdf_source(args.pdf, repositories.sources)
    except (FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))

    print("Source imported successfully:")
    print(f"  ID: {source.id}")
    print(f"  Title: {source.title}")
    print(f"  Locator: {source.locator}")
    return 0


def _import_call(
    args: argparse.Namespace, parser: argparse.ArgumentParser, repositories: Repositories
) -> int:
    try:
        call = import_call_from_pdf(
            args.pdf, repositories.sources, repositories.calls, repositories.programmes
        )
    except (FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))

    print("Call imported successfully:")
    print(f"  ID: {call.id}")
    print(f"  Title: {call.title}")
    return 0


def _get_source(
    args: argparse.Namespace, _parser: argparse.ArgumentParser, repositories: Repositories
) -> int:
    source = get_source(args.source_id, repositories.sources)
    if source is None:
        print(f"Source not found: {args.source_id}")
        return 1

    print("Source:")
    print(f"  ID: {source.id}")
    print(f"  Title: {source.title}")
    print(f"  Locator: {source.locator}")
    return 0


def _list_sources(
    _args: argparse.Namespace, _parser: argparse.ArgumentParser, repositories: Repositories
) -> int:
    sources = list_sources(repositories.sources)
    if not sources:
        print("No sources found.")
        return 0

    print("Sources:")
    for index, source in enumerate(sources, start=1):
        print(f"  {index}. {source.id}")
        print(f"     {source.title}")
        print(f"     {source.locator}")
    return 0


def _get_requirement(
    args: argparse.Namespace, _parser: argparse.ArgumentParser, repositories: Repositories
) -> int:
    requirement = get_requirement(args.requirement_id, repositories.requirements)
    if requirement is None:
        print(f"Requirement not found: {args.requirement_id}")
        return 1

    print("Requirement:")
    print(f"  ID: {requirement.id}")
    print(f"  Title: {requirement.title}")
    print(f"  Source ID: {requirement.source_id}")
    return 0


def _list_requirements(
    _args: argparse.Namespace, _parser: argparse.ArgumentParser, repositories: Repositories
) -> int:
    requirements = list_requirements(repositories.requirements)
    if not requirements:
        print("No requirements found.")
        return 0

    print("Requirements:")
    for index, requirement in enumerate(requirements, start=1):
        print(f"  {index}. {requirement.id}")
        print(f"     {requirement.title}")
        print(f"     Source: {requirement.source_id}")
    return 0


def _study_support_report(
    args: argparse.Namespace, parser: argparse.ArgumentParser, _repositories: Repositories
) -> int:
    try:
        reports = [build_support_report(pdf) for pdf in args.pdfs]
    except FileNotFoundError as exc:
        parser.error(str(exc))

    print(REPORT_SEPARATOR.join(format_support_report(report) for report in reports))
    return 0


_COMMANDS: dict[str, CommandHandler] = {
    "import-source": _import_source,
    "import-call": _import_call,
    "get-source": _get_source,
    "list-sources": _list_sources,
    "get-requirement": _get_requirement,
    "list-requirements": _list_requirements,
    "study-support-report": _study_support_report,
}


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = _COMMANDS.get(args.command)
    if handler is None:
        return 1

    repositories = Repositories(
        sources=SqlAlchemySourceRepository(SessionLocal),
        requirements=SqlAlchemyRequirementRepository(SessionLocal),
        calls=SqlAlchemyCallRepository(SessionLocal),
        programmes=SqlAlchemyStudyProgrammeRepository(SessionLocal),
    )
    return handler(args, parser, repositories)


if __name__ == "__main__":
    raise SystemExit(main())
