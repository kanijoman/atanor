"""Probe candidate-facing study content coverage against canonical evidence.

This is a deterministic product experiment, not a production contract. It
checks whether semantic coverage validation is useful across more than one
KnowledgeNeed from the same canonical legal corpus.
"""

from dataclasses import dataclass
from urllib.request import Request, urlopen

from canonical_knowledge_construction import CANONICAL_SOURCE, _extract_articles


@dataclass(frozen=True)
class StudySection:
    title: str
    content: str
    evidence_articles: tuple[str, ...]
    covered_points: tuple[str, ...]
    exam_points: tuple[str, ...] = ()


@dataclass(frozen=True)
class CoverageResult:
    concept: str
    status: str
    covered_aspects: tuple[str, ...]
    missing_aspects: tuple[str, ...]


@dataclass(frozen=True)
class KnowledgeNeedCase:
    title: str
    evidence_articles: tuple[str, ...]
    sections: tuple[StudySection, ...]
    required_aspects: dict[str, tuple[str, ...]]
    covered_aspects: dict[str, tuple[str, ...]]


CANONICAL_LOCATOR = CANONICAL_SOURCE["locator"]

ACCESS_CASE = KnowledgeNeedCase(
    title="Derecho de acceso a la información pública",
    evidence_articles=tuple(str(number) for number in range(12, 25)),
    sections=(
        StudySection(
            "1. Qué es el derecho de acceso",
            "La Ley reconoce a todas las personas el derecho a acceder a la información pública.",
            ("12",),
            ("right_holder",),
            ("Titularidad: todas las personas.",),
        ),
        StudySection(
            "2. Qué se considera información pública",
            "Es información pública la contenida en documentos o contenidos, cualquiera que sea su formato o soporte, que esté en poder de los sujetos incluidos en el ámbito de aplicación y haya sido elaborada o adquirida en el ejercicio de sus funciones.",
            ("13",),
            ("public_information",),
            ("El formato o soporte no altera la definición.",),
        ),
        StudySection(
            "3. Límites del derecho",
            "El acceso puede limitarse cuando perjudique alguno de los intereses protegidos por la Ley. La aplicación del límite debe estar justificada y ser proporcionada, atendiendo a las circunstancias del caso concreto.",
            ("14",),
            ("access_limits",),
            ("Los límites deben distinguirse de las causas de inadmisión.",),
        ),
        StudySection(
            "4. Protección de datos y acceso parcial",
            "Cuando la información contenga datos personales debe aplicarse el régimen correspondiente. Cuando un límite afecte solo a una parte de la información, puede existir acceso parcial si es posible separar la información protegida sin alterar el sentido de la restante.",
            ("15", "16"),
            ("personal_data", "partial_access"),
            (
                "Distinguir protección de datos de los restantes límites.",
                "Recordar la figura del acceso parcial.",
            ),
        ),
        StudySection(
            "5. Cómo se ejerce el derecho",
            "La solicitud debe identificar al solicitante y la información solicitada, proporcionar un medio de contacto y, en su caso, indicar la modalidad preferida. No es obligatorio motivarla.",
            ("17",),
            ("application_requirements",),
            ("La ausencia de motivación no es causa de rechazo.",),
        ),
        StudySection(
            "6. Cuándo puede inadmitirse una solicitud",
            "La Ley establece causas de inadmisión, entre ellas información en curso de elaboración o publicación general, carácter auxiliar o de apoyo, necesidad de reelaboración, falta de posesión por el órgano cuando se desconoce el competente, y solicitudes manifiestamente repetitivas o abusivas en los términos legales.",
            ("18",),
            ("inadmissibility",),
            ("Las causas de inadmisión deben distinguirse de los límites del artículo 14.",),
        ),
        StudySection(
            "7. Tramitación",
            "Durante la tramitación pueden intervenir terceros afectados y puede procederse a la remisión prevista legalmente.",
            ("19",),
            ("processing",),
        ),
        StudySection(
            "8. Resolución",
            "La resolución debe notificarse con carácter general en el plazo máximo de un mes, ampliable por otro mes en determinados supuestos de volumen o complejidad. El silencio produce el efecto previsto por la Ley.",
            ("20",),
            ("resolution",),
            ("Plazo general: un mes. Puede existir ampliación por otro mes.",),
        ),
        StudySection(
            "9. Unidades de información",
            "Las unidades de información participan en la gestión de las solicitudes conforme al régimen establecido por la Ley.",
            ("21",),
            ("information_units",),
        ),
        StudySection(
            "10. Formalización del acceso",
            "El acceso se realiza preferentemente por vía electrónica. Como regla general es gratuito, aunque las copias o transformaciones pueden estar sujetas a las exacciones legalmente previstas.",
            ("22",),
            ("formalisation",),
            ("Preferencia por el medio electrónico. Acceso gratuito como regla general.",),
        ),
        StudySection(
            "11. Recursos",
            "Las resoluciones en materia de acceso pueden ser objeto de los recursos previstos legalmente.",
            ("23",),
            ("appeal",),
        ),
        StudySection(
            "12. Reclamación",
            "La Ley establece una reclamación potestativa ante el Consejo de Transparencia y Buen Gobierno, previa a la vía contencioso-administrativa, en los términos legalmente previstos.",
            ("24",),
            ("claim",),
            ("La reclamación es potestativa y previa a la vía contencioso-administrativa.",),
        ),
    ),
    required_aspects={
        "right_holder": ("all persons are entitled",),
        "public_information": (
            "documents or content",
            "any format or medium",
            "held by covered subjects",
            "prepared or acquired in the exercise of functions",
        ),
        "access_limits": (
            "protected interests",
            "justified application",
            "proportional application",
            "case-specific circumstances",
        ),
        "personal_data": (
            "specific personal-data regime",
            "distinction from general access limits",
        ),
        "partial_access": (
            "separable protected part",
            "remaining information keeps its meaning",
        ),
        "application_requirements": (
            "applicant identification",
            "requested information",
            "contact method",
            "preferred access method when applicable",
            "no duty to provide reasons",
        ),
        "inadmissibility": (
            "information under preparation or general publication",
            "auxiliary or support information",
            "re-elaboration requirement",
            "information not held when competent body is unknown",
            "manifestly repetitive or abusive requests",
        ),
        "processing": (
            "affected third parties",
            "legal referral to another body",
        ),
        "resolution": (
            "notification",
            "one-month deadline",
            "possible one-month extension",
            "reasoned denial",
            "negative administrative silence",
            "judicial challenge",
            "optional claim",
        ),
        "information_units": (
            "specialised information units",
            "support for access-request management",
        ),
        "formalisation": (
            "electronic access preference",
            "access generally free",
            "copies or format transformations may incur charges",
        ),
        "appeal": ("available legal appeals",),
        "claim": (
            "claim before the Transparency and Good Governance Council",
            "optional nature",
            "prior to contentious-administrative proceedings",
        ),
    },
    covered_aspects={
        "right_holder": ("all persons are entitled",),
        "public_information": (
            "documents or content",
            "any format or medium",
            "held by covered subjects",
            "prepared or acquired in the exercise of functions",
        ),
        "access_limits": (
            "justified application",
            "proportional application",
            "case-specific circumstances",
        ),
        "personal_data": ("specific personal-data regime",),
        "partial_access": (
            "separable protected part",
            "remaining information keeps its meaning",
        ),
        "application_requirements": (
            "applicant identification",
            "requested information",
            "contact method",
            "preferred access method when applicable",
            "no duty to provide reasons",
        ),
        "inadmissibility": (
            "information under preparation or general publication",
            "auxiliary or support information",
            "re-elaboration requirement",
            "information not held when competent body is unknown",
            "manifestly repetitive or abusive requests",
        ),
        "processing": ("affected third parties", "legal referral to another body"),
        "resolution": (
            "notification",
            "one-month deadline",
            "possible one-month extension",
            "negative administrative silence",
        ),
        "information_units": ("support for access-request management",),
        "formalisation": (
            "electronic access preference",
            "access generally free",
            "copies or format transformations may incur charges",
        ),
        "appeal": ("available legal appeals",),
        "claim": (
            "claim before the Transparency and Good Governance Council",
            "optional nature",
            "prior to contentious-administrative proceedings",
        ),
    },
)


PUBLICITY_CASE = KnowledgeNeedCase(
    title="Principios y obligaciones generales de publicidad activa",
    evidence_articles=("5", "6", "6 bis", "7", "8", "9", "10", "11"),
    sections=(
        StudySection(
            "1. Qué exige la publicidad activa",
            "Los sujetos obligados deben publicar de forma periódica y actualizada la información relevante para garantizar la transparencia de su actividad y el funcionamiento y control de la actuación pública.",
            ("5",),
            ("publication_duty", "periodicity_update"),
            ("La publicidad activa se produce sin esperar una solicitud concreta.",),
        ),
        StudySection(
            "2. Cómo debe publicarse la información",
            "La información debe publicarse de forma clara, estructurada y comprensible, preferiblemente en formatos reutilizables, facilitando su accesibilidad, interoperabilidad, calidad, reutilización, identificación y localización. Debe ser de acceso fácil y gratuito.",
            ("5",),
            ("publication_quality", "accessibility", "reusability"),
            ("Distinguir publicidad activa de simple disponibilidad documental.",),
        ),
        StudySection(
            "3. Información institucional, organizativa y de planificación",
            "Debe publicarse información sobre las funciones, la normativa aplicable y la estructura organizativa, incluido un organigrama actualizado. Las Administraciones Públicas deben publicar sus planes y programas y evaluar y publicar periódicamente su grado de cumplimiento y resultados.",
            ("6",),
            ("institutional_information", "planning_information", "evaluation"),
        ),
        StudySection(
            "4. Registro de actividades de tratamiento",
            "Determinados sujetos deben publicar su inventario de actividades de tratamiento conforme a la normativa de protección de datos.",
            ("6 bis",),
            ("processing_activities",),
        ),
        StudySection(
            "5. Información de relevancia jurídica",
            "Las Administraciones Públicas deben publicar, entre otros contenidos, determinadas directrices, instrucciones, acuerdos, circulares o respuestas con relevancia interpretativa o efectos jurídicos, así como proyectos normativos, memorias e informes de expedientes y documentos sometidos a información pública en los términos legales.",
            ("7",),
            ("legal_relevance_information",),
            ("Identificar las principales categorías de información jurídica sometida a publicidad.",),
        ),
        StudySection(
            "6. Información económica, presupuestaria y estadística",
            "Los sujetos obligados deben hacer pública la información mínima que la Ley determina sobre actos de gestión administrativa con repercusión económica o presupuestaria y otros contenidos económicos, presupuestarios y estadísticos previstos legalmente.",
            ("8",),
            ("economic_information",),
        ),
        StudySection(
            "7. Control del cumplimiento",
            "El cumplimiento de las obligaciones de publicidad activa de la Administración General del Estado está sometido al control del Consejo de Transparencia y Buen Gobierno, que puede dictar medidas para corregir incumplimientos e iniciar actuaciones disciplinarias en los términos legales.",
            ("9",),
            ("compliance_control", "enforcement"),
            ("El control del cumplimiento forma parte del régimen de publicidad activa.",),
        ),
        StudySection(
            "8. Portal de la Transparencia",
            "La Administración General del Estado desarrolla el Portal de la Transparencia para facilitar el acceso a la información correspondiente a su ámbito de actuación, incluida la información cuyo acceso sea solicitado con mayor frecuencia.",
            ("10",),
            ("transparency_portal", "frequently_requested_information"),
            ("El Portal facilita el acceso, pero no sustituye el contenido de las obligaciones de publicidad activa.",),
        ),
        StudySection(
            "9. Principios técnicos",
            "La información del Portal debe ajustarse a principios de accesibilidad, interoperabilidad y reutilización, de acuerdo con las prescripciones técnicas y normas aplicables.",
            ("11",),
            ("technical_principles",),
            ("Recordar la tríada: accesibilidad, interoperabilidad y reutilización.",),
        ),
    ),
    required_aspects={
        "publication_duty": (
            "mandatory publication",
            "relevant transparency information",
        ),
        "periodicity_update": (
            "periodic publication",
            "updated information",
        ),
        "publication_quality": (
            "clear structured understandable publication",
            "easy access",
            "free access",
        ),
        "accessibility": (
            "accessibility",
            "identification and location mechanisms",
        ),
        "reusability": (
            "reusable formats",
            "reusability",
        ),
        "institutional_information": (
            "functions and applicable rules",
            "organisational structure and updated organigram",
        ),
        "planning_information": (
            "annual and multiannual plans",
            "objectives activities means and timing",
        ),
        "evaluation": (
            "periodic evaluation",
            "publication of compliance results and indicators",
        ),
        "processing_activities": ("processing activities inventory",),
        "legal_relevance_information": (
            "interpretative instructions or agreements",
            "draft normative texts",
            "regulatory preparation reports",
            "documents subject to public information",
        ),
        "economic_information": (
            "economic or budgetary management information",
            "statistical information",
        ),
        "compliance_control": (
            "Council of Transparency and Good Governance control",
            "measures to correct non-compliance",
        ),
        "enforcement": (
            "disciplinary proceedings for repeated non-compliance",
        ),
        "transparency_portal": (
            "General State Administration portal",
            "facilitates access to transparency information",
        ),
        "frequently_requested_information": (
            "frequently requested information",
        ),
        "technical_principles": (
            "accessibility",
            "interoperability",
            "reusability",
        ),
    },
    covered_aspects={
        "publication_duty": (
            "mandatory publication",
            "relevant transparency information",
        ),
        "periodicity_update": ("periodic publication", "updated information"),
        "publication_quality": (
            "clear structured understandable publication",
            "easy access",
            "free access",
        ),
        "accessibility": ("accessibility", "identification and location mechanisms"),
        "reusability": ("reusable formats", "reusability"),
        "institutional_information": (
            "functions and applicable rules",
            "organisational structure and updated organigram",
        ),
        "planning_information": (
            "annual and multiannual plans",
            "objectives activities means and timing",
        ),
        "evaluation": (
            "periodic evaluation",
            "publication of compliance results and indicators",
        ),
        "processing_activities": ("processing activities inventory",),
        "legal_relevance_information": (
            "interpretative instructions or agreements",
            "draft normative texts",
            "regulatory preparation reports",
            "documents subject to public information",
        ),
        "economic_information": ("economic or budgetary management information",),
        "compliance_control": ("Council of Transparency and Good Governance control",),
        "enforcement": (),
        "transparency_portal": ("General State Administration portal",),
        "frequently_requested_information": (),
        "technical_principles": ("accessibility", "interoperability", "reusability"),
    },
)

CASES = (ACCESS_CASE, PUBLICITY_CASE)


def _fetch_canonical_text() -> str:
    request = Request(
        CANONICAL_LOCATOR,
        headers={"User-Agent": "Atanor candidate-study-content experiment"},
    )
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def _validate_evidence(
    sections: tuple[StudySection, ...], articles: dict[str, object]
) -> None:
    referenced = {article for section in sections for article in section.evidence_articles}
    missing = sorted(referenced - set(articles))
    if missing:
        raise RuntimeError(f"Study content references missing canonical articles: {missing}")


def _evaluate_semantic_coverage(case: KnowledgeNeedCase) -> tuple[CoverageResult, ...]:
    results: list[CoverageResult] = []
    for concept, required in case.required_aspects.items():
        covered = tuple(
            aspect for aspect in required if aspect in case.covered_aspects.get(concept, ())
        )
        missing = tuple(aspect for aspect in required if aspect not in covered)
        if not missing:
            status = "COVERED"
        elif covered:
            status = "PARTIAL"
        else:
            status = "MISSING"
        results.append(CoverageResult(concept, status, covered, missing))
    return tuple(results)


def _print_case(case: KnowledgeNeedCase, articles: dict[str, object]) -> tuple[CoverageResult, ...]:
    _validate_evidence(case.sections, articles)
    referenced = {article for section in case.sections for article in section.evidence_articles}
    uncovered_articles = [article for article in case.evidence_articles if article not in referenced]
    all_points = {point for section in case.sections for point in section.covered_points}
    semantic_results = _evaluate_semantic_coverage(case)

    print("\n" + "=" * 80)
    print(f"KNOWLEDGE NEED: {case.title}")
    print(f"  canonical evidence: articles {', '.join(case.evidence_articles)}")

    print("\nCANDIDATE-FACING STUDY CONTENT")
    print("  The artifact is a pedagogical synthesis, not the legal text.")
    for section in case.sections:
        print(f"\n{section.title}")
        print(f"  {section.content}")
        print(f"  evidence: articles {', '.join(section.evidence_articles)}")
        print(f"  covered concepts: {', '.join(section.covered_points)}")
        for point in section.exam_points:
            print(f"  exam point: {point}")

    print("\nARTICLE COVERAGE")
    print(f"  target articles: {', '.join(case.evidence_articles)}")
    print(f"  referenced articles: {', '.join(sorted(referenced))}")
    print(f"  uncovered articles: {', '.join(uncovered_articles) if uncovered_articles else 'none'}")
    print(f"  distinct covered concepts: {len(all_points)}")
    print("  article-reference coverage: " + ("COMPLETE" if not uncovered_articles else "PARTIAL"))

    print("\nSEMANTIC COVERAGE")
    for result in semantic_results:
        print(f"  {result.concept}: {result.status}")
        print(f"    covered: {', '.join(result.covered_aspects) if result.covered_aspects else 'none'}")
        print(f"    missing: {', '.join(result.missing_aspects) if result.missing_aspects else 'none'}")

    complete = sum(result.status == "COVERED" for result in semantic_results)
    partial = sum(result.status == "PARTIAL" for result in semantic_results)
    missing = sum(result.status == "MISSING" for result in semantic_results)
    print(f"  semantic concepts: {complete} covered, {partial} partial, {missing} missing")
    return semantic_results


def _print_comparison(results_by_case: dict[str, tuple[CoverageResult, ...]]) -> None:
    print("\n" + "=" * 80)
    print("REPEATABILITY COMPARISON")

    for title, results in results_by_case.items():
        complete = sum(result.status == "COVERED" for result in results)
        partial = sum(result.status == "PARTIAL" for result in results)
        missing = sum(result.status == "MISSING" for result in results)
        print(f"  {title}")
        print(f"    semantic concepts: {complete} covered, {partial} partial, {missing} missing")
        print("    aspect-based validation: APPLIED")

    print("\n  protocol: KnowledgeNeed -> canonical evidence -> study content -> required aspects -> semantic coverage")
    print("  repeated protocol: DEMONSTRATED")
    print("  semantic aspect matrix as reusable experimental mechanism: SUPPORTED")
    print("  semantic matching automation: NOT ESTABLISHED")
    print("  production model changes: NOT YET JUSTIFIED")


def run() -> None:
    articles = _extract_articles(_fetch_canonical_text())

    print("CANONICAL SOURCE")
    print(f"  {CANONICAL_SOURCE['title']}")
    print(f"  {CANONICAL_SOURCE['identifier']}")
    print(f"  {CANONICAL_LOCATOR}")
    print(f"  extracted article provisions: {len(articles)}")

    results_by_case = {
        case.title: _print_case(case, articles)
        for case in CASES
    }

    _print_comparison(results_by_case)

    print("\nTRACEABILITY")
    for case in CASES:
        for section in case.sections:
            print(
                f"  {case.title} / {section.title} -> articles {', '.join(section.evidence_articles)}"
                f" -> concepts {', '.join(section.covered_points)}"
            )

    print("\nEXPERIMENT FINDINGS")
    print("  article-level completeness: DEMONSTRATED FOR BOTH TARGET RANGES")
    print("  article reference as coverage criterion: INSUFFICIENT")
    print("  semantic aspect matrix: REPEATED SUCCESSFULLY ACROSS TWO KNOWLEDGE NEEDS")
    print("  semantic matching automation: NOT ESTABLISHED")
    print("  production model changes: NOT YET JUSTIFIED")
    print("  next architectural question: WHETHER THE ASPECT STRUCTURE CAN BE MINIMALLY GENERALIZED")


if __name__ == "__main__":
    run()
