"""Validate semantic coverage repeatability on a different canonical legal source.

This is a deterministic product experiment, not a production contract. It repeats
the AT-084 semantic-coverage protocol on Ley 39/2015, independently from the
Ley 19/2013 experiment:

    KnowledgeNeed
        -> canonical evidence
        -> candidate-facing study content
        -> required aspects
        -> semantic coverage

The required and covered aspect matrices are deliberately manual. The experiment
asks whether the validation pattern remains useful across canonical sources; it
does not attempt to automate semantic matching or introduce production models.
"""

from dataclasses import dataclass
from html.parser import HTMLParser
import re
from urllib.request import Request, urlopen


CANONICAL_SOURCE = {
    "title": "Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las Administraciones Públicas",
    "identifier": "BOE-A-2015-10565",
    "locator": "https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565",
    "authority": "Boletín Oficial del Estado",
}


@dataclass(frozen=True)
class StudySection:
    title: str
    content: str
    evidence_articles: tuple[str, ...]
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
    evidence_articles: tuple[str, ...]
    sections: tuple[StudySection, ...]
    required_aspects: dict[str, tuple[str, ...]]
    covered_aspects: dict[str, tuple[str, ...]]


CASE = KnowledgeNeedCase(
    title="Derecho y obligación de relacionarse electrónicamente con las Administraciones Públicas",
    evidence_articles=("13", "14"),
    sections=(
        StudySection(
            "1. Derechos generales de las personas",
            "Las personas con capacidad de obrar ante las Administraciones Públicas tienen los derechos reconocidos por la Ley en sus relaciones con ellas, entre ellos comunicarse mediante el Punto de Acceso General electrónico y ser asistidas en el uso de medios electrónicos.",
            ("13",),
            ("general_rights", "electronic_access_point", "electronic_assistance"),
        ),
        StudySection(
            "2. Elección del medio por las personas físicas",
            "Las personas físicas pueden elegir en todo momento si se relacionan electrónicamente o por medios no electrónicos, salvo cuando estén obligadas a utilizar medios electrónicos. La elección puede modificarse en cualquier momento.",
            ("14",),
            ("natural_person_choice", "choice_change"),
        ),
        StudySection(
            "3. Quiénes están obligados a relacionarse electrónicamente",
            "Están obligados, entre otros, las personas jurídicas, las entidades sin personalidad jurídica, quienes ejerzan una actividad profesional para la que se requiera colegiación obligatoria en el ejercicio de dicha actividad, quienes representen a un interesado que esté obligado y los empleados públicos para los trámites y actuaciones que realicen por razón de su condición.",
            ("14",),
            ("mandatory_categories",),
        ),
        StudySection(
            "4. Ampliación reglamentaria de la obligación",
            "Reglamentariamente puede establecerse la obligación de relacionarse electrónicamente para determinados procedimientos y para determinados colectivos de personas físicas que, por su capacidad económica, técnica, dedicación profesional u otras razones, quede acreditado que tienen acceso y disponibilidad de los medios electrónicos necesarios.",
            ("14",),
            ("regulatory_extension", "objective_criteria"),
        ),
    ),
    required_aspects={
        "general_rights": (
            "rights in relations with public administrations",
            "rights apply to persons with legal capacity to act",
        ),
        "electronic_access_point": (
            "right to communicate through the General Electronic Access Point",
        ),
        "electronic_assistance": (
            "right to assistance in the use of electronic means",
        ),
        "natural_person_choice": (
            "natural persons may choose electronic or non-electronic communication",
            "choice is subject to statutory exceptions",
        ),
        "choice_change": (
            "choice may be changed at any time",
        ),
        "mandatory_categories": (
            "legal persons",
            "entities without legal personality",
            "mandatory-collegiation professionals acting professionally",
            "representatives of obliged persons",
            "public employees acting in that capacity",
        ),
        "regulatory_extension": (
            "regulations may extend electronic-obligation categories",
            "extension may target specific procedures",
            "extension may target specified groups of natural persons",
        ),
        "objective_criteria": (
            "economic capacity",
            "technical capacity",
            "professional dedication",
            "other demonstrated access and availability of necessary electronic means",
        ),
    },
    covered_aspects={
        "general_rights": (
            "rights in relations with public administrations",
            "rights apply to persons with legal capacity to act",
        ),
        "electronic_access_point": (
            "right to communicate through the General Electronic Access Point",
        ),
        "electronic_assistance": (
            "right to assistance in the use of electronic means",
        ),
        "natural_person_choice": (
            "natural persons may choose electronic or non-electronic communication",
        ),
        "choice_change": (
            "choice may be changed at any time",
        ),
        "mandatory_categories": (
            "legal persons",
            "entities without legal personality",
            "mandatory-collegiation professionals acting professionally",
            "representatives of obliged persons",
            "public employees acting in that capacity",
        ),
        "regulatory_extension": (
            "regulations may extend electronic-obligation categories",
            "extension may target specific procedures",
        ),
        "objective_criteria": (
            "economic capacity",
            "technical capacity",
            "professional dedication",
        ),
    },
)


class _ArticleParser(HTMLParser):
    """Extract article headings and their following paragraphs from BOE HTML."""

    _ARTICLE_PATTERN = re.compile(r"Artículo\s+([0-9]+(?:\s+bis)?)\.\s*(.*)", re.I)

    def __init__(self) -> None:
        super().__init__()
        self.articles: dict[str, str] = {}
        self._number: str | None = None
        self._title: str | None = None
        self._text: list[str] = []
        self._heading = False
        self._body = False

    def handle_starttag(self, tag: str, attrs) -> None:
        attributes = dict(attrs)
        element_id = attributes.get("id", "")
        if element_id.startswith("a") and element_id[1:].isdigit():
            self._finish()
        if tag in {"h4", "h5"}:
            self._heading = True
        elif self._number is not None and tag in {"p", "li"}:
            self._body = True

    def handle_endtag(self, tag: str) -> None:
        if tag in {"h4", "h5"}:
            self._heading = False
        elif tag in {"p", "li"}:
            self._body = False

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if not text:
            return
        if self._heading:
            match = self._ARTICLE_PATTERN.match(text)
            if match:
                self._finish()
                self._number = match.group(1)
                self._title = match.group(2)
                return
        if self._number is not None and self._body:
            self._text.append(text)

    def _finish(self) -> None:
        if self._number is not None:
            self.articles[self._number] = " ".join(self._text)
        self._number = None
        self._title = None
        self._text = []

    def close(self) -> None:
        super().close()
        self._finish()


def fetch_canonical_articles() -> dict[str, str]:
    request = Request(
        CANONICAL_SOURCE["locator"],
        headers={"User-Agent": "Atanor AT-084.4 experiment"},
    )
    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8")
    parser = _ArticleParser()
    parser.feed(html)
    parser.close()
    return parser.articles


def evaluate_coverage(case: KnowledgeNeedCase) -> tuple[CoverageResult, ...]:
    results = []
    for concept, required in case.required_aspects.items():
        covered = case.covered_aspects.get(concept, ())
        missing = tuple(aspect for aspect in required if aspect not in covered)
        status = "COVERED" if not missing else "PARTIAL" if covered else "MISSING"
        results.append(CoverageResult(concept, status, covered, missing))
    return tuple(results)


def run() -> None:
    articles = fetch_canonical_articles()
    missing_articles = [number for number in CASE.evidence_articles if number not in articles]
    if missing_articles:
        raise RuntimeError(f"Canonical source is missing articles: {missing_articles}")

    results = evaluate_coverage(CASE)
    covered = sum(result.status == "COVERED" for result in results)
    partial = sum(result.status == "PARTIAL" for result in results)
    missing = sum(result.status == "MISSING" for result in results)

    print("=== AT-084.4 — CROSS-SOURCE SEMANTIC COVERAGE ===")
    print("canonical source:", CANONICAL_SOURCE["title"])
    print("identifier:", CANONICAL_SOURCE["identifier"])
    print("locator:", CANONICAL_SOURCE["locator"])
    print("canonical evidence:", ", ".join(f"art. {n}" for n in CASE.evidence_articles))
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
    print("  cross-source repetition: DEMONSTRATED")


if __name__ == "__main__":
    run()
