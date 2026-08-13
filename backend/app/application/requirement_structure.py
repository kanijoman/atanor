from dataclasses import dataclass


@dataclass(frozen=True)
class StructuredRequirementContext:
    """A source-specific context in which numbered lines may be requirements."""

    name: str


def find_program_context(lines: list[str]) -> StructuredRequirementContext | None:
    """Find the simple program context used by the initial BOE strategy.

    This is intentionally source-specific and does not make 'Programa' a
    domain-level requirement concept.
    """
    for line in lines:
        if line.strip().casefold() == "programa":
            return StructuredRequirementContext(name="program")
    return None


def discover_numbered_mentions_in_context(
    text: str,
    source_id,
) -> list:
    """Discover numbered mentions only inside the known program context."""
    from app.application.requirement import RequirementMention
    import re

    lines = text.splitlines()
    context = find_program_context(lines)
    if context is None:
        return []

    marker = re.compile(r"^\s*\d+(?:\.\d+)*[.)]\s+(.+?)\s*$")
    mentions: list[RequirementMention] = []
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
            mentions.append(
                RequirementMention(
                    expression=expression,
                    source_id=source_id,
                    locator=f"line:{line_number}",
                )
            )

    return mentions
