"""Discover competitive-exam calls from source documents."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol

from app.application.document_processing import process_document
from app.application.study_programmes import discover_programmes
from app.domain.models import Call, Source, StudyProgramme


class CallRepository(Protocol):
    def save(self, call: Call) -> Call: ...

    def list_all(self) -> list[Call]: ...


class StudyProgrammeRepository(Protocol):
    def save(self, programme: StudyProgramme) -> StudyProgramme: ...


@dataclass(frozen=True)
class CallContextSignals:
    """Deterministic textual signals used to identify a call document."""

    signals_present: int
    strong_signals_present: int
    nearby_call_signal_pairs: int

    @property
    def is_strong(self) -> bool:
        return self.strong_signals_present >= 3 and self.nearby_call_signal_pairs >= 2


_SIGNALS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("convocatoria", (r"\bconvocatoria\b",)),
    ("plazas", (r"\bplazas?\b",)),
    ("cuerpo_escala", (r"\bcuerpos?\b", r"\bescala[s]?\b")),
    ("sistema_selectivo", (r"\bsistema\s+selectivo\b",)),
    ("turno", (r"\bturno[s]?\b",)),
    ("organo_convocante", (r"\b[oó]rgano\s+convocante\b",)),
    ("resolucion_orden", (r"\bresoluci[oó]n(?:es)?\b", r"\borden(?:es)?\b")),
    ("fecha", (r"\bfecha\b", r"\bde\s+\d{1,2}\s+de\s+\w+\s+de\s+\d{4}\b")),
)

_STRONG_SIGNAL_NAMES = {
    "convocatoria",
    "plazas",
    "cuerpo_escala",
    "sistema_selectivo",
    "organo_convocante",
}

_CALL_CONTEXT_PAIRS = (
    ("convocatoria", "plazas"),
    ("convocatoria", "cuerpo_escala"),
    ("plazas", "sistema_selectivo"),
    ("cuerpo_escala", "sistema_selectivo"),
)


def _positions(text: str, patterns: tuple[str, ...]) -> list[int]:
    return sorted(
        match.start()
        for pattern in patterns
        for match in re.finditer(pattern, text, flags=re.IGNORECASE)
    )


def _has_nearby_signals(
    text: str,
    signal_a: tuple[str, ...],
    signal_b: tuple[str, ...],
    window: int = 3000,
) -> bool:
    positions_a = _positions(text, signal_a)
    positions_b = _positions(text, signal_b)
    return any(abs(a - b) <= window for a in positions_a for b in positions_b)


def analyse_call_context(text: str) -> CallContextSignals:
    """Analyse deterministic call-context signals without creating domain entities."""
    signal_map = dict(_SIGNALS)
    present = {
        name: any(
            re.search(pattern, text, flags=re.IGNORECASE)
            for pattern in patterns
        )
        for name, patterns in _SIGNALS
    }
    strong_signals_present = sum(present[name] for name in _STRONG_SIGNAL_NAMES)
    nearby_call_signal_pairs = sum(
        _has_nearby_signals(text, signal_map[left], signal_map[right])
        for left, right in _CALL_CONTEXT_PAIRS
    )
    return CallContextSignals(
        signals_present=sum(present.values()),
        strong_signals_present=strong_signals_present,
        nearby_call_signal_pairs=nearby_call_signal_pairs,
    )


def discover_calls(source: Source) -> list[Call]:
    """Discover calls when a source contains strong deterministic call context."""
    processing = process_document(source)
    if len(processing.text.strip()) < 100:
        return []

    signals = analyse_call_context(processing.text)
    if not signals.is_strong:
        return []

    call = Call(title=source.title, source_id=source.id)
    if not discover_programmes(call, source):
        return []

    return [call]


def discover_and_persist_call(
    source: Source,
    call_repository: CallRepository,
    programme_repository: StudyProgrammeRepository,
) -> Call | None:
    """Discover, persist, and populate a call from a source document."""
    existing_call = next(
        (call for call in call_repository.list_all() if call.source_id == source.id),
        None,
    )
    if existing_call is not None:
        return existing_call

    calls = discover_calls(source)
    if not calls:
        return None

    call = call_repository.save(calls[0])
    for programme in discover_programmes(call, source):
        programme_repository.save(programme)
    return call
