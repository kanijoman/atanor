"""Study topic: Derecho de acceso a la información pública (Ley 19/2013), acquired from the BOE."""

from app.application.normative_source import LEY_19_2013
from app.application.study_material.coverage import aspects_covered_by_sections
from app.application.study_material.providers import AcquiredNormativeMaterial, ArticleSection
from app.application.study_material.topic import StudyTopic

TOPIC_NAME = "Derecho de acceso a la información pública"

# Aspect -> articles of Ley 19/2013 that develop it. Explicit contract, pending expert review.
SECTIONS = (
    ArticleSection("Concepto y titulares del derecho de acceso", (12,)),
    ArticleSection("Qué se entiende por información pública", (13,)),
    ArticleSection("Límites del derecho de acceso", (14,)),
    ArticleSection("Protección de datos y acceso parcial", (15, 16)),
    ArticleSection("Solicitud de acceso", (17,)),
    ArticleSection("Inadmisión", (18,)),
    ArticleSection("Tramitación", (19,)),
    ArticleSection("Resolución", (20,)),
    ArticleSection("Formalización del acceso", (22,)),
    ArticleSection("Recursos y reclamaciones", (23, 24)),
)

REQUIRED_ASPECTS = tuple(section.aspect for section in SECTIONS)


def _matches(title: str) -> bool:
    return title == TOPIC_NAME.casefold() or ("ley 19/2013" in title and "transparencia" in title)


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    provider=AcquiredNormativeMaterial(LEY_19_2013, SECTIONS),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=aspects_covered_by_sections,
)
