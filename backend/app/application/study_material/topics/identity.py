"""Study topic: Identidad y firma electrónica."""

from app.application.study_material.coverage import aspects_covered_by_sections
from app.application.study_material.providers import CuratedMaterial
from app.application.study_material.topic import StudyTopic
from app.domain.models import Source

TOPIC_NAME = "Identidad y firma electrónica"

_EIDAS = Source(
    title=(
        "Reglamento (UE) n.º 910/2014 relativo a la identificación electrónica y los servicios de "
        "confianza para las transacciones electrónicas"
    ),
    locator="https://eur-lex.europa.eu/eli/reg/2014/910/oj/spa",
)

_LEY_6_2020 = Source(
    title=(
        "Ley 6/2020, de 11 de noviembre, reguladora de determinados aspectos de los servicios "
        "electrónicos de confianza"
    ),
    locator="https://www.boe.es/buscar/act.php?id=BOE-A-2020-14046",
)

_RD_255_2025 = Source(
    title=(
        "Real Decreto 255/2025, de 1 de abril, por el que se regula "
        "el Documento Nacional de Identidad"
    ),
    locator="https://www.boe.es/eli/es/rd/2025/04/01/255",
)

_RD_203_2021 = Source(
    title=(
        "Real Decreto 203/2021, de 30 de marzo, por el que se aprueba el Reglamento de actuación "
        "y funcionamiento del sector público por medios electrónicos"
    ),
    locator="https://www.boe.es/buscar/act.php?id=BOE-A-2021-5032",
)

REQUIRED_ASPECTS = (
    "Marco jurídico de la identificación y firma electrónica",
    "Identificación electrónica y autenticación",
    "Firma electrónica y efectos jurídicos",
    "Servicios electrónicos de confianza y certificados",
    "Documento Nacional de Identidad físico y digital",
    "Identificación y firma ante las Administraciones Públicas",
)


def _matches(title: str) -> bool:
    return "identidad y firma electrónica" in title and "dni electrónico" in title


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    provider=CuratedMaterial("identity.md", (_EIDAS, _LEY_6_2020, _RD_255_2025, _RD_203_2021)),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=aspects_covered_by_sections,
)
