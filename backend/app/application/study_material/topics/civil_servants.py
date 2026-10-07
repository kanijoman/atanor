"""Study topic: El personal funcionario al servicio de las Administraciones públicas (TREBEP).

Designed for the programme unit "El personal funcionario al servicio de las Administraciones
públicas: concepto y clases. Régimen jurídico. El Registro Central de Personal. Programación de
efectivos y Oferta de Empleo Público. Selección. Provisión de puestos de trabajo. Situaciones
administrativas de los funcionarios."
"""

from app.application.normative_source import TREBEP
from app.application.study_material.coverage import aspects_covered_by_sections
from app.application.study_material.providers import AcquiredNormativeMaterial, ArticleSection
from app.application.study_material.topic import StudyTopic
from app.application.study_material.wording import states_subject_with_scope

TOPIC_NAME = "El personal funcionario al servicio de las Administraciones públicas"

# Aspect -> articles of the TREBEP that develop it. Explicit contract, pending expert review.
SECTIONS = (
    ArticleSection("Concepto y clases de empleados públicos", (8, 9, 10, 11, 12, 13)),
    ArticleSection("Régimen jurídico", (1, 2, 3, 6, 7)),
    ArticleSection("El Registro Central de Personal", (71,)),
    ArticleSection("Programación de efectivos y Oferta de Empleo Público", (69, 70)),
    ArticleSection("Selección", (55, 56, 59, 60, 61, 62)),
    ArticleSection("Provisión de puestos de trabajo", (78, 79, 80, 81, 82, 84)),
    ArticleSection("Situaciones administrativas de los funcionarios", tuple(range(85, 92))),
)

REQUIRED_ASPECTS = tuple(section.aspect for section in SECTIONS)

_SUBJECT = "el personal funcionario al servicio de las administraciones públicas"
_SCOPE = (
    "régimen jurídico",
    "registro central de personal",
    "oferta de empleo público",
    "selección",
    "provisión de puestos de trabajo",
    "situaciones administrativas",
)


def _matches(title: str) -> bool:
    return states_subject_with_scope(title, _SUBJECT, _SCOPE)


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    provider=AcquiredNormativeMaterial(TREBEP, SECTIONS),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=aspects_covered_by_sections,
)
