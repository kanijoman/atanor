import "@testing-library/jest-dom/vitest";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen, waitFor } from "@testing-library/react";

import { ProgrammePage } from "./ProgrammePage";

const programme = {
  id: "programme-1",
  identifier: "I",
  title: "Programa oficial",
  units: [
    {
      id: "unit-1",
      number: 1,
      title: "Organización del Estado",
    },
    {
      id: "unit-2",
      number: 2,
      title: "Derecho de acceso a la información pública",
    },
  ],
};

describe("ProgrammePage", () => {
  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  it("shows the programme and its units returned by the API", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify(programme), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );

    render(<ProgrammePage programmeId="programme-1" />);

    expect(screen.getByRole("heading", { name: "Programme I" })).toBeVisible();
    expect(screen.getByText("Loading programme…")).toBeVisible();

    expect(
      await screen.findByRole("link", {
        name: /Derecho de acceso a la información pública/,
      }),
    ).toBeVisible();
    expect(screen.getByText("Organización del Estado")).toBeVisible();
  });

  it("offers a selectable link for each programme unit", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify(programme), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );

    render(<ProgrammePage programmeId="programme-1" />);

    const unitLink = await screen.findByRole("link", {
      name: /Derecho de acceso a la información pública/,
    });

    expect(unitLink).toHaveAttribute("href", "/study/unit-2");
  });

  it("shows an empty state when the programme has no units", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ ...programme, units: [] }), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );

    render(<ProgrammePage programmeId="programme-1" />);

    expect(await screen.findByText("No programme units are available yet.")).toBeVisible();
  });

  it("shows an error when the programme cannot be loaded", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("Network error")));

    render(<ProgrammePage programmeId="programme-1" />);

    await waitFor(() => {
      expect(screen.getByText("Unable to load programme.")).toBeVisible();
    });
  });

  it("requests the selected programme from the study API", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(programme), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<ProgrammePage programmeId="programme-1" />);

    await screen.findByRole("link", {
      name: /Derecho de acceso a la información pública/,
    });

    expect(fetchMock).toHaveBeenCalledWith("/api/study/programmes/programme-1");
  });
});
