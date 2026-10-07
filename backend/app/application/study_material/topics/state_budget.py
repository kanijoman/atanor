"""Study topic: El presupuesto del Estado en España (Constitution and Ley 47/2003).

Designed for the programme unit "El presupuesto del Estado en España. Contenido, elaboración y
estructura. Fases del ciclo presupuestario."
"""

from app.application.normative_source import CONSTITUCION_ESPANOLA, LEY_47_2003
from app.application.study_material.coverage import aspects_covered_by_sections
from app.application.study_material.providers import (
    AcquiredNormativeMaterial,
    ArticleRef,
    ArticleSection,
)
from app.application.study_material.topic import StudyTopic
from app.application.study_material.wording import states_subject_with_scope

TOPIC_NAME = "El presupuesto del Estado en España"

# Aspect -> articles that develop it. Explicit contract, pending expert review.
SECTIONS = (
    ArticleSection("El presupuesto del Estado en España", (32,), source=LEY_47_2003),
    ArticleSection("Contenido", (33, 34, 35), source=LEY_47_2003),
    ArticleSection(
        "Elaboración",
        (36, 37, 38),
        source=LEY_47_2003,
        also=(ArticleRef(CONSTITUCION_ESPANOLA, (134,)),),
    ),
    ArticleSection("Estructura", tuple(range(39, 45)), source=LEY_47_2003),
    ArticleSection(
        "Fases del ciclo presupuestario",
        (26, 27, 36, 37, 73, 75, 130, 131, 132, 140),
        source=LEY_47_2003,
    ),
)

REQUIRED_ASPECTS = tuple(section.aspect for section in SECTIONS)

_SUBJECT = "el presupuesto del estado en españa"
_SCOPE = ("contenido, elaboración y estructura", "ciclo presupuestario")


def _matches(title: str) -> bool:
    return states_subject_with_scope(title, _SUBJECT, _SCOPE)


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    provider=AcquiredNormativeMaterial(LEY_47_2003, SECTIONS),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=aspects_covered_by_sections,
)
