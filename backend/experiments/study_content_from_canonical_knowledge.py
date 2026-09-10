"""Probe candidate-facing study content from canonical legal evidence.

This is a deterministic product experiment, not a production contract. It takes
one real legal KnowledgeNeed and turns selected canonical provisions into a
candidate-readable study artifact while keeping evidence links explicit.

The content is intentionally authored in the experiment. The goal is to learn
what a useful study artifact needs to contain before choosing an implementation
strategy or extending the production domain model.
"""

from dataclasses import dataclass
from pathlib import Path
from urllib.request import Request, urlopen

from app.experiments.canonical_knowledge_construction import (
    _extract_articles,
    CANONICAL_SOURCE,
)


@dataclass(frozen=True)
class StudySection:
    title: str
    content: str
    evidence_articles: tuple[str, ...]
    exam_points: tuple[str, ...] = ()


CANONICAL_LOCATOR = CANONICAL_SOURCE["locator"]

# The structure and wording are deliberately authored for this experiment.
# They represent a candidate-facing synthesis, not a claim that the law itself
# uses this pedagogical structure.
STUDY_SECTIONS = (
    StudySection(
        title="1. Qué es el derecho de acceso",
        content=(
            "La Ley reconoce a todas las personas el derecho a acceder a la "
            "información pública, en los términos establecidos por la propia Ley. "
            "El régimen estatal se entiende además junto con la normativa "
            "autonómica que resulte aplicable."
        ),
        evidence_articles=("12",),
        exam_points=("Titularidad: todas las personas.",),
    ),
    StudySection(
        title="2. Qué se considera información pública",
        content=(
            "Es información pública la contenida en documentos o contenidos, "
            "cualquiera que sea su formato o soporte, que esté en poder de los "
            "sujetos incluidos en el ámbito de aplicación y que haya sido elaborada "
            "o adquirida en el ejercicio de sus funciones."
        ),
        evidence_articles=("13",),
        exam_points=("Formato o soporte: irrelevante para la definición.",),
    ),
    StudySection(
        title="3. Límites del derecho",
        content=(
            "El acceso puede limitarse cuando perjudique alguno de los intereses "
            "protegidos por la Ley, entre ellos la seguridad nacional, la defensa, "
            "las relaciones exteriores, la seguridad pública, la prevención e "
            "investigación de ilícitos, la tutela judicial efectiva, los intereses "
            "económicos y comerciales o la protección del medio ambiente. La "
            "aplicación del límite debe estar justificada y ser proporcionada, "
            "atendiendo a las circunstancias del caso concreto."
        ),
        evidence_articles=("14",),
        exam_points=(
            "Los límites no operan de forma abstracta: su aplicación debe justificarse y ser proporcionada.",
        ),
    ),
    StudySection(
        title="4. Protección de datos y acceso parcial",
        content=(
            "Cuando la información solicitada contenga datos personales, el régimen "
            "de acceso debe coordinarse con la protección de esos datos. Cuando una "
            "parte de la información quede afectada por un límite, la Ley contempla "
            "el acceso parcial cuando sea posible separar la información protegida "
            "sin alterar el sentido de la información restante."
        ),
        evidence_articles=("15", "16"),
        exam_points=(
            "Distinguir protección de datos de los restantes límites del artículo 14.",
            "Recordar la figura del acceso parcial.",
        ),
    ),
    StudySection(
        title="5. Cómo se ejerce el derecho",
        content=(
            "La solicitud debe permitir identificar al solicitante y la información "
            "que pide, además de proporcionar un medio de contacto y, en su caso, "
            "indicar la modalidad preferida de acceso. El solicitante no está "
            "obligado a motivar la solicitud. Si la solicitud no identifica "
            "suficientemente la información, puede pedirse su concreción."
        ),
        evidence_articles=("17", "19"),
        exam_points=(
            "La ausencia de motivación no es por sí sola causa de rechazo.",
            "La solicitud debe contener los elementos exigidos por el artículo 17.",
        ),
    ),
    StudySection(
        title="6. Cuándo puede inadmitirse una solicitud",
        content=(
            "La Ley establece causas tasadas de inadmisión, entre ellas que la "
            "información esté en curso de elaboración o publicación general, que "
            "tenga carácter auxiliar o de apoyo, que requiera una acción previa de "
            "reelaboración, que se dirija a un órgano que no la posea cuando se "
            "desconozca el competente, o que la solicitud sea manifiestamente "
            "repetitiva o abusiva sin justificación vinculada a la finalidad de la Ley."
        ),
        evidence_articles=("18",),
        exam_points=("Las causas de inadmisión deben distinguirse de los límites del artículo 14.",),
    ),
    StudySection(
        title="7. Tramitación y resolución",
        content=(
            "Durante la tramitación pueden intervenir terceros afectados y pueden "
            "producirse remisiones al órgano que haya elaborado o generado la "
            "información. La resolución que conceda o deniegue el acceso debe "
            "notificarse, con carácter general, en el plazo máximo de un mes desde "
            "la recepción de la solicitud por el órgano competente, ampliable por "
            "otro mes en determinados supuestos de volumen o complejidad. El "
            "silencio ante el transcurso del plazo máximo tiene el efecto previsto "
            "por la Ley."
        ),
        evidence_articles=("19", "20"),
        exam_points=(
            "Plazo general de resolución: un mes.",
            "Puede existir ampliación por otro mes en los supuestos legales.",
        ),
    ),
    StudySection(
        title="8. Formalización del acceso",
        content=(
            "El acceso se realiza preferentemente por vía electrónica, salvo que no "
            "sea posible o el solicitante haya señalado expresamente otro medio. "
            "Como regla general el acceso es gratuito, aunque la expedición de "
            "copias o la transformación a otro formato puede estar sujeta a las "
            "exacciones previstas legalmente."
        ),
        evidence_articles=("22",),
        exam_points=(
            "Preferencia por el medio electrónico.",
            "Acceso gratuito como regla general.",
        ),
    ),
    StudySection(
        title="9. Impugnación y reclamación",
        content=(
            "Las resoluciones en materia de acceso pueden ser objeto de control. "
            "La Ley establece una reclamación potestativa ante el Consejo de "
            "Transparencia y Buen Gobierno, con carácter previo a la impugnación "
            "en vía contencioso-administrativa, en los términos previstos en el "
            "artículo 24 y en la normativa aplicable."
        ),
        evidence_articles=("23", "24"),
        exam_points=(
            "La reclamación del artículo 24 es potestativa y previa a la vía contencioso-administrativa.",
        ),
    ),
)


def _fetch_canonical_text() -> str:
    request = Request(
        CANONICAL_LOCATOR,
        headers={"User-Agent": "Atanor candidate-study-content experiment"},
    )
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def _validate_evidence(sections: tuple[StudySection, ...], articles: dict[str, object]) -> None:
    referenced = {article for section in sections for article in section.evidence_articles}
    missing = sorted(referenced - set(articles))
    if missing:
        raise RuntimeError(f"Study content references missing canonical articles: {missing}")


def _print_section(index: int, section: StudySection) -> None:
    print(f"\n{section.title}")
    print(f"  {section.content}")
    print(f"  evidence: articles {', '.join(section.evidence_articles)}")
    if section.exam_points:
        print("  exam points:")
        for point in section.exam_points:
            print(f"    - {point}")


def run() -> None:
    """Run the candidate-facing study-content experiment."""
    articles = _extract_articles(_fetch_canonical_text())
    _validate_evidence(STUDY_SECTIONS, articles)

    print("CANONICAL SOURCE")
    print(f"  {CANONICAL_SOURCE['title']}")
    print(f"  {CANONICAL_SOURCE['identifier']}")
    print(f"  {CANONICAL_LOCATOR}")
    print(f"  extracted article provisions: {len(articles)}")

    print("\nKNOWLEDGE NEED")
    print("  Derecho de acceso a la información pública")
    print("  canonical evidence: articles 12–24")

    print("\nCANDIDATE-FACING STUDY CONTENT")
    print("  This artifact is a pedagogical synthesis, not the legal text.")
    for index, section in enumerate(STUDY_SECTIONS, start=1):
        _print_section(index, section)

    referenced = tuple(
        article for section in STUDY_SECTIONS for article in section.evidence_articles
    )
    covered_articles = set(referenced)
    expected_articles = {str(number) for number in range(12, 25)}

    print("\nTRACEABILITY")
    for section in STUDY_SECTIONS:
        print(
            f"  {section.title} -> "
            f"{', '.join(CANONICAL_LOCATOR + '#a' + article for article in section.evidence_articles)}"
        )

    print("\nEXPERIMENT FINDINGS")
    print("  candidate-facing structure: WORKS AS A PRODUCT PROBE")
    print("  canonical evidence validation: WORKS FOR REFERENCED PROVISIONS")
    print("  knowledge vs study-content distinction: NECESSARY")
    print("  evidence traceability: NECESSARY AND FEASIBLE IN EXPERIMENT")
    print(
        "  article coverage of target range: "
        + ("COMPLETE" if covered_articles == expected_articles else "PARTIAL")
    )
    print("  pedagogical completeness: NOT ESTABLISHED")
    print("  legal correctness/completeness: REQUIRES VALIDATION")
    print("  production model changes: NOT YET JUSTIFIED")
    print("  generation strategy: INTENTIONALLY UNDECIDED")


if __name__ == "__main__":
    run()
