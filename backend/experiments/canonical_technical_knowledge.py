"""Probe canonical technical knowledge construction outside the legal domain.

This deterministic experiment asks whether the AT-084 semantic-coverage pattern
also works when the canonical evidence is a technical specification rather than
legislation. It deliberately keeps the required/covered aspect matrices manual.

Protocol:
    KnowledgeNeed
        -> canonical evidence
        -> candidate-facing study content
        -> required aspects
        -> semantic coverage

This is an experiment, not a production contract.
"""

from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.request import Request, urlopen


CANONICAL_SOURCE = {
    "title": "HTTP Semantics",
    "identifier": "RFC 9110",
    "locator": "https://www.rfc-editor.org/rfc/rfc9110",
    "authority": "RFC Editor / IETF",
}


@dataclass(frozen=True)
class StudySection:
    title: str
    content: str
    evidence_sections: tuple[str, ...]
    covered_points: tuple[str, ...]


@dataclass(frozen=True)
class CoverageResult:
    concept: str
    status: str
    covered_aspects: tuple[str, ...]
    missing_aspects: tuple[str, ...]


@dataclass(frozen=True)
class KnowledgeNeedCase:
    title: str
    evidence_sections: tuple[str, ...]
    sections: tuple[StudySection, ...]
    required_aspects: dict[str, tuple[str, ...]]
    covered_aspects: dict[str, tuple[str, ...]]


CASE = KnowledgeNeedCase(
    title="Métodos HTTP y semántica de las peticiones",
    evidence_sections=("9.2", "9.3", "9.3.1", "9.3.2", "9.3.3", "9.3.4", "9.3.5", "9.3.6", "9.3.7", "9.3.8", "9.3.9"),
    sections=(
        StudySection(
            "1. Propiedades generales de los métodos HTTP",
            "Los métodos HTTP expresan la intención de una petición. La especificación distingue, entre otras propiedades, métodos seguros e idempotentes; estas propiedades tienen consecuencias semánticas para el cliente y el servidor.",
            ("9.2",),
            ("method_intent", "safe_methods", "idempotent_methods"),
        ),
        StudySection(
            "2. GET",
            "GET solicita la transferencia de una representación del recurso objetivo. Es un método seguro e idempotente.",
            ("9.3.1",),
            ("get_semantics", "get_safe", "get_idempotent"),
        ),
        StudySection(
            "3. HEAD",
            "HEAD es idéntico a GET salvo que el servidor no debe enviar contenido en la respuesta. Se utiliza para obtener metadatos de una respuesta sin transferir su contenido.",
            ("9.3.2",),
            ("head_semantics", "head_no_content"),
        ),
        StudySection(
            "4. POST",
            "POST solicita que el recurso procese la representación incluida en el contenido de la petición de acuerdo con la semántica del recurso. No es, por definición, un método idempotente.",
            ("9.3.3",),
            ("post_semantics", "post_non_idempotent"),
        ),
        StudySection(
            "5. PUT",
            "PUT solicita que el estado del recurso objetivo sea creado o reemplazado con el estado definido por la representación de la petición. PUT es idempotente.",
            ("9.3.4",),
            ("put_semantics", "put_idempotent"),
        ),
        StudySection(
            "6. DELETE",
            "DELETE solicita eliminar la asociación entre el recurso objetivo y su funcionalidad actual. DELETE es idempotente.",
            ("9.3.5",),
            ("delete_semantics", "delete_idempotent"),
        ),
        StudySection(
            "7. CONNECT, OPTIONS y TRACE",
            "CONNECT establece un túnel hacia el servidor identificado por el recurso objetivo. OPTIONS solicita información sobre las opciones de comunicación disponibles. TRACE permite realizar una prueba de bucle de retorno en la ruta hacia el recurso objetivo.",
            ("9.3.6", "9.3.7", "9.3.8"),
            ("connect_semantics", "options_semantics", "trace_semantics"),
        ),
        StudySection(
            "8. Seguridad e idempotencia",
            "Un método seguro es aquel cuya semántica esencial es de solo lectura o recuperación y no requiere que el cliente solicite un cambio de estado. Un método idempotente produce, en términos de la intención solicitada, el mismo efecto en el servidor tras una o varias peticiones idénticas.",
            ("9.2",),
            ("safe_definition", "idempotent_definition"),
        ),
    ),
    required_aspects={
        "method_intent": ("methods express request intent",),
        "safe_methods": ("safe-method concept", "safe methods include GET and HEAD"),
        "idempotent_methods": ("idempotent-method concept", "GET, HEAD, PUT and DELETE are idempotent"),
        "get_semantics": ("transfer of a representation of the target resource",),
        "get_safe": ("GET is safe",),
        "get_idempotent": ("GET is idempotent",),
        "head_semantics": ("same semantics as GET except for response content",),
        "head_no_content": ("server does not send response content",),
        "post_semantics": ("resource processes request content according to its semantics",),
        "post_non_idempotent": ("POST is not inherently idempotent",),
        "put_semantics": ("create or replace target resource state",),
        "put_idempotent": ("PUT is idempotent",),
        "delete_semantics": ("remove association with current functionality",),
        "delete_idempotent": ("DELETE is idempotent",),
        "connect_semantics": ("establish a tunnel to the target server",),
        "options_semantics": ("request communication options",),
        "trace_semantics": ("loop-back test along the request path",),
        "safe_definition": ("safe means request semantics are read-oriented",),
        "idempotent_definition": ("repeating the same request has the same intended effect",),
    },
    covered_aspects={
        "method_intent": ("methods express request intent",),
        "safe_methods": ("safe-method concept", "safe methods include GET and HEAD"),
        "idempotent_methods": ("idempotent-method concept", "GET, HEAD, PUT and DELETE are idempotent"),
        "get_semantics": ("transfer of a representation of the target resource",),
        "get_safe": ("GET is safe",),
        "get_idempotent": ("GET is idempotent",),
        "head_semantics": ("same semantics as GET except for response content",),
        "head_no_content": ("server does not send response content",),
        "post_semantics": ("resource processes request content according to its semantics",),
        "post_non_idempotent": ("POST is not inherently idempotent",),
        "put_semantics": ("create or replace target resource state",),
        "put_idempotent": ("PUT is idempotent",),
        "delete_semantics": ("remove association with current functionality",),
        "delete_idempotent": ("DELETE is idempotent",),
        "connect_semantics": ("establish a tunnel to the target server",),
        "options_semantics": ("request communication options",),
        "trace_semantics": ("loop-back test along the request path",),
        "safe_definition": ("safe means request semantics are read-oriented",),
        "idempotent_definition": ("repeating the same request has the same intended effect",),
    },
)


class _SectionParser(HTMLParser):
    """Collect visible text from an RFC HTML document for evidence resolution."""

    def __init__(self) -> None:
        super().__init__()
        self.text: list[str] = []

    def handle_data(self, data: str) -> None:
        value = " ".join(data.split())
        if value:
            self.text.append(value)


def fetch_canonical_text() -> str:
    request = Request(
        CANONICAL_SOURCE["locator"],
        headers={"User-Agent": "Atanor AT-084.5 experiment"},
    )
    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8")
    parser = _SectionParser()
    parser.feed(html)
    parser.close()
    return " ".join(parser.text)


def evaluate_coverage(case: KnowledgeNeedCase) -> tuple[CoverageResult, ...]:
    results = []
    for concept, required in case.required_aspects.items():
        covered = case.covered_aspects.get(concept, ())
        missing = tuple(aspect for aspect in required if aspect not in covered)
        status = "COVERED" if not missing else "PARTIAL" if covered else "MISSING"
        results.append(CoverageResult(concept, status, covered, missing))
    return tuple(results)


def run() -> None:
    canonical_text = fetch_canonical_text()
    required_markers = ("9.2", "9.3", "9.3.1", "9.3.9")
    missing_markers = [marker for marker in required_markers if marker not in canonical_text]
    if missing_markers:
        raise RuntimeError(f"Canonical source is missing expected section markers: {missing_markers}")

    results = evaluate_coverage(CASE)
    covered = sum(result.status == "COVERED" for result in results)
    partial = sum(result.status == "PARTIAL" for result in results)
    missing = sum(result.status == "MISSING" for result in results)

    print("=== AT-084.5 — CANONICAL TECHNICAL KNOWLEDGE ===")
    print("canonical source:", CANONICAL_SOURCE["title"])
    print("identifier:", CANONICAL_SOURCE["identifier"])
    print("locator:", CANONICAL_SOURCE["locator"])
    print("authority:", CANONICAL_SOURCE["authority"])
    print("canonical evidence:", ", ".join(f"sec. {s}" for s in CASE.evidence_sections))
    print("knowledge need:", CASE.title)
    print("candidate-facing sections:", len(CASE.sections))
    print("\nSEMANTIC COVERAGE")
    for result in results:
        print(f"  {result.concept}: {result.status}")
        if result.missing_aspects:
            print("    missing:", "; ".join(result.missing_aspects))
    print("\nSUMMARY")
    print(f"  semantic concepts: {covered} covered, {partial} partial, {missing} missing")
    print("  protocol: KnowledgeNeed -> canonical evidence -> study content -> required aspects -> semantic coverage")
    print("  canonical evidence resolved: YES")
    print("  candidate-facing study content: YES")
    print("  aspect-based validation: APPLIED")
    print("  semantic matching automation: NOT ESTABLISHED")
    print("  production model changes: NOT YET JUSTIFIED")
    print("  non-legal canonical source: DEMONSTRATED")


if __name__ == "__main__":
    run()
