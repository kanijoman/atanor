"""Study topic: the procedure and public-sector laws, administrative review and judicial appeal.

Designed for the programme unit "Las Leyes del Procedimiento Administrativo Común de las
Administraciones Públicas y del Régimen Jurídico del Sector Público. El procedimiento
administrativo común y sus fases. La revisión de los actos en vía administrativa: revisión de
oficio y recursos administrativos. El recurso contencioso-administrativo. Actividad administrativa
impugnable. Las partes: capacidad, legitimación, representación y defensa."
"""

from app.application.normative_source import LEY_29_1998, LEY_39_2015, LEY_40_2015
from app.application.study_material.coverage import aspects_covered_by_sections
from app.application.study_material.providers import (
    AcquiredNormativeMaterial,
    ArticleRef,
    ArticleSection,
)
from app.application.study_material.topic import StudyTopic
from app.application.study_material.wording import states_subject_with_scope

TOPIC_NAME = (
    "Las Leyes del Procedimiento Administrativo Común y del Régimen Jurídico del Sector Público"
)

# Aspect -> articles that develop it. Explicit contract, pending expert review.
SECTIONS = (
    ArticleSection(
        "Las Leyes del Procedimiento Administrativo Común de las Administraciones Públicas "
        "y del Régimen Jurídico del Sector Público",
        (1, 2),
        also=(ArticleRef(LEY_40_2015, (1, 2, 3)),),
    ),
    ArticleSection("El procedimiento administrativo común y sus fases", (53, 54, 75, 82, 84, 88)),
    ArticleSection(
        "La revisión de los actos en vía administrativa: revisión de oficio y recursos "
        "administrativos",
        (106, 107, 109, 110, 112, 113, 114, 121, 123, 125),
    ),
    ArticleSection("El recurso contencioso-administrativo", (1, 2, 3, 4, 5, 45), LEY_29_1998),
    ArticleSection("Actividad administrativa impugnable", tuple(range(25, 31)), LEY_29_1998),
    ArticleSection(
        "Las partes: capacidad, legitimación, representación y defensa",
        tuple(range(18, 25)),
        LEY_29_1998,
    ),
)

REQUIRED_ASPECTS = tuple(section.aspect for section in SECTIONS)

_SUBJECT = (
    "las leyes del procedimiento administrativo común de las administraciones públicas y del "
    "régimen jurídico del sector público"
)
_SCOPE = (
    "el procedimiento administrativo común y sus fases",
    "la revisión de los actos en vía administrativa",
    "el recurso contencioso-administrativo",
    "actividad administrativa impugnable",
    "las partes: capacidad, legitimación, representación y defensa",
)


def _matches(title: str) -> bool:
    return states_subject_with_scope(title, _SUBJECT, _SCOPE)


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    provider=AcquiredNormativeMaterial(LEY_39_2015, SECTIONS),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=aspects_covered_by_sections,
)
