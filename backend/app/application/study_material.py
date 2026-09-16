from typing import Protocol

from app.domain.models import Knowledge, KnowledgeNeed, Source, StudyProgrammeUnit


class KnowledgeRepository(Protocol):
    def save(self, knowledge: Knowledge) -> Knowledge: ...

    def get_by_identity(self, identity_key: tuple[str, int]) -> Knowledge | None: ...


_CANONICAL_SOURCE = Source(
    title=(
        "Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la "
        "información pública y buen gobierno"
    ),
    locator="https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887",
)

_PROCEDURE_CANONICAL_SOURCE = Source(
    title=(
        "Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo "
        "Común de las Administraciones Públicas"
    ),
    locator="https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565",
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

_PROCEDURE_STUDY_CONTENT = """1. Objeto de la ley
La Ley 39/2015 establece las bases del procedimiento administrativo común de las Administraciones Públicas y regula los requisitos de validez y eficacia de los actos administrativos, el procedimiento administrativo común, incluida su especialidad sancionadora y la de responsabilidad de las Administraciones Públicas, y los principios a los que debe ajustarse la iniciativa legislativa y la potestad reglamentaria. (Artículo 1)

2. Ámbito subjetivo de aplicación
La ley se aplica al sector público, que comprende la Administración General del Estado, las Administraciones de las Comunidades Autónomas, las Entidades que integran la Administración Local y el sector público institucional. También determina las entidades que integran este último ámbito. (Artículo 2)
"""


_ACCESS_TOPIC = "Derecho de acceso a la información pública"
_PROCEDURE_TOPIC = "Procedimiento administrativo común"

_PROCEDURE_REQUIRED_ASPECTS = (
    "Objeto y finalidad del procedimiento administrativo común",
    "Ámbito subjetivo de aplicación",
    "Interesados, capacidad, representación y derechos",
    "Actividad administrativa, plazos y medios electrónicos",
    "Actos administrativos: requisitos, eficacia e invalidez",
    "Procedimiento administrativo común y sus fases",
    "Procedimientos sancionador y de responsabilidad patrimonial",
    "Revisión de actos, recursos, iniciativa legislativa y potestad reglamentaria",
)


def _get_or_generate(
    need: KnowledgeNeed,
    repository: KnowledgeRepository,
    generate: callable,
) -> Knowledge:
    existing = repository.get_by_identity(need.identity_key)
    if existing is not None:
        return existing
    return repository.save(generate(need))


def generate_access_to_public_information_material(
    need: KnowledgeNeed,
    repository: KnowledgeRepository,
) -> Knowledge:
    """Generate and persist candidate-facing study material."""
    if need.topic != _ACCESS_TOPIC:
        raise ValueError(f"Unsupported study topic: {need.topic}")

    return _get_or_generate(
        need,
        repository,
        lambda current_need: Knowledge(
            title=current_need.topic,
            description=_STUDY_CONTENT,
            sources=(_CANONICAL_SOURCE,),
            identity_key=current_need.identity_key,
        ),
    )


def generate_common_administrative_procedure_material(
    need: KnowledgeNeed,
    repository: KnowledgeRepository,
) -> Knowledge:
    """Generate candidate-facing material for the common administrative procedure."""
    if need.topic != _PROCEDURE_TOPIC:
        raise ValueError(f"Unsupported study topic: {need.topic}")

    return _get_or_generate(
        need,
        repository,
        lambda current_need: Knowledge(
            title=current_need.topic,
            description=_PROCEDURE_STUDY_CONTENT,
            sources=(_PROCEDURE_CANONICAL_SOURCE,),
            identity_key=current_need.identity_key,
        ),
    )


def generate_study_material_for_programme_unit(
    programme_unit: StudyProgrammeUnit,
    need: KnowledgeNeed,
    repository: KnowledgeRepository,
) -> Knowledge:
    """Generate study material when a programme unit identifies the knowledge need."""
    normalized_title = programme_unit.title.casefold()
    supports_access_topic = (
        normalized_title == _ACCESS_TOPIC.casefold()
        or ("ley 19/2013" in normalized_title and "transparencia" in normalized_title)
    )
    supports_procedure_topic = (
        (
            "ley 39/2015" in normalized_title
            and "procedimiento administrativo común" in normalized_title
        )
        or normalized_title == "las leyes del procedimiento administrativo común de las administraciones"
    )

    if need.topic == _ACCESS_TOPIC and supports_access_topic:
        return generate_access_to_public_information_material(need, repository)

    if need.topic == _PROCEDURE_TOPIC and supports_procedure_topic:
        return generate_common_administrative_procedure_material(need, repository)

    raise ValueError(
        f"Knowledge need '{need.topic}' does not match programme item "
        f"'{programme_unit.title}'"
    )


def derive_knowledge_needs_for_programme_unit(
    programme_unit: StudyProgrammeUnit,
) -> tuple[KnowledgeNeed, ...]:
    """Derive supported knowledge needs from a programme item."""
    normalized_title = programme_unit.title.casefold()
    if (
        normalized_title == _ACCESS_TOPIC.casefold()
        or ("ley 19/2013" in normalized_title and "transparencia" in normalized_title)
    ):
        return (KnowledgeNeed(topic=_ACCESS_TOPIC, depth=1),)

    if (
        "ley 39/2015" in normalized_title
        and "procedimiento administrativo común" in normalized_title
    ) or normalized_title == "las leyes del procedimiento administrativo común de las administraciones":
        return (KnowledgeNeed(topic=_PROCEDURE_TOPIC, depth=1),)

    raise ValueError(
        f"No supported knowledge need can be derived from programme item "
        f"'{programme_unit.title}'"
    )


def derive_required_aspects_for_programme_unit(
    programme_unit: StudyProgrammeUnit,
) -> tuple[str, ...]:
    """Derive the aspects currently required to cover a supported study scope."""
    normalized_title = programme_unit.title.casefold()
    supports_procedure_topic = (
        (
            "ley 39/2015" in normalized_title
            and "procedimiento administrativo común" in normalized_title
        )
        or normalized_title == "las leyes del procedimiento administrativo común de las administraciones"
    )
    if supports_procedure_topic:
        return _PROCEDURE_REQUIRED_ASPECTS

    raise ValueError(
        f"No supported required-aspect scope can be derived from programme item "
        f"'{programme_unit.title}'"
    )


def derive_covered_aspects(
    programme_unit: StudyProgrammeUnit,
    knowledge: Knowledge,
) -> tuple[str, ...]:
    """Derive the aspects explicitly covered by the current study material."""
    required_aspects = derive_required_aspects_for_programme_unit(programme_unit)

    if knowledge.title != _PROCEDURE_TOPIC:
        raise ValueError(
            f"Knowledge '{knowledge.title}' does not match the supported coverage scope"
        )

    return required_aspects[:2]


def is_study_material_available_for_programme_unit(
    programme_unit: StudyProgrammeUnit,
) -> bool:
    """Return whether study material can currently be generated for a programme unit."""
    try:
        needs = derive_knowledge_needs_for_programme_unit(programme_unit)
    except ValueError:
        return False

    return len(needs) == 1


def prepare_programme_unit_for_study(
    programme_unit: StudyProgrammeUnit,
    repository: KnowledgeRepository,
) -> Knowledge:
    """Prepare candidate-facing study material for a programme unit."""
    needs = derive_knowledge_needs_for_programme_unit(programme_unit)
    if len(needs) != 1:
        raise ValueError(
            "Preparing a programme item requires exactly one supported "
            "knowledge need"
        )

    return generate_study_material_for_programme_unit(
        programme_unit,
        needs[0],
        repository,
    )
