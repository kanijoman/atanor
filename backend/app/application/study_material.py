from typing import Protocol

from app.domain.models import Knowledge, KnowledgeNeed, Source, StudyProgrammeUnit


class KnowledgeRepository(Protocol):
    def save(self, knowledge: Knowledge) -> Knowledge: ...


_CANONICAL_SOURCE = Source(
    title=(
        "Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la "
        "información pública y buen gobierno"
    ),
    locator="https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887",
)

_STUDY_CONTENT = """1. Concepto y titulares
El derecho de acceso permite a las personas solicitar información pública en los términos establecidos por la Ley 19/2013. Su reconocimiento constituye uno de los mecanismos principales de transparencia de la actividad pública. (Artículo 12)

2. Qué se entiende por información pública
La información pública comprende los contenidos o documentos que obren en poder de las entidades sujetas a la ley y que hayan sido elaborados o adquiridos en el ejercicio de sus funciones. (Artículo 13)

3. Límites del derecho
El acceso puede limitarse cuando resulte necesario para proteger determinados intereses públicos o privados previstos legalmente. La aplicación de un límite debe justificarse y atender al alcance concreto de la información solicitada. (Artículo 14)

4. Protección de datos y acceso parcial
Cuando la información contenga datos personales, deben aplicarse las reglas específicas de protección de datos. Si una parte de la información está afectada por un límite y el resto puede facilitarse, procede valorar el acceso parcial. (Artículos 15 y 16)

5. Solicitud de acceso
La persona interesada puede iniciar el procedimiento mediante una solicitud que identifique la información que solicita. La ley establece el contenido mínimo y las condiciones para presentar la solicitud. (Artículo 17)

6. Inadmisión
Existen causas legalmente previstas que permiten inadmitir una solicitud, entre ellas determinados supuestos relacionados con información en curso de elaboración, información auxiliar o solicitudes que no permitan identificar adecuadamente la información pretendida. (Artículo 18)

7. Tramitación
La solicitud debe tramitarse siguiendo las reglas establecidas por la ley, incluyendo la intervención de terceros cuando resulte procedente y la actuación de la unidad competente en materia de información. (Artículo 19)

8. Resolución
La resolución debe decidir sobre el acceso solicitado dentro del plazo legal y debe estar motivada cuando deniegue el acceso o lo conceda parcialmente. Frente a la resolución existen mecanismos de impugnación previstos legalmente. (Artículo 20)

9. Formalización del acceso
Una vez reconocido el derecho, el acceso debe hacerse efectivo en la forma establecida por la resolución. Cuando proceda, puede facilitarse mediante medios electrónicos y deben respetarse las condiciones derivadas de los límites aplicables. (Artículo 22)

10. Recursos y reclamaciones
Las resoluciones en materia de acceso pueden ser objeto de recurso en los términos previstos por la normativa aplicable. Además, la ley establece una reclamación potestativa ante el Consejo de Transparencia y Buen Gobierno como mecanismo específico de revisión. (Artículos 23 y 24)
"""


def generate_access_to_public_information_material(
    need: KnowledgeNeed,
    repository: KnowledgeRepository,
) -> Knowledge:
    """Generate and persist the first candidate-facing study material."""
    if need.topic != "Derecho de acceso a la información pública":
        raise ValueError(f"Unsupported study topic: {need.topic}")

    knowledge = Knowledge(
        title=need.topic,
        description=_STUDY_CONTENT,
        sources=(_CANONICAL_SOURCE,),
    )
    return repository.save(knowledge)


def generate_study_material_for_programme_unit(
    programme_unit: StudyProgrammeUnit,
    need: KnowledgeNeed,
    repository: KnowledgeRepository,
) -> Knowledge:
    """Generate study material when a programme unit identifies the knowledge need."""
    if programme_unit.title != need.topic:
        raise ValueError(
            f"Knowledge need '{need.topic}' does not match programme item "
            f"'{programme_unit.title}'"
        )

    return generate_access_to_public_information_material(need, repository)


def prepare_programme_unit_for_study(
    programme_unit: StudyProgrammeUnit,
    repository: KnowledgeRepository,
) -> Knowledge:
    """Prepare candidate-facing study material for a programme unit."""
    need = KnowledgeNeed(topic=programme_unit.title, depth=1)
    return generate_study_material_for_programme_unit(
        programme_unit,
        need,
        repository,
    )
