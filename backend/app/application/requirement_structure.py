from dataclasses import dataclass
import re


@dataclass(frozen=True)
class StructuredRequirementContext:
    """A source-specific context in which numbered lines may be requirements."""

    name: str


@dataclass(frozen=True)
class StructuredRequirementCandidate:
    """A numbered candidate found inside a structured context."""

    expression: str
    line_number: int


def find_program_context(lines: list[str]) -> StructuredRequirementContext | None:
    """Find the simple program context used by the initial BOE strategy."""
    for line in lines:
        if line.strip().casefold() == "programa":
            return StructuredRequirementContext(name="programa")
    return None


def discover_numbered_candidates_in_context(
    text: str,
) -> list[StructuredRequirementCandidate]:
    """Discover numbered candidates only inside the known program context."""
    lines = text.splitlines()
    context = find_program_context(lines)
    if context is None:
        return []

    marker = re.compile(r"^\s*\d+(?:\.\d+)*[.)]\s+(.+?)\s*$")
    candidates: list[StructuredRequirementCandidate] = []
    in_context = False

    for line_number, line in enumerate(lines, start=1):
        if line.strip().casefold() == context.name:
            in_context = True
            continue
        if not in_context:
            continue

        match = marker.match(line)
        if not match:
            continue

        expression = " ".join(match.group(1).split())
        if expression:
            candidates.append(
                StructuredRequirementCandidate(
                    expression=expression,
                    line_number=line_number,
                )
            )

    return candidates
