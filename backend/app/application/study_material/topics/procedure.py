"""Study topic: Procedimiento administrativo común (Ley 39/2015)."""

from app.application.study_material.topic import StudyTopic
from app.domain.models import Knowledge, Source

TOPIC_NAME = "Procedimiento administrativo común"

_LEY_39_2015 = Source(
    title=(
        "Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las "
        "Administraciones Públicas"
    ),
    locator="https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565",
)

REQUIRED_ASPECTS = (
    "Objeto y finalidad del procedimiento administrativo común",
    "Ámbito subjetivo de aplicación",
    "Interesados, capacidad, representación y derechos",
    "Actividad administrativa, plazos y medios electrónicos",
    "Actos administrativos: requisitos, eficacia e invalidez",
    "Procedimiento administrativo común y sus fases",
    "Procedimientos sancionador y de responsabilidad patrimonial",
    "Revisión de actos, recursos, iniciativa legislativa y potestad reglamentaria",
)

_UNIT_TITLE = "las leyes del procedimiento administrativo común de las administraciones"


def _matches(title: str) -> bool:
    return (
        "ley 39/2015" in title and "procedimiento administrativo común" in title
    ) or title == _UNIT_TITLE


def _covered_aspects(knowledge: Knowledge, required_aspects: tuple[str, ...]) -> tuple[str, ...]:
    """Count an aspect only when the material is substantively about it.

    A mere normative mention is not sufficient evidence of study coverage.
    Article 1 is recognized as evidence for the object's purpose and article 2
    for the subjective scope; other aspects need their regulatory subject to
    be developed, not merely mentioned.
    """
    content = (knowledge.description or "").casefold()
    covered: list[str] = []
    if (
        "tiene por objeto" in content
        or "establece las bases del procedimiento administrativo común" in content
    ):
        covered.append(required_aspects[0])
    if "se aplica al sector público" in content:
        covered.append(required_aspects[1])
    return tuple(covered)


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    content_file="procedure.md",
    sources=(_LEY_39_2015,),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=_covered_aspects,
)
