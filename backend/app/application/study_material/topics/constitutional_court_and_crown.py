"""Study topic: Tribunal Constitucional, reforma de la Constitución and Corona, from the BOE.

Designed for the programme unit "El Tribunal Constitucional. La reforma de la Constitución. La
Corona: funciones constitucionales del Rey. Sucesión y regencia."
"""

from app.application.normative_source import CONSTITUCION_ESPANOLA
from app.application.study_material.coverage import aspects_covered_by_sections
from app.application.study_material.providers import AcquiredNormativeMaterial, ArticleSection
from app.application.study_material.topic import StudyTopic
from app.application.study_material.wording import states_subject_with_scope

TOPIC_NAME = "El Tribunal Constitucional, la reforma de la Constitución y la Corona"

# Aspect -> articles of the Constitution that develop it. Explicit contract, pending expert review.
SECTIONS = (
    ArticleSection("El Tribunal Constitucional", tuple(range(159, 166))),
    ArticleSection("La reforma de la Constitución", tuple(range(166, 170))),
    ArticleSection("La Corona: funciones constitucionales del Rey", (56, 62, 63, 64, 65)),
    ArticleSection("Sucesión y regencia", (57, 58, 59, 60, 61)),
)

REQUIRED_ASPECTS = tuple(section.aspect for section in SECTIONS)

_SUBJECT = "el tribunal constitucional"
_SCOPE = ("la reforma de la constitución", "la corona", "sucesión y regencia")


def _matches(title: str) -> bool:
    return states_subject_with_scope(title, _SUBJECT, _SCOPE)


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    provider=AcquiredNormativeMaterial(CONSTITUCION_ESPANOLA, SECTIONS),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=aspects_covered_by_sections,
)
