"""Study topic: Derechos y deberes de los funcionarios (TREBEP and RDL 4/2000).

Designed for the programme unit "Derechos y deberes de los funcionarios. La carrera administrativa.
Promoción interna. El sistema de retribuciones e indemnizaciones. Régimen disciplinario. El
régimen de la Seguridad Social de los funcionarios."
"""

from app.application.normative_source import RDL_4_2000, TREBEP
from app.application.study_material.coverage import aspects_covered_by_sections
from app.application.study_material.providers import AcquiredNormativeMaterial, ArticleSection
from app.application.study_material.topic import StudyTopic
from app.application.study_material.wording import states_subject_with_scope

TOPIC_NAME = "Derechos y deberes de los funcionarios"

# Aspect -> articles that develop it. Explicit contract, pending expert review.
SECTIONS = (
    ArticleSection("Derechos y deberes de los funcionarios", (14, 15, 47, 48, 49, 50, 52, 53, 54)),
    ArticleSection("La carrera administrativa", (16, 17, 20)),
    ArticleSection("Promoción interna", (18,)),
    ArticleSection("El sistema de retribuciones e indemnizaciones", (21, 22, 23, 24, 25, 26, 28)),
    ArticleSection("Régimen disciplinario", tuple(range(93, 99))),
    ArticleSection(
        "El régimen de la Seguridad Social de los funcionarios",
        (1, 2, 3, 4, 11, 12),
        source=RDL_4_2000,
    ),
)

REQUIRED_ASPECTS = tuple(section.aspect for section in SECTIONS)

_SUBJECT = "derechos y deberes de los funcionarios"
_SCOPE = (
    "carrera administrativa",
    "promoción interna",
    "retribuciones e indemnizaciones",
    "régimen disciplinario",
    "seguridad social de los funcionarios",
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
