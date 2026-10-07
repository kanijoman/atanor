import { type FormEvent, useState } from "react";

import { ApiError, uploadCall } from "../api";

type UploadState =
  { status: "idle" } | { status: "uploading" } | { status: "error"; message: string };

const FALLBACK_ERROR = "The convocatoria could not be imported. Please try again.";

function errorMessage(error: unknown): string {
  return error instanceof ApiError && error.detail ? error.detail : FALLBACK_ERROR;
}

export function UploadCallForm() {
  const [file, setFile] = useState<File | null>(null);
  const [state, setState] = useState<UploadState>({ status: "idle" });

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!file) {
      return;
    }

    setState({ status: "uploading" });
    try {
      const call = await uploadCall(file);
      window.location.assign(`/calls/${call.id}`);
    } catch (error) {
      setState({ status: "error", message: errorMessage(error) });
    }
  }

  return (
    <form onSubmit={handleSubmit} aria-labelledby="import-call-heading">
      <h2 id="import-call-heading">Import a convocatoria</h2>
      <label>
        Convocatoria PDF
        <input
          type="file"
          accept="application/pdf,.pdf"
          onChange={(event) => setFile(event.target.files?.[0] ?? null)}
        />
      </label>
      <button type="submit" disabled={!file || state.status === "uploading"}>
        {state.status === "uploading" ? "Importing…" : "Import convocatoria"}
      </button>
      {state.status === "error" && <p role="alert">{state.message}</p>}
    </form>
  );
}
