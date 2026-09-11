import "@testing-library/jest-dom/vitest";
import { afterEach, describe, expect, it, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";

import { ProgrammesPage } from "./ProgrammesPage";

const programmes = [
  {
    id: "programme-1",
    identifier: "I",
    title: "Programa oficial",
  },
  {
    id: "programme-2",
    identifier: "II",
    title: "Programa técnico",
  },
];

describe("ProgrammesPage", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("shows the available programmes returned by the API", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify(programmes), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );

    render(<ProgrammesPage />);

    expect(screen.getByRole("heading", { name: "Programmes" })).toBeVisible();
    expect(screen.getByText("Loading programmes…")).toBeVisible();

    const officialProgramme = await screen.findByRole("link", {
      name: /Programa oficial/,
    });
    const technicalProgramme = screen.getByRole("link", {
      name: /Programa técnico/,
    });

    expect(officialProgramme).toHaveTextContent("I");
    expect(officialProgramme).toHaveTextContent("Programa oficial");
    expect(technicalProgramme).toHaveTextContent("II");
    expect(technicalProgramme).toHaveTextContent("Programa técnico");
  });

  it("offers a selectable link for each programme", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify([programmes[0]]), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );

    render(<ProgrammesPage />);

    const programmeLink = await screen.findByRole("link", {
      name: /Programa oficial/,
    });

    expect(programmeLink).toHaveAttribute("href", "/programmes/programme-1");
  });

  it("shows an empty state when no programmes are available", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response("[]", {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );

    render(<ProgrammesPage />);

    expect(
      await screen.findByText("No programmes are available yet."),
    ).toBeVisible();
  });

  it("shows an error when the programmes cannot be loaded", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("Network error")));

    render(<ProgrammesPage />);

    await waitFor(() => {
      expect(screen.getByText("Unable to load programmes.")).toBeVisible();
    });
  });

  it("requests programmes from the study API", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify([programmes[0]]), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<ProgrammesPage />);

    await screen.findByRole("link", { name: /Programa oficial/ });

    expect(fetchMock).toHaveBeenCalledWith("/api/study/programmes");
  });
});
