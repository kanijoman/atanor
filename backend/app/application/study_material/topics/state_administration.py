"""Study topic: La Administración General del Estado, from the BOE (Ley 40/2015).

Designed for the programme unit "La Administración General del Estado. Órganos centrales. Órganos
superiores y órganos directivos. Órganos territoriales. Otros órganos administrativos. La
Administración del Estado en el exterior."
"""

from app.application.normative_source import LEY_40_2015
from app.application.study_material.coverage import aspects_covered_by_sections
from app.application.study_material.providers import AcquiredNormativeMaterial, ArticleSection
from app.application.study_material.topic import StudyTopic
from app.application.study_material.wording import states_subject_with_scope

TOPIC_NAME = "La Administración General del Estado"

# Aspect -> articles of Ley 40/2015 that develop it. Explicit contract, pending expert review.
SECTIONS = (
    ArticleSection("La Administración General del Estado", (54, 55, 56)),
    ArticleSection("Órganos centrales", (57, 58, 59, 60)),
    ArticleSection("Órganos superiores y órganos directivos", tuple(range(61, 68))),
    ArticleSection("Órganos territoriales", tuple(range(69, 77))),
    ArticleSection("Otros órganos administrativos", (68, 77, 78, 79)),
    ArticleSection("La Administración del Estado en el exterior", (80, 81)),
)

REQUIRED_ASPECTS = tuple(section.aspect for section in SECTIONS)

_SUBJECT = "la administración general del estado"
_SCOPE = (
    "órganos centrales",
    "órganos superiores y órganos directivos",
    "órganos territoriales",
    "otros órganos administrativos",
    "en el exterior",
)


def _matches(title: str) -> bool:
    return states_subject_with_scope(title, _SUBJECT, _SCOPE)


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    provider=AcquiredNormativeMaterial(LEY_40_2015, SECTIONS),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=aspects_covered_by_sections,
)
