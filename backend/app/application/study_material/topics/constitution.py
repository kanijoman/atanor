"""Study topic: La Constitución Española de 1978 (principles and fundamental rights), from the BOE.

Designed for the programme unit "La Constitución Española de 1978. Características. Los
principios constitucionales y los valores superiores. Derechos y deberes fundamentales. Su
garantía y suspensión."
"""

from app.application.normative_source import CONSTITUCION_ESPANOLA
from app.application.study_material.coverage import aspects_covered_by_sections
from app.application.study_material.providers import AcquiredNormativeMaterial, ArticleSection
from app.application.study_material.topic import StudyTopic
from app.application.study_material.wording import states_subject_with_scope

TOPIC_NAME = "La Constitución Española de 1978"

# Aspect -> articles of the Constitution that develop it. Explicit contract, pending expert review.
SECTIONS = (
    ArticleSection("Características de la Constitución", tuple(range(1, 9))),
    ArticleSection("Los principios constitucionales y los valores superiores", (1, 9, 10)),
    ArticleSection("Derechos y deberes fundamentales", tuple(range(14, 32))),
    ArticleSection("Garantía y suspensión de los derechos y libertades", (53, 54, 55)),
)

REQUIRED_ASPECTS = tuple(section.aspect for section in SECTIONS)

_SUBJECT = "la constitución española de 1978"
_SCOPE = (
    "características",
    "principios constitucionales",
    "valores superiores",
    "derechos y deberes fundamentales",
    "garantía y suspensión",
)


def _matches(title: str) -> bool:
    return states_subject_with_scope(title, _SUBJECT, _SCOPE)


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    provider=AcquiredNormativeMaterial(CONSTITUCION_ESPANOLA, SECTIONS),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=aspects_covered_by_sections,
)
