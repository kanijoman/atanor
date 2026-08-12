import argparse
from pathlib import Path

from app.application.source import import_pdf_source
from app.persistence.database import SessionLocal
from app.persistence.source_repository import SqlAlchemySourceRepository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="atanor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    import_source = subparsers.add_parser(
        "import-source", help="Import a local PDF as a source"
    )
    import_source.add_argument("pdf", type=Path, help="Path to the PDF file")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "import-source":
        repository = SqlAlchemySourceRepository(SessionLocal)
        try:
            source = import_pdf_source(args.pdf, repository)
        except (FileNotFoundError, ValueError) as exc:
            parser.error(str(exc))

        print("Source imported successfully:")
        print(f"  Title: {source.title}")
        print(f"  Locator: {source.locator}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
