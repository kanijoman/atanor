"""Study topic: Programación orientada a objetos."""

from app.application.study_material.coverage import aspects_covered_by_signals
from app.application.study_material.topic import StudyTopic
from app.domain.models import Source

TOPIC_NAME = "Programación orientada a objetos"

_PYTHON_CLASSES = Source(
    title="Python Documentation, Classes",
    locator="https://docs.python.org/3/tutorial/classes.html",
)

REQUIRED_ASPECTS = (
    "Objetos y clases",
    "Herencia",
    "Métodos",
    "Sobrecarga",
    "Ventajas e inconvenientes de la programación orientada a objetos",
    "Patrones de diseño",
    "Lenguaje de modelado unificado (UML)",
)

_REQUIRED_TERMS = ("clases", "objetos", "herencia")
_ANY_OF_TERMS = ("métodos", "sobrecarga", "patrones de diseño", "uml")

_ASPECT_SIGNALS = (
    ("Objetos y clases", ("clase", "objeto")),
    ("Herencia", ("herencia",)),
    ("Métodos", ("método",)),
    ("Sobrecarga", ("sobrecarga",)),
    (
        "Ventajas e inconvenientes de la programación orientada a objetos",
        ("ventaja", "inconveniente"),
    ),
    ("Patrones de diseño", ("patrones de diseño",)),
    ("Lenguaje de modelado unificado (UML)", ("uml",)),
)


def _matches(title: str) -> bool:
    return (
        "programación orientada a objetos" in title
        and all(term in title for term in _REQUIRED_TERMS)
        and any(term in title for term in _ANY_OF_TERMS)
    )


TOPIC = StudyTopic(
    name=TOPIC_NAME,
    matches=_matches,
    content_file="object_oriented.md",
    sources=(_PYTHON_CLASSES,),
    required_aspects=REQUIRED_ASPECTS,
    covered_aspects=aspects_covered_by_signals(_ASPECT_SIGNALS),
)
