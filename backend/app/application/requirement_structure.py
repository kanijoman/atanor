from dataclasses import dataclass
import re


@dataclass(frozen=True)
class StructuredRequirementContext:
    """A source-specific context in which requirement items may be found."""

    name: str


@dataclass(frozen=True)
class StructuredRequirementCandidate:
    """A candidate found inside a structured context."""

    expression: str
    line_number: int


_PROGRAM_CONTEXT_MARKER = re.compile(
    r"^\s*(?:\d+(?:\.\d+)*[.)]\s*)?programa(?:\s+que\b.*)?\.?\s*$",
    re.IGNORECASE,
)

_NUMBERED_MARKER = re.compile(r"^\s*\d+(?:\.\d+)*[.)]\s+(.+?)\s*$")
_TEMA_MARKER = re.compile(
    r"^\s*Tema\s+(?P<identifier>[A-Za-z0-9]+)\s*[.\u2013-]\s*(?P<expression>.+?)\s*$",
    re.IGNORECASE,
)


def find_program_context(lines: list[str]) -> StructuredRequirementContext | None:
    """Find the supported program context in a source document."""
    for line in lines:
        if _PROGRAM_CONTEXT_MARKER.match(line):
            return StructuredRequirementContext(name="programa")
    return None


def discover_numbered_candidates_in_context(
    text: str,
) -> list[StructuredRequirementCandidate]:
    """Discover supported requirement candidates inside the program context."""
    lines = text.splitlines()
    if find_program_context(lines) is None:
        return []

    candidates: list[StructuredRequirementCandidate] = []
    in_context = False

    for line_number, line in enumerate(lines, start=1):
        if _PROGRAM_CONTEXT_MARKER.match(line):
            in_context = True
            continue
        if not in_context:
            continue

        numbered_match = _NUMBERED_MARKER.match(line)
        tema_match = _TEMA_MARKER.match(line)

        if numbered_match:
            expression = " ".join(numbered_match.group(1).split())
        elif tema_match:
            expression = " ".join(line.strip().split())
        else:
            continue

        if expression:
            candidates.append(
                StructuredRequirementCandidate(
                    expression=expression,
                    line_number=line_number,
                )
            )

    return candidates
