from dataclasses import dataclass
import re

from app.domain.models import Knowledge, KnowledgeNeed


class KnowledgeExtractionStrategy:
    def extract(self, need: KnowledgeNeed, text: str) -> Knowledge | None:
        raise NotImplementedError


@dataclass(frozen=True)
class DeterministicKnowledgeExtractionStrategy(KnowledgeExtractionStrategy):
    """Extract a small relevant text window using deterministic topic matching."""

    context_lines: int = 2

    def extract(self, need: KnowledgeNeed, text: str) -> Knowledge | None:
        normalized_topic = _normalize(need.topic)
        if not normalized_topic:
            return None

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        matches = [
            index
            for index, line in enumerate(lines)
            if normalized_topic in _normalize(line)
        ]
        if not matches:
            return None

        selected: list[str] = []
        seen: set[int] = set()
        for index in matches:
            start = max(0, index - self.context_lines)
            end = min(len(lines), index + self.context_lines + 1)
            for candidate_index in range(start, end):
                if candidate_index not in seen:
                    selected.append(lines[candidate_index])
                    seen.add(candidate_index)

        return Knowledge(title=need.topic, description="\n".join(selected))


def _normalize(value: str) -> str:
    value = value.casefold()
    value = re.sub(r"\s+", " ", value)
    return value.strip()
