"""Study topic: Protección de datos personales."""

from app.application.study_material.coverage import all_required_covered
from app.application.study_material.topic import StudyTopic
from app.domain.models import Source

TOPIC_NAME = "Protección de datos personales"

_GDPR = Source(
    title="Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo, de 27 de abril de 2016",
    locator="https://eur-lex.europa.eu/eli/reg/2016/679/oj/spa",
)

_LOPDGDD = Source(
    title=(
        "Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de "
        "los derechos digitales"
    ),
    locator="https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673",
)

REQUIRED_ASPECTS = (
    "Principios del tratamiento de datos personales",
    "Derechos de las personas",
    "Obligaciones y responsabilidad del responsable y encargado del tratamiento",
)


def _matches(title: str) -> bool:
    return "protección de datos personales" in title


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    content_file="personal_data.md",
    sources=(_GDPR, _LOPDGDD),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=all_required_covered,
)
