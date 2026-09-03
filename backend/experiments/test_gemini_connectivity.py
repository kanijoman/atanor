import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


MODEL = os.getenv("ATANOR_GEMINI_MODEL", "gemini-3.8-flash")
API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent"
)


def call_gemini() -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": "Reply with exactly: OK"}],
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 16,
        },
    }
    request = Request(
        API_URL.format(model=MODEL),
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "x-goog-api-key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=30) as response:
            body = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Gemini request failed ({error.code}): {detail}"
        ) from error
    except URLError as error:
        raise RuntimeError(f"Gemini request failed: {error.reason}") from error
    except TimeoutError as error:
        raise RuntimeError("Gemini request timed out after 30 seconds") from error

    try:
        return body["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError("Gemini response did not contain generated text") from error


def main() -> None:
    print("GEMINI CONNECTIVITY TEST")
    print(f"  model: {MODEL}")
    print("  prompt: Reply with exactly: OK")
    print("  timeout: 30 seconds")
    print("  status: querying Gemini")

    try:
        result = call_gemini()
    except RuntimeError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1) from error

    print(f"  response: {result!r}")
    print("  status: success")


if __name__ == "__main__":
    main()
