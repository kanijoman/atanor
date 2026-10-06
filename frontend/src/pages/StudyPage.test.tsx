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
  sources: [
    {
      title: "Ley 19/2013, de transparencia, acceso a la información pública y buen gobierno",
      locator: "https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887",
    },
  ],
  coverage: {
    status: "partial",
    covered_count: 2,
    required_count: 8,
    coverage_percentage: 25,
    required_aspects: [
      "Objeto y finalidad del procedimiento administrativo común",
      "Ámbito subjetivo de aplicación",
      "Interesados, capacidad, representación y derechos",
      "Actividad administrativa, plazos y medios electrónicos",
      "Actos administrativos: requisitos, eficacia e invalidez",
      "Procedimiento administrativo común y sus fases",
      "Procedimientos sancionador y de responsabilidad patrimonial",
      "Revisión de actos, recursos, iniciativa legislativa y potestad reglamentaria",
    ],
    covered_aspects: [
      "Objeto y finalidad del procedimiento administrativo común",
      "Ámbito subjetivo de aplicación",
    ],
    pending_aspects: [
      "Interesados, capacidad, representación y derechos",
      "Actividad administrativa, plazos y medios electrónicos",
      "Actos administrativos: requisitos, eficacia e invalidez",
      "Procedimiento administrativo común y sus fases",
      "Procedimientos sancionador y de responsabilidad patrimonial",
      "Revisión de actos, recursos, iniciativa legislativa y potestad reglamentaria",
    ],
  },
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
    expect(screen.getByText("Study coverage")).toBeVisible();
    expect(screen.getByText("Partial · 2 of 8 aspects covered (25%)")).toBeVisible();
    expect(screen.getByRole("heading", { name: "Study aspects" })).toBeVisible();
    expect(screen.getByText(/Objeto y finalidad del procedimiento administrativo común/, { selector: "li" }).textContent).toMatch(/^Covered/);
    expect(screen.getByText(/Interesados, capacidad, representación y derechos/, { selector: "li" }).textContent).toMatch(/^Pending/);
    expect(screen.getAllByText("Covered")).toHaveLength(2);
    expect(screen.getAllByText("Pending")).toHaveLength(6);
    expect(screen.getByRole("link", { name: /Ley 19\/2013/ })).toBeVisible();
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
