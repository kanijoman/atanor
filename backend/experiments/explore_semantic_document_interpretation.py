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
API_URL = os.getenv("ATANOR_LLM_API_URL", "https://api.openai.com/v1/responses")
MODEL = os.getenv("ATANOR_LLM_MODEL", "gpt-5.6-luna")
MAX_OUTPUT_TOKENS = int(os.getenv("ATANOR_LLM_MAX_OUTPUT_TOKENS", "12000"))


@dataclass(frozen=True)
class TextUnit:
    page: int
    order: int
    text: str


SYSTEM_PROMPT = """
You are analysing an official public-administration examination convocatoria.

Interpret the document semantically. Do not rely on specific words, numbering
conventions, annex names, or formatting conventions as rules. Identify concepts
by their meaning and relationships.

Find, when present:
1. selection processes: distinct processes a candidate could apply to;
2. eligibility requirements: conditions a candidate must satisfy;
3. study programmes/syllabi: content that candidates are expected to study;
4. relationships between each selection process, its requirements, and its
   programme.

Return only valid JSON with this shape:
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

Use concise normalized titles, preserve the meaning of requirements, and avoid
inventing information. If a relationship is uncertain, omit it rather than
creating a guess. Evidence must point to the supplied document units.
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


def format_document(units: list[TextUnit]) -> str:
    return "\n".join(
        f"[p{unit.page} u{unit.order}] {unit.text}" for unit in units
    )


def call_model(document: str) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    payload = {
        "model": MODEL,
        "instructions": SYSTEM_PROMPT,
        "input": document,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
    }
    request = Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=300) as response:
            body = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"LLM request failed ({error.code}): {detail}") from error
    except URLError as error:
        raise RuntimeError(f"LLM request failed: {error.reason}") from error

    output_text = body.get("output_text")
    if not output_text:
        raise RuntimeError("LLM response did not contain output_text")

    try:
        return json.loads(output_text)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"LLM output was not valid JSON: {output_text[:1000]}") from error


def summarize(pdf_path: Path) -> None:
    units = extract_units(pdf_path)
    print("SEMANTIC DOCUMENT INTERPRETATION")
    print(f"  sample: {pdf_path.name}")
    print(f"  units: {len(units):,}")

    if not units:
        print("  status: no_extractable_text")
        return

    document = format_document(units)
    print(f"  document characters: {len(document):,}")
    print(f"  model: {MODEL}")
    print("  status: querying semantic model")

    result = call_model(document)
    print()
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main() -> None:
    samples = sorted(SAMPLES_DIR.glob("*.pdf"))
    if not samples:
        raise FileNotFoundError(f"No PDF samples found in: {SAMPLES_DIR}")

    target = [sample for sample in samples if sample.name == TARGET_SAMPLE]
    selected = target or samples[:1]

    try:
        for sample in selected:
            summarize(sample)
    except RuntimeError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
