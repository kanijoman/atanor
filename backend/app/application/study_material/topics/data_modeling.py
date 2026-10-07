"""Study topic: Modelado de datos."""

from app.application.study_material.coverage import aspects_covered_by_sections
from app.application.study_material.topic import StudyTopic
from app.domain.models import Source

TOPIC_NAME = "Modelado de datos"

_ISO_19763_12 = Source(
    title=(
        "ISO/IEC 19763-12:2015, Information technology — Metamodel framework for interoperability "
        "(MFI) — Part 12: Metamodel for information model registration"
    ),
    locator="https://www.iso.org/standard/61559.html",
)

REQUIRED_ASPECTS = (
    "Entidades",
    "Atributos",
    "Relaciones",
    "Modelo relacional",
    "Normalización",
    "Metodologías y reglas de modelado",
)


def _matches(title: str) -> bool:
    return ("modelado de datos" in title or "modelos de datos" in title) and all(
        term in title for term in ("entidades", "atributos", "relaciones")
    )


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    content_file="data_modeling.md",
    sources=(_ISO_19763_12,),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=aspects_covered_by_sections,
)
