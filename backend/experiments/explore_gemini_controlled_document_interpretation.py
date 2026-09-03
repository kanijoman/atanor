import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from pypdf import PdfReader


SAMPLES_DIR = Path("tests/samples")
TARGET_SAMPLE = "BOE-A-2024-14098.pdf"
MODEL = os.getenv("ATANOR_GEMINI_MODEL", "gemini-3.8-flash")
API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent"
)
MAX_OUTPUT_TOKENS = int(os.getenv("ATANOR_GEMINI_MAX_OUTPUT_TOKENS", "6000"))

# This experiment deliberately uses one known, bounded section of the BOE
# document. The anchors are only used to select the test slice; they are not
# sent as semantic instructions to Gemini.
START_ANCHOR = "CUERPO DE TÉCNICOS AUXILIARES DE INFORMÁTICA"
PROGRAM_ANCHOR = "Programa."
START_CONTEXT_UNITS = 45
END_CONTEXT_UNITS = 140


@dataclass(frozen=True)
class TextUnit:
    page: int
    order: int
    text: str


PROMPT = """
Analyse the supplied excerpt from an official Spanish public-administration
examination document.

This is a controlled experiment. The excerpt was selected from a larger
convocatoria, but you are NOT told which lines are headings, requirements, or
programme content. Infer their meaning from the supplied text.

Identify only the following:

1. the distinct selection process or processes described in the excerpt;
2. the eligibility requirements that apply to those processes;
3. the study programme/syllabus associated with those processes;
4. the relationships between each process, its requirements, and its programme.

Return ONLY valid JSON with this structure:
{
  "selection_processes": [
    {
      "id": "process-1",
      "title": "...",
      "evidence": [{"page": 1, "unit_start": 10, "unit_end": 12}]
    }
  ],
  "requirements": [
    {
      "id": "requirement-1",
      "text": "...",
      "evidence": [{"page": 2, "unit_start": 20, "unit_end": 21}]
    }
  ],
  "programmes": [
    {
      "id": "programme-1",
      "title": "...",
      "evidence": [{"page": 5, "unit_start": 40, "unit_end": 60}]
    }
  ],
  "relationships": [
    {
      "selection_process_id": "process-1",
      "requirement_ids": ["requirement-1"],
      "programme_id": "programme-1"
    }
  ]
}

Rules:
- Do not assume fixed meanings for annexes, numbering, headings, or wording.
- Do not treat an occurrence of the word "programa" as sufficient evidence of
  a study programme.
- Distinguish requirements from explanatory or procedural statements.
- Preserve the meaning of requirements; do not strengthen or weaken them.
- Use concise titles, but do not invent facts that are absent from the excerpt.
- Evidence must refer to the supplied page and global unit numbers.
- If something is genuinely uncertain, omit it rather than guessing.
""".strip()


def extract_units(pdf_path: Path) -> list[TextUnit]:
    reader = PdfReader(pdf_path)
    units: list[TextUnit] = []
    order = 0

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for line in text.splitlines():
            value = " ".join(line.split())
            if not value:
                continue
            order += 1
            units.append(TextUnit(page_number, order, value))

    return units


def find_anchor(units: list[TextUnit], anchor: str) -> int:
    normalized_anchor = " ".join(anchor.casefold().split())
    for index, unit in enumerate(units):
        if normalized_anchor in unit.text.casefold():
            return index
    raise RuntimeError(f"Anchor not found in extracted document: {anchor!r}")


def select_controlled_slice(units: list[TextUnit]) -> list[TextUnit]:
    start_index = find_anchor(units, START_ANCHOR)
    program_index = find_anchor(units[start_index:], PROGRAM_ANCHOR) + start_index

    # Include the process context before the process anchor and enough text
    # after the programme marker to contain meaningful programme content.
    slice_start = max(0, start_index - START_CONTEXT_UNITS)
    slice_end = min(len(units), program_index + END_CONTEXT_UNITS)
    return units[slice_start:slice_end]


def format_document(units: list[TextUnit]) -> str:
    return "\n".join(
        f"[p{unit.page} u{unit.order}] {unit.text}" for unit in units
    )


def call_gemini(document: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    payload = {
        "system_instruction": {"parts": [{"text": PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": document}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "maxOutputTokens": MAX_OUTPUT_TOKENS,
        },
    }
    request = Request(
        API_URL.format(model=MODEL),
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "x-goog-api-key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=180) as response:
            body = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Gemini request failed ({error.code}): {detail}"
        ) from error
    except URLError as error:
        raise RuntimeError(f"Gemini request failed: {error.reason}") from error

    try:
        output_text = body["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError("Gemini response did not contain generated text") from error

    try:
        return json.loads(output_text)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Gemini output was not valid JSON: {output_text[:1000]}"
        ) from error


def summarize(pdf_path: Path) -> None:
    units = extract_units(pdf_path)
    print("GEMINI CONTROLLED DOCUMENT INTERPRETATION")
    print(f"  sample: {pdf_path.name}")
    print(f"  total units: {len(units):,}")

    selected = select_controlled_slice(units)
    first = selected[0]
    last = selected[-1]
    print(f"  selected units: {len(selected):,}")
    print(f"  selected range: u{first.order}-u{last.order}")
    print(f"  selected pages: p{first.page}-p{last.page}")
    print(f"  selected characters: {len(format_document(selected)):,}")
    print(f"  model: {MODEL}")
    print("  status: querying Gemini")

    result = call_gemini(format_document(selected))
    print()
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main() -> None:
    pdf_path = SAMPLES_DIR / TARGET_SAMPLE
    if not pdf_path.exists():
        raise FileNotFoundError(f"Sample not found: {pdf_path}")

    try:
        summarize(pdf_path)
    except RuntimeError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
