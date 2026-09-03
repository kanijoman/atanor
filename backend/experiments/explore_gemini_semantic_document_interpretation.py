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
MAX_OUTPUT_TOKENS = int(os.getenv("ATANOR_GEMINI_MAX_OUTPUT_TOKENS", "16000"))


@dataclass(frozen=True)
class TextUnit:
    page: int
    order: int
    text: str


PROMPT = """
Analyse the supplied official public-administration examination document.

Interpret it semantically. Do not assume that headings, annexes, numbering,
terminology, or document layout follow a fixed convention. Infer the meaning
from the document itself.

Identify, when present:

1. selection processes: distinct processes that a candidate could apply to;
2. eligibility requirements: conditions a candidate must satisfy to participate;
3. study programmes/syllabi: content candidates are expected to study;
4. relationships connecting each selection process with its applicable
   requirements and programme.

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
- Discover the relevant concepts without being given their location.
- Do not use lexical occurrences of words such as "programa" as proof that a
  section is a study programme.
- Distinguish generic statements from requirements that apply to a process.
- Preserve the meaning of requirements; do not rewrite them into stronger or
  weaker conditions.
- Use concise titles, but do not invent facts.
- Evidence must refer to the supplied units using their page and global unit
  numbers.
- If a relationship is uncertain, omit it instead of guessing.
- Prefer complete coverage of distinct processes over exhaustive extraction of
  every minor detail.
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


def call_gemini(document: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    payload = {
        "system_instruction": {"parts": [{"text": PROMPT}]},
        "contents": [
            {"role": "user", "parts": [{"text": document}]}
        ],
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
        with urlopen(request, timeout=300) as response:
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
    print("GEMINI SEMANTIC DOCUMENT INTERPRETATION")
    print(f"  sample: {pdf_path.name}")
    print(f"  units: {len(units):,}")

    if not units:
        print("  status: no_extractable_text")
        return

    document = format_document(units)
    print(f"  document characters: {len(document):,}")
    print(f"  model: {MODEL}")
    print("  status: querying Gemini")

    result = call_gemini(document)
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
