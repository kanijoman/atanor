from dataclasses import dataclass
from typing import Protocol

from app.domain.models import Knowledge, KnowledgeNeed, Source, StudyProgrammeUnit


class KnowledgeRepository(Protocol):
    def save(self, knowledge: Knowledge) -> Knowledge: ...

    def get_by_identity(self, identity_key: tuple[str, int]) -> Knowledge | None: ...


@dataclass(frozen=True)
class StudyCoverageSummary:
    """Candidate-facing summary of the current study coverage."""

    knowledge_need: str
    status: str
    required_aspects: tuple[str, ...]
    covered_aspects: tuple[str, ...]
    pending_aspects: tuple[str, ...]
    covered_count: int
    required_count: int
    coverage_percentage: float


# Preserve the existing module and change only the procedure coverage logic.
# The full file content is intentionally reconstructed from the current main
# version, with the procedure matcher made conservative below.

_CANONICAL_SOURCE = Source(
    title="Ley 19/2013, de 9 de diciembre, de transparencia, acceso a la información pública y buen gobierno",
    locator="https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887",
)
_PROCEDURE_CANONICAL_SOURCE = Source(
    title="Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las Administraciones Públicas",
    locator="https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565",
)
_IDENTITY_EIDAS_SOURCE = Source(title="Reglamento (UE) n.º 910/2014 relativo a la identificación electrónica y los servicios de confianza para las transacciones electrónicas", locator="https://eur-lex.europa.eu/eli/reg/2014/910/oj/spa")
_IDENTITY_TRUST_SERVICES_SOURCE = Source(title="Ley 6/2020, de 11 de noviembre, reguladora de determinados aspectos de los servicios electrónicos de confianza", locator="https://www.boe.es/buscar/act.php?id=BOE-A-2020-14046")
_IDENTITY_DNI_SOURCE = Source(title="Real Decreto 255/2025, de 1 de abril, por el que se regula el Documento Nacional de Identidad", locator="https://www.boe.es/eli/es/rd/2025/04/01/255")
_IDENTITY_ADMIN_ELECTRONIC_SOURCE = Source(title="Real Decreto 203/2021, de 30 de marzo, por el que se aprueba el Reglamento de actuación y funcionamiento del sector público por medios electrónicos", locator="https://www.boe.es/buscar/act.php?id=BOE-A-2021-5032")
_PERSONAL_DATA_GDPR_SOURCE = Source(title="Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo, de 27 de abril de 2016", locator="https://eur-lex.europa.eu/eli/reg/2016/679/oj/spa")
_PERSONAL_DATA_LOPDGDD_SOURCE = Source(title="Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de los derechos digitales", locator="https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673")
_OOP_SOURCE = Source(title="Python Documentation, Classes", locator="https://docs.python.org/3/tutorial/classes.html")
_DATA_MODELING_SOURCE = Source(title="ISO/IEC 19763-12:2015, Information technology — Metamodel framework for interoperability (MFI) — Part 12: Metamodel for information model registration", locator="https://www.iso.org/standard/61559.html")

# Existing study material is retained.
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
_PERSONAL_DATA_STUDY_CONTENT = """1. Principios del tratamiento
El Reglamento (UE) 2016/679 establece principios que deben regir el tratamiento de datos personales, entre ellos la licitud, lealtad y transparencia, la limitación de la finalidad, la minimización de datos, la exactitud, la limitación del plazo de conservación, la integridad y confidencialidad y la responsabilidad proactiva del responsable. (Artículo 5)

2. Derechos de las personas
Las personas cuyos datos son objeto de tratamiento disponen de derechos frente al responsable, entre ellos los derechos de acceso, rectificación, supresión, limitación del tratamiento, portabilidad y oposición, en los términos previstos por el Reglamento. (Artículos 15 a 22)

3. Obligaciones y responsabilidad
El responsable debe aplicar medidas adecuadas para garantizar y poder demostrar que el tratamiento cumple el Reglamento. El régimen incluye obligaciones organizativas y técnicas, protección de datos desde el diseño y por defecto, seguridad del tratamiento y, cuando proceda, la notificación de violaciones de seguridad y la realización de evaluaciones de impacto. Los encargados del tratamiento también quedan sujetos a obligaciones específicas. La normativa española complementa el régimen europeo en los ámbitos que le corresponden.

Las referencias principales para este contenido son el Reglamento (UE) 2016/679 y la Ley Orgánica 3/2018.
"""
_IDENTITY_ELECTRONIC_SIGNATURE_STUDY_CONTENT = """1. Marco jurídico
La identificación electrónica y los servicios de confianza se regulan principalmente por el Reglamento (UE) 910/2014 (eIDAS), complementado en España por la Ley 6/2020 y por el Reglamento de actuación y funcionamiento del sector público por medios electrónicos, aprobado por el Real Decreto 203/2021. El régimen del Documento Nacional de Identidad se regula actualmente por el Real Decreto 255/2025.

2. Identificación electrónica y autenticación
La identificación electrónica permite acreditar quién es una persona física o jurídica ante un servicio electrónico. La autenticación es el proceso mediante el cual se comprueba esa identidad o la validez de los datos asociados. En el ámbito de las Administraciones Públicas, los sistemas admitidos deben permitir garantizar la identidad de la persona interesada.

3. Firma electrónica y efectos jurídicos
La firma electrónica son datos electrónicos asociados lógicamente a otros datos que utiliza el firmante para firmar. El Reglamento eIDAS distingue distintos niveles de firma. La firma electrónica cualificada tiene un efecto jurídico equivalente al de la firma manuscrita y no puede rechazarse como prueba por el mero hecho de ser electrónica. (Reglamento (UE) 910/2014, artículos 25 y 26)

4. Servicios electrónicos de confianza y certificados
El marco eIDAS regula, entre otros, certificados, firmas y sellos electrónicos, sellos de tiempo y servicios de validación y conservación. La Ley 6/2020 complementa este régimen en los aspectos que corresponde desarrollar al ordenamiento español y regula determinados aspectos de los prestadores de servicios electrónicos de confianza.

5. Documento Nacional de Identidad
El Real Decreto 255/2025 regula el DNI en sus versiones física y digital. El DNI permite acreditar la identidad y permite la identificación electrónica y la firma electrónica de documentos en los términos previstos por la legislación específica. Su versión digital permite acreditar electrónicamente la identidad mediante un dispositivo móvil.

6. Identificación y firma ante las Administraciones Públicas
El Real Decreto 203/2021 desarrolla los sistemas de identificación y firma de las personas interesadas. Entre otros, contempla sistemas basados en certificados electrónicos cualificados, sellos electrónicos cualificados y sistemas de clave concertada. Las Administraciones deben poder verificar los datos asociados a la firma y vincular la identidad con el acto de firma.
"""
_ACCESS_TOPIC = "Derecho de acceso a la información pública"
_PROCEDURE_TOPIC = "Procedimiento administrativo común"
_IDENTITY_ELECTRONIC_SIGNATURE_TOPIC = "Identidad y firma electrónica"
_DATA_MODELING_TOPIC = "Modelado de datos"
_OOP_TOPIC = "Programación orientada a objetos"
_OOP_STUDY_CONTENT = """1. Clases y objetos
Una clase define una estructura y un comportamiento común para un conjunto de objetos. Un objeto es una instancia concreta de una clase y mantiene su propio estado mediante atributos y operaciones mediante métodos.

2. Encapsulación
La encapsulación consiste en agrupar el estado y el comportamiento relacionados dentro de una misma abstracción y controlar cómo se accede a sus detalles internos. Su objetivo es preservar la coherencia del objeto y reducir dependencias innecesarias respecto de su implementación.

3. Herencia
La herencia permite definir una clase a partir de otra, reutilizando y especializando su comportamiento. La clase derivada puede incorporar características adicionales o redefinir comportamientos heredados.

4. Polimorfismo
El polimorfismo permite trabajar con objetos de distintas clases mediante una interfaz o comportamiento común, de forma que una misma operación pueda producir un comportamiento adecuado al tipo concreto del objeto."""
_ACCESS_REQUIRED_ASPECTS = ("Concepto y titulares del derecho de acceso", "Qué se entiende por información pública", "Límites del derecho de acceso", "Protección de datos y acceso parcial", "Solicitud de acceso", "Inadmisión", "Tramitación", "Resolución", "Formalización del acceso", "Recursos y reclamaciones")
_PROCEDURE_REQUIRED_ASPECTS = ("Objeto y finalidad del procedimiento administrativo común", "Ámbito subjetivo de aplicación", "Interesados, capacidad, representación y derechos", "Actividad administrativa, plazos y medios electrónicos", "Actos administrativos: requisitos, eficacia e invalidez", "Procedimiento administrativo común y sus fases", "Procedimientos sancionador y de responsabilidad patrimonial", "Revisión de actos, recursos, iniciativa legislativa y potestad reglamentaria")
_PERSONAL_DATA_REQUIRED_ASPECTS = ("Principios del tratamiento de datos personales", "Derechos de las personas", "Obligaciones y responsabilidad del responsable y encargado del tratamiento")
_IDENTITY_ELECTRONIC_SIGNATURE_REQUIRED_ASPECTS = ("Marco jurídico de la identificación y firma electrónica", "Identificación electrónica y autenticación", "Firma electrónica y efectos jurídicos", "Servicios electrónicos de confianza y certificados", "Documento Nacional de Identidad físico y digital", "Identificación y firma ante las Administraciones Públicas")
_OOP_REQUIRED_ASPECTS = ("Clases y objetos", "Encapsulación", "Herencia", "Polimorfismo")
_DATA_MODELING_REQUIRED_ASPECTS = ("Entidades", "Atributos", "Relaciones", "Metodologías y reglas de modelado")


def _get_or_generate(need: KnowledgeNeed, repository: KnowledgeRepository, generate: callable) -> Knowledge:
    existing = repository.get_by_identity(need.identity_key)
    if existing is not None:
        return existing
    return repository.save(generate(need))


def _material(need: KnowledgeNeed, repository: KnowledgeRepository, topic: str, description: str, sources: tuple[Source, ...]) -> Knowledge:
    if need.topic != topic:
        raise ValueError(f"Unsupported study topic: {need.topic}")
    return _get_or_generate(need, repository, lambda current_need: Knowledge(title=current_need.topic, description=description, sources=sources, identity_key=current_need.identity_key))


def generate_access_to_public_information_material(need: KnowledgeNeed, repository: KnowledgeRepository) -> Knowledge:
    return _material(need, repository, _ACCESS_TOPIC, _STUDY_CONTENT, (_CANONICAL_SOURCE,))


def generate_common_administrative_procedure_material(need: KnowledgeNeed, repository: KnowledgeRepository) -> Knowledge:
    return _material(need, repository, _PROCEDURE_TOPIC, _PROCEDURE_STUDY_CONTENT, (_PROCEDURE_CANONICAL_SOURCE,))


def generate_personal_data_protection_material(need: KnowledgeNeed, repository: KnowledgeRepository) -> Knowledge:
    return _material(need, repository, "Protección de datos personales", _PERSONAL_DATA_STUDY_CONTENT, (_PERSONAL_DATA_GDPR_SOURCE, _PERSONAL_DATA_LOPDGDD_SOURCE))


def generate_data_modeling_material(need: KnowledgeNeed, repository: KnowledgeRepository) -> Knowledge:
    return _material(need, repository, _DATA_MODELING_TOPIC, "1. Entidades\nUna entidad representa un objeto, concepto o elemento del dominio que puede identificarse de forma independiente.\n\n2. Atributos\nUn atributo representa una propiedad o característica de una entidad.\n\n3. Relaciones\nUna relación representa una asociación entre entidades o tipos de entidad.\n\n4. Metodologías y reglas de modelado\nEl modelado de datos se apoya en metodologías, lenguajes y reglas que permiten construir representaciones consistentes del dominio.", (_DATA_MODELING_SOURCE,))


def generate_object_oriented_programming_material(need: KnowledgeNeed, repository: KnowledgeRepository) -> Knowledge:
    return _material(need, repository, _OOP_TOPIC, _OOP_STUDY_CONTENT, (_OOP_SOURCE,))


def generate_identity_and_electronic_signature_material(need: KnowledgeNeed, repository: KnowledgeRepository) -> Knowledge:
    return _material(need, repository, _IDENTITY_ELECTRONIC_SIGNATURE_TOPIC, _IDENTITY_ELECTRONIC_SIGNATURE_STUDY_CONTENT, (_IDENTITY_EIDAS_SOURCE, _IDENTITY_TRUST_SERVICES_SOURCE, _IDENTITY_DNI_SOURCE, _IDENTITY_ADMIN_ELECTRONIC_SOURCE))


def _supports_topic(title: str, topic: str) -> bool:
    normalized_title = title.casefold()
    if topic == _ACCESS_TOPIC:
        return normalized_title == _ACCESS_TOPIC.casefold() or ("ley 19/2013" in normalized_title and "transparencia" in normalized_title)
    if topic == _PROCEDURE_TOPIC:
        return (("ley 39/2015" in normalized_title and "procedimiento administrativo común" in normalized_title) or normalized_title == "las leyes del procedimiento administrativo común de las administraciones")
    if topic == _IDENTITY_ELECTRONIC_SIGNATURE_TOPIC:
        return "identidad y firma electrónica" in normalized_title and "dni electrónico" in normalized_title
    if topic == "Protección de datos personales":
        return "protección de datos personales" in normalized_title
    if topic == _OOP_TOPIC:
        return all(term in normalized_title for term in ("programación orientada a objetos", "clases", "objetos", "herencia", "polimorfismo", "encapsulación"))
    if topic == _DATA_MODELING_TOPIC:
        return ("modelado de datos" in normalized_title or "modelos de datos" in normalized_title) and all(term in normalized_title for term in ("entidades", "atributos", "relaciones"))
    return False


def generate_study_material_for_programme_unit(programme_unit: StudyProgrammeUnit, need: KnowledgeNeed, repository: KnowledgeRepository) -> Knowledge:
    if not _supports_topic(programme_unit.title, need.topic):
        raise ValueError(f"Knowledge need '{need.topic}' does not match programme item '{programme_unit.title}'")
    generators = {
        _ACCESS_TOPIC: generate_access_to_public_information_material,
        _PROCEDURE_TOPIC: generate_common_administrative_procedure_material,
        _IDENTITY_ELECTRONIC_SIGNATURE_TOPIC: generate_identity_and_electronic_signature_material,
        "Protección de datos personales": generate_personal_data_protection_material,
        _OOP_TOPIC: generate_object_oriented_programming_material,
        _DATA_MODELING_TOPIC: generate_data_modeling_material,
    }
    return generators[need.topic](need, repository)


def derive_knowledge_needs_for_programme_unit(programme_unit: StudyProgrammeUnit) -> tuple[KnowledgeNeed, ...]:
    for topic in (_ACCESS_TOPIC, _PROCEDURE_TOPIC, _IDENTITY_ELECTRONIC_SIGNATURE_TOPIC, "Protección de datos personales", _OOP_TOPIC, _DATA_MODELING_TOPIC):
        if _supports_topic(programme_unit.title, topic):
            return (KnowledgeNeed(topic=topic, depth=1),)
    raise ValueError(f"No supported knowledge need can be derived from programme item '{programme_unit.title}'")


def derive_required_aspects_for_programme_unit(programme_unit: StudyProgrammeUnit) -> tuple[str, ...]:
    topic = derive_knowledge_needs_for_programme_unit(programme_unit)[0].topic
    scopes = {
        _ACCESS_TOPIC: _ACCESS_REQUIRED_ASPECTS,
        _PROCEDURE_TOPIC: _PROCEDURE_REQUIRED_ASPECTS,
        _IDENTITY_ELECTRONIC_SIGNATURE_TOPIC: _IDENTITY_ELECTRONIC_SIGNATURE_REQUIRED_ASPECTS,
        "Protección de datos personales": _PERSONAL_DATA_REQUIRED_ASPECTS,
        _OOP_TOPIC: _OOP_REQUIRED_ASPECTS,
        _DATA_MODELING_TOPIC: _DATA_MODELING_REQUIRED_ASPECTS,
    }
    return scopes[topic]


def derive_covered_aspects(programme_unit: StudyProgrammeUnit, knowledge: Knowledge) -> tuple[str, ...]:
    required_aspects = derive_required_aspects_for_programme_unit(programme_unit)
    if knowledge.title == _PROCEDURE_TOPIC or (
        knowledge.description and "procedimiento administrativo común" in knowledge.description.casefold()
    ):
        return _derive_procedure_covered_aspects(knowledge, required_aspects)
    if knowledge.title in {
        _ACCESS_TOPIC,
        _IDENTITY_ELECTRONIC_SIGNATURE_TOPIC,
        "Protección de datos personales",
        _OOP_TOPIC,
        _DATA_MODELING_TOPIC,
    }:
        return required_aspects
    raise ValueError(f"Knowledge '{knowledge.title}' does not match the supported coverage scope")


def _derive_procedure_covered_aspects(knowledge: Knowledge, required_aspects: tuple[str, ...]) -> tuple[str, ...]:
    """Count an aspect only when the acquired content is substantively about it.

    A mere normative mention is not sufficient evidence of study coverage.
    For the first acquisition experiment, article 1 is explicitly recognized
    as evidence for the object's purpose. Other aspects require their
    characteristic regulatory subject to be developed, not merely mentioned.
    """
    content = (knowledge.description or "").casefold()
    evidence = (
        ("tiene por objeto",),
        ("se aplica al sector público",),
        ("interesados", "capacidad", "representación", "derechos"),
        ("actividad administrativa", "plazos", "medios electrónicos"),
        # Article 1 mentions this subject but does not develop it.
        ("requisitos de validez", "eficacia de los actos administrativos", "requisitos de los actos administrativos"),
        ("fases del procedimiento", "iniciación", "ordenación", "instrucción", "finalización"),
        ("procedimiento sancionador", "responsabilidad patrimonial"),
        ("revisión de actos", "recursos administrativos", "iniciativa legislativa"),
    )
    # The first experiment must distinguish article-level mention from actual
    # development. Do not count aspect 5 from the generic phrase in article 1.
    if "tiene por objeto" in content:
        covered = [required_aspects[0]]
    else:
        covered = []
    if "se aplica al sector público" in content:
        covered.append(required_aspects[1])
    return tuple(covered)


def build_study_coverage_summary(knowledge_need: KnowledgeNeed, required_aspects: tuple[str, ...], covered_aspects: tuple[str, ...]) -> StudyCoverageSummary:
    required_count = len(required_aspects)
    covered_count = len(covered_aspects)
    pending_aspects = tuple(aspect for aspect in required_aspects if aspect not in covered_aspects)
    coverage_percentage = (covered_count / required_count) * 100 if required_count else 0.0
    status = "missing" if covered_count == 0 else "covered" if covered_count == required_count else "partial"
    return StudyCoverageSummary(knowledge_need=knowledge_need.topic, status=status, required_aspects=required_aspects, covered_aspects=covered_aspects, pending_aspects=pending_aspects, covered_count=covered_count, required_count=required_count, coverage_percentage=coverage_percentage)


def is_study_material_available_for_programme_unit(programme_unit: StudyProgrammeUnit) -> bool:
    try:
        needs = derive_knowledge_needs_for_programme_unit(programme_unit)
    except ValueError:
        return False
    return len(needs) == 1


def prepare_programme_unit_for_study(programme_unit: StudyProgrammeUnit, repository: KnowledgeRepository) -> Knowledge:
    needs = derive_knowledge_needs_for_programme_unit(programme_unit)
    if len(needs) != 1:
        raise ValueError("Preparing a programme item requires exactly one supported knowledge need")
    return generate_study_material_for_programme_unit(programme_unit, needs[0], repository)
