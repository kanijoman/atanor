"""Study topic: Las Cortes Generales y el Defensor del Pueblo, from the BOE.

Designed for the programme unit "Las Cortes Generales: composición, atribuciones y funcionamiento
del Congreso de los Diputados y Senado. El Defensor del Pueblo."
"""

from app.application.normative_source import CONSTITUCION_ESPANOLA
from app.application.study_material.coverage import aspects_covered_by_sections
from app.application.study_material.providers import AcquiredNormativeMaterial, ArticleSection
from app.application.study_material.topic import StudyTopic
from app.application.study_material.wording import states_subject_with_scope

TOPIC_NAME = "Las Cortes Generales y el Defensor del Pueblo"

# Aspect -> articles of the Constitution that develop it. Explicit contract, pending expert review.
SECTIONS = (
    ArticleSection("Composición de las Cortes Generales", (66, 67, 68, 69)),
    ArticleSection("Atribuciones de las Cortes Generales", (66, 74, 76, 77, 94)),
    ArticleSection(
        "Funcionamiento del Congreso de los Diputados y del Senado", (72, 73, 78, 79, 80)
    ),
    ArticleSection("El Defensor del Pueblo", (54,)),
)

REQUIRED_ASPECTS = tuple(section.aspect for section in SECTIONS)

_SUBJECT = "las cortes generales"
_SCOPE = ("congreso de los diputados y senado", "defensor del pueblo")


def _matches(title: str) -> bool:
    return states_subject_with_scope(title, _SUBJECT, _SCOPE)


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    provider=AcquiredNormativeMaterial(CONSTITUCION_ESPANOLA, SECTIONS),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=aspects_covered_by_sections,
)
