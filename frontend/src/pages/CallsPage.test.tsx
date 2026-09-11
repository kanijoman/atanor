import "@testing-library/jest-dom/vitest";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen, waitFor } from "@testing-library/react";

import { CallsPage } from "./CallsPage";

const calls = [
  { id: "call-1", title: "Convocatoria TIC 2026" },
  { id: "call-2", title: "Convocatoria Archivos 2026" },
];

describe("CallsPage", () => {
  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  it("shows available calls returned by the API", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify(calls), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );

    render(<CallsPage />);

    expect(screen.getByRole("heading", { name: "Calls" })).toBeVisible();
    expect(screen.getByText("Loading calls…")).toBeVisible();
    expect(await screen.findByRole("link", { name: calls[0].title })).toBeVisible();
    expect(screen.getByRole("link", { name: calls[1].title })).toBeVisible();
  });

  it("links each call to its detail page", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify([calls[0]]), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );

    render(<CallsPage />);

    const link = await screen.findByRole("link", { name: calls[0].title });
    expect(link).toHaveAttribute("href", "/calls/call-1");
  });

  it("shows an empty state when no calls are available", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response("[]", {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );

    render(<CallsPage />);

    expect(await screen.findByText("No calls are available yet.")).toBeVisible();
  });

  it("shows an error when calls cannot be loaded", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("Network error")));

    render(<CallsPage />);

    await waitFor(() => {
      expect(screen.getByText("Unable to load calls.")).toBeVisible();
    });
  });

  it("requests calls from the calls API", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify([calls[0]]), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<CallsPage />);

    await screen.findByRole("link", { name: calls[0].title });
    expect(fetchMock).toHaveBeenCalledWith("/api/calls");
  });
});
