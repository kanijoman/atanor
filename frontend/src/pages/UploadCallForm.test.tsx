import "@testing-library/jest-dom/vitest";
import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { UploadCallForm } from "./UploadCallForm";

const pdf = new File(["%PDF-1.4"], "convocatoria.pdf", { type: "application/pdf" });

function respond(status: number, body: unknown) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

async function importPdf() {
  await userEvent.upload(screen.getByLabelText("Convocatoria PDF"), pdf);
  await userEvent.click(screen.getByRole("button", { name: "Import convocatoria" }));
}

describe("UploadCallForm", () => {
  const assign = vi.fn();

  beforeEach(() => {
    vi.stubGlobal("location", { assign });
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
    assign.mockReset();
  });

  it("cannot be submitted before a file is chosen", () => {
    render(<UploadCallForm />);

    expect(screen.getByRole("button", { name: "Import convocatoria" })).toBeDisabled();
  });

  it("uploads the chosen PDF and opens the imported call", async () => {
    const fetchMock = vi.fn().mockResolvedValue(respond(201, { id: "call-9", title: "x" }));
    vi.stubGlobal("fetch", fetchMock);
    render(<UploadCallForm />);

    await importPdf();

    await waitFor(() => expect(assign).toHaveBeenCalledWith("/calls/call-9"));
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/calls?filename=convocatoria.pdf",
      expect.objectContaining({ method: "POST", body: pdf }),
    );
  });

  it("shows why the API refused the document", async () => {
    const detail = "We could not find a convocatoria with a study programme in this PDF.";
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(respond(422, { detail })));
    render(<UploadCallForm />);

    await importPdf();

    expect(await screen.findByRole("alert")).toHaveTextContent(detail);
    expect(assign).not.toHaveBeenCalled();
  });

  it("shows a generic message when the API cannot be reached", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("network down")));
    render(<UploadCallForm />);

    await importPdf();

    expect(await screen.findByRole("alert")).toHaveTextContent("could not be imported");
  });
});
