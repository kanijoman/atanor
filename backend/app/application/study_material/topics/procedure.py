"""Study topic: Procedimiento administrativo común (Ley 39/2015), acquired from the BOE."""

from app.application.normative_source import LEY_39_2015
from app.application.study_material.coverage import aspects_covered_by_sections
from app.application.study_material.providers import AcquiredNormativeMaterial, ArticleSection
from app.application.study_material.topic import StudyTopic
from app.application.study_material.wording import leading_statement

TOPIC_NAME = "Procedimiento administrativo común"

# Aspect -> key articles of Ley 39/2015 that develop it. Explicit contract, pending expert review.
SECTIONS = (
    ArticleSection("Objeto y finalidad del procedimiento administrativo común", (1,)),
    ArticleSection("Ámbito subjetivo de aplicación", (2,)),
    ArticleSection("Interesados, capacidad, representación y derechos", (3, 4, 5, 13)),
    ArticleSection("Actividad administrativa, plazos y medios electrónicos", (14, 16, 29, 30)),
    ArticleSection("Actos administrativos: requisitos, eficacia e invalidez", (34, 35, 39, 47, 48)),
    ArticleSection("Procedimiento administrativo común y sus fases", (53, 54, 75, 82, 84, 88)),
    ArticleSection("Procedimientos sancionador y de responsabilidad patrimonial", (63, 64, 67)),
    ArticleSection(
        "Revisión de actos, recursos, iniciativa legislativa y potestad reglamentaria",
        (106, 112, 121, 127),
    ),
)

REQUIRED_ASPECTS = tuple(section.aspect for section in SECTIONS)

_UNIT_LEAD = "las leyes del procedimiento administrativo común de las administraciones"


def _matches(title: str) -> bool:
    lead = leading_statement(title)
    return (
        "ley 39/2015" in lead and "procedimiento administrativo común" in lead
    ) or lead.startswith(_UNIT_LEAD)


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    provider=AcquiredNormativeMaterial(LEY_39_2015, SECTIONS),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=aspects_covered_by_sections,
)
