"""Study topic: El Gobierno y la Administración, from the BOE (Constitution and Ley 50/1997).

Designed for the programme unit "El Gobierno y la Administración. El Presidente del Gobierno. El
Consejo de Ministros. Designación, causas de cese y responsabilidad del Gobierno."
"""

from app.application.normative_source import CONSTITUCION_ESPANOLA, LEY_50_1997
from app.application.study_material.coverage import aspects_covered_by_sections
from app.application.study_material.providers import (
    AcquiredNormativeMaterial,
    ArticleRef,
    ArticleSection,
)
from app.application.study_material.topic import StudyTopic
from app.application.study_material.wording import states_subject_with_scope

TOPIC_NAME = "El Gobierno y la Administración"

# Aspect -> articles that develop it. Explicit contract, pending expert review.
SECTIONS = (
    ArticleSection(
        "El Gobierno y la Administración", (97, 103), also=(ArticleRef(LEY_50_1997, (1,)),)
    ),
    ArticleSection("El Presidente del Gobierno", (98,), also=(ArticleRef(LEY_50_1997, (2,)),)),
    ArticleSection("El Consejo de Ministros", (5, 17, 18), source=LEY_50_1997),
    ArticleSection(
        "Designación, causas de cese y responsabilidad del Gobierno",
        (99, 100, 101, 102, 108, 112, 113, 114),
        also=(ArticleRef(LEY_50_1997, (12, 21)),),
    ),
)

REQUIRED_ASPECTS = tuple(section.aspect for section in SECTIONS)

_SUBJECT = "el gobierno y la administración"
_SCOPE = ("presidente del gobierno", "consejo de ministros", "causas de cese")


def _matches(title: str) -> bool:
    return states_subject_with_scope(title, _SUBJECT, _SCOPE)


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    provider=AcquiredNormativeMaterial(CONSTITUCION_ESPANOLA, SECTIONS),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=aspects_covered_by_sections,
)
