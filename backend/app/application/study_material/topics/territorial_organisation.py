"""Study topic: La organización territorial del Estado, from the BOE (Constitution, Ley 7/1985).

Designed for the programme unit "La Organización territorial del Estado: las Comunidades
Autónomas: Constitución y distribución de competencias entre el Estado y las Comunidades
Autónomas. La Administración local: entidades que la integran. La provincia, el municipio y la
isla."
"""

from app.application.normative_source import CONSTITUCION_ESPANOLA, LEY_7_1985
from app.application.study_material.coverage import aspects_covered_by_sections
from app.application.study_material.providers import (
    AcquiredNormativeMaterial,
    ArticleRef,
    ArticleSection,
)
from app.application.study_material.topic import StudyTopic
from app.application.study_material.wording import states_subject_with_scope

TOPIC_NAME = "La organización territorial del Estado"

# Aspect -> articles that develop it. Explicit contract, pending expert review.
SECTIONS = (
    ArticleSection("La organización territorial del Estado", (137, 138, 139)),
    ArticleSection("Las Comunidades Autónomas: constitución", (143, 144, 145, 146, 147, 151, 152)),
    ArticleSection(
        "Distribución de competencias entre el Estado y las Comunidades Autónomas",
        (148, 149, 150),
    ),
    ArticleSection(
        "La Administración local: entidades que la integran",
        (137, 140),
        also=(ArticleRef(LEY_7_1985, (1, 2, 3, 4)),),
    ),
    ArticleSection(
        "La provincia, el municipio y la isla",
        (141,),
        also=(ArticleRef(LEY_7_1985, (11, 12, 25, 26, 31, 32, 36, 41)),),
    ),
)

REQUIRED_ASPECTS = tuple(section.aspect for section in SECTIONS)

_SUBJECT = "la organización territorial del estado"
_SCOPE = (
    "comunidades autónomas",
    "distribución de competencias",
    "la provincia, el municipio y la isla",
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
