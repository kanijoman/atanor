"""Study topic: Derecho de acceso a la información pública (Ley 19/2013)."""

from app.application.study_material.coverage import aspects_covered_by_sections
from app.application.study_material.topic import StudyTopic
from app.domain.models import Source

TOPIC_NAME = "Derecho de acceso a la información pública"

_LEY_19_2013 = Source(
    title=(
        "Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen "
        "gobierno"
    ),
    locator="https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887",
)

REQUIRED_ASPECTS = (
    "Concepto y titulares del derecho de acceso",
    "Qué se entiende por información pública",
    "Límites del derecho de acceso",
    "Protección de datos y acceso parcial",
    "Solicitud de acceso",
    "Inadmisión",
    "Tramitación",
    "Resolución",
    "Formalización del acceso",
    "Recursos y reclamaciones",
)


def _matches(title: str) -> bool:
    return title == TOPIC_NAME.casefold() or ("ley 19/2013" in title and "transparencia" in title)


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    content_file="access.md",
    sources=(_LEY_19_2013,),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=aspects_covered_by_sections,
)
