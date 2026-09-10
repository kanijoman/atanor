"""Probe candidate-facing study content coverage against canonical evidence.

This is a deterministic product experiment, not a production contract. It
extends the first AT-084 probe by checking whether the candidate-facing
artifact covers the intended knowledge aspects, rather than merely citing the
articles that contain them.
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


CANONICAL_LOCATOR = CANONICAL_SOURCE["locator"]
TARGET_ARTICLES = tuple(str(number) for number in range(12, 25))

STUDY_SECTIONS = (
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
)


# This matrix is intentionally manual and experimental. It describes the aspects
# that must be checked before a concept can be considered fully covered. It is
# not a production domain model.
REQUIRED_ASPECTS: dict[str, tuple[str, ...]] = {
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
}

# Manual aspect matching for the current artifact. This makes the semantic
# validation explicit and inspectable without pretending that the experiment
# has solved semantic matching automatically.
COVERED_ASPECTS: dict[str, tuple[str, ...]] = {
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
    "inadmissibility": REQUIRED_ASPECTS["inadmissibility"],
    "processing": ("affected third parties", "legal referral to another body"),
    "resolution": (
        "notification",
        "one-month deadline",
        "possible one-month extension",
        "negative administrative silence",
    ),
    "information_units": ("support for access-request management",),
    "formalisation": REQUIRED_ASPECTS["formalisation"],
    "appeal": ("available legal appeals",),
    "claim": REQUIRED_ASPECTS["claim"],
}


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
    missing = sorted(referenced - set(articles), key=int)
    if missing:
        raise RuntimeError(f"Study content references missing canonical articles: {missing}")


def _evaluate_semantic_coverage() -> tuple[CoverageResult, ...]:
    results: list[CoverageResult] = []
    for concept, required in REQUIRED_ASPECTS.items():
        covered = tuple(
            aspect for aspect in required if aspect in COVERED_ASPECTS.get(concept, ())
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


def run() -> None:
    articles = _extract_articles(_fetch_canonical_text())
    _validate_evidence(STUDY_SECTIONS, articles)

    referenced = {article for section in STUDY_SECTIONS for article in section.evidence_articles}
    uncovered_articles = sorted(set(TARGET_ARTICLES) - referenced, key=int)
    all_points = {point for section in STUDY_SECTIONS for point in section.covered_points}
    semantic_results = _evaluate_semantic_coverage()

    print("CANONICAL SOURCE")
    print(f"  {CANONICAL_SOURCE['title']}")
    print(f"  {CANONICAL_SOURCE['identifier']}")
    print(f"  {CANONICAL_LOCATOR}")
    print(f"  extracted article provisions: {len(articles)}")

    print("\nKNOWLEDGE NEED")
    print("  Derecho de acceso a la información pública")
    print("  canonical evidence: articles 12–24")

    print("\nCANDIDATE-FACING STUDY CONTENT")
    print("  The artifact is a pedagogical synthesis, not the legal text.")
    for section in STUDY_SECTIONS:
        print(f"\n{section.title}")
        print(f"  {section.content}")
        print(f"  evidence: articles {', '.join(section.evidence_articles)}")
        print(f"  covered concepts: {', '.join(section.covered_points)}")
        for point in section.exam_points:
            print(f"  exam point: {point}")

    print("\nARTICLE COVERAGE")
    print(f"  target articles: {', '.join(TARGET_ARTICLES)}")
    print(f"  referenced articles: {', '.join(sorted(referenced, key=int))}")
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
    print("  semantic coverage: REQUIRES VALIDATION OF THE MANUAL ASPECT MATRIX")
    print("  pedagogical completeness: NOT ESTABLISHED")
    print("  legal correctness/completeness: REQUIRES VALIDATION")

    print("\nTRACEABILITY")
    for section in STUDY_SECTIONS:
        print(
            f"  {section.title} -> articles {', '.join(section.evidence_articles)}"
            f" -> concepts {', '.join(section.covered_points)}"
        )

    print("\nEXPERIMENT FINDINGS")
    print("  article-level completeness: DEMONSTRATED FOR TARGET RANGE")
    print("  article reference as coverage criterion: INSUFFICIENT")
    print("  semantic aspect matrix: USEFUL EXPERIMENTAL MECHANISM")
    print("  semantic matching automation: NOT ESTABLISHED")
    print("  production model changes: NOT YET JUSTIFIED")
    print("  next architectural question: WHETHER SEMANTIC COVERAGE REPEATS ACROSS KNOWLEDGE NEEDS")


if __name__ == "__main__":
    run()
