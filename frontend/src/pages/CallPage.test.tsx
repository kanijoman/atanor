import "@testing-library/jest-dom/vitest";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen, waitFor } from "@testing-library/react";

import { CallPage } from "./CallPage";

const call = { id: "call-1", title: "Convocatoria TIC 2026" };
const programmes = [
  { id: "programme-1", identifier: "I", title: "Programa oficial" },
  { id: "programme-2", identifier: "II", title: "Programa técnico" },
];

function mockCallResponses() {
  const fetchMock = vi.fn((url: string) => {
    if (url === "/api/calls/call-1") {
      return Promise.resolve(
        new Response(JSON.stringify(call), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      );
    }

    return Promise.resolve(
      new Response(JSON.stringify(programmes), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );
  });

  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

describe("CallPage", () => {
  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  it("shows the selected call and its programmes", async () => {
    mockCallResponses();

    render(<CallPage callId="call-1" />);

    expect(screen.getByText("Loading call…")).toBeVisible();
    expect(await screen.findByRole("heading", { name: call.title })).toBeVisible();
    expect(screen.getByRole("link", { name: /I — Programa oficial/ })).toBeVisible();
    expect(screen.getByRole("link", { name: /II — Programa técnico/ })).toBeVisible();
  });

  it("links programmes to the existing programme page", async () => {
    mockCallResponses();

    render(<CallPage callId="call-1" />);

    const link = await screen.findByRole("link", {
      name: /I — Programa oficial/,
    });

    expect(link).toHaveAttribute("href", "/programmes/programme-1");
  });

  it("requests call details and programmes", async () => {
    const fetchMock = mockCallResponses();

    render(<CallPage callId="call-1" />);
    await screen.findByRole("heading", { name: call.title });

    expect(fetchMock).toHaveBeenCalledWith("/api/calls/call-1");
    expect(fetchMock).toHaveBeenCalledWith("/api/calls/call-1/programmes");
  });

  it("shows an empty state when the call has no programmes", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((url: string) =>
        Promise.resolve(
          new Response(
            JSON.stringify(url.endsWith("/programmes") ? [] : call),
            {
              status: 200,
              headers: { "Content-Type": "application/json" },
            },
          ),
        ),
      ),
    );

    render(<CallPage callId="call-1" />);

    expect(
      await screen.findByText("No programmes are available for this call yet."),
    ).toBeVisible();
  });

  it("shows an error when either call request fails", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((url: string) =>
        Promise.resolve(
          new Response(url.endsWith("/programmes") ? "[]" : "Not found", {
            status: url.endsWith("/programmes") ? 200 : 404,
          }),
        ),
      ),
    );

    render(<CallPage callId="call-1" />);

    await waitFor(() => {
      expect(screen.getByText("Unable to load call.")).toBeVisible();
    });
  });
});
