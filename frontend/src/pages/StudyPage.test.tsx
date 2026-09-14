import "@testing-library/jest-dom/vitest";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";

import { StudyPage } from "./StudyPage";

const studyResponse = {
  programme_unit: {
    id: "unit-2",
    number: 2,
    title: "Derecho de acceso a la información pública",
  },
  knowledge_need: {
    title: "Derecho de acceso a la información pública",
  },
  study_material:
    "1. Concepto y titulares\nEl derecho de acceso permite a las personas solicitar información pública. (Artículo 12)",
};

describe("StudyPage", () => {
  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  it("loads and displays candidate study material for the selected unit", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(studyResponse), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<StudyPage unitId="unit-2" />);

    expect(screen.getByText("Loading study material…")).toBeVisible();
    expect(
      await screen.findByRole("heading", {
        name: "Derecho de acceso a la información pública",
      }),
    ).toBeVisible();
    expect(
      screen.getByText("Knowledge need: Derecho de acceso a la información pública"),
    ).toBeVisible();
    expect(screen.getByText(/Artículo 12/)).toBeVisible();
    expect(fetchMock).toHaveBeenCalledWith("/api/study/units/unit-2");
  });

  it("shows an error when study material cannot be loaded", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response("Not found", { status: 404 })),
    );

    render(<StudyPage unitId="unit-2" />);

    expect(
      await screen.findByText("Unable to load study material."),
    ).toBeVisible();
  });
});
