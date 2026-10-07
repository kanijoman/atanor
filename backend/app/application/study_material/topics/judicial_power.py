"""Study topic: El Poder Judicial, from the BOE.

Designed for the programme unit "El Poder Judicial. El Consejo General del Poder Judicial. El
Tribunal Supremo. La organización judicial española."
"""

from app.application.normative_source import CONSTITUCION_ESPANOLA
from app.application.study_material.coverage import aspects_covered_by_sections
from app.application.study_material.providers import AcquiredNormativeMaterial, ArticleSection
from app.application.study_material.topic import StudyTopic
from app.application.study_material.wording import states_subject_with_scope

TOPIC_NAME = "El Poder Judicial"

# Aspect -> articles of the Constitution that develop it. Explicit contract, pending expert review.
SECTIONS = (
    ArticleSection("Principios del Poder Judicial", (117, 118, 119, 120, 121)),
    ArticleSection("El Consejo General del Poder Judicial", (122,)),
    ArticleSection("El Tribunal Supremo", (123,)),
    ArticleSection("La organización judicial española", (117, 124, 125, 126, 152)),
)

REQUIRED_ASPECTS = tuple(section.aspect for section in SECTIONS)

_SUBJECT = "el poder judicial"
_SCOPE = ("consejo general del poder judicial", "tribunal supremo", "organización judicial")


def _matches(title: str) -> bool:
    return states_subject_with_scope(title, _SUBJECT, _SCOPE)


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    provider=AcquiredNormativeMaterial(CONSTITUCION_ESPANOLA, SECTIONS),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=aspects_covered_by_sections,
)
