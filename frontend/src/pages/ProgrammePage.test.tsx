import "@testing-library/jest-dom/vitest";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen, waitFor } from "@testing-library/react";

import type { Programme } from "../api";
import { ProgrammePage } from "./ProgrammePage";

const programme: Programme & { id: string } = {
  id: "programme-1",
  identifier: "I",
  title: "Programa oficial",
  coverage: { units_total: 2, units_with_material: 1 },
  units: [
    {
      id: "unit-1",
      number: 1,
      title: "Organización del Estado",
      section: null,
      study_material_available: false,
    },
    {
      id: "unit-2",
      number: 2,
      title: "Derecho de acceso a la información pública",
      section: null,
      study_material_available: true,
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

    expect(screen.getByText("Loading programme…")).toBeVisible();

    expect(await screen.findByRole("heading", { name: "Programme I" })).toBeVisible();
    expect(screen.getByText("1 of 2 units have study material")).toBeVisible();
    expect(screen.getByText("1. Organización del Estado")).toBeVisible();
    expect(
      screen.getByRole("link", {
        name: /Derecho de acceso a la información pública/,
      }),
    ).toBeVisible();
  });

  it("shows which programme units have study material available", async () => {
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

    await screen.findByRole("heading", { name: "Programme I" });

    expect(screen.getByText("Study material not available")).toBeVisible();
    expect(screen.getByText("Study material available")).toBeVisible();
  });

  it("offers a selectable link only for programme units with study material", async () => {
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

    const availableUnitLink = await screen.findByRole("link", {
      name: /Derecho de acceso a la información pública/,
    });

    expect(availableUnitLink).toHaveAttribute("href", "/study/unit-2");
    expect(screen.queryByRole("link", { name: /Organización del Estado/ })).not.toBeInTheDocument();
  });

  it("shows an empty state when the programme has no units", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            ...programme,
            coverage: { units_total: 0, units_with_material: 0 },
            units: [],
          }),
          {
            status: 200,
            headers: { "Content-Type": "application/json" },
          },
        ),
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

    expect(fetchMock).toHaveBeenCalledWith(
      "/api/study/programmes/programme-1",
      expect.objectContaining({ signal: expect.any(AbortSignal) }),
    );
  });

  it("groups units by block when numbering restarts in each block", async () => {
    const blocks: Programme & { id: string } = {
      ...programme,
      coverage: { units_total: 2, units_with_material: 1 },
      units: [
        {
          id: "unit-a",
          number: 1,
          title: "La Constitución Española de 1978. Características.",
          section: "I. Organización pública",
          study_material_available: false,
        },
        {
          id: "unit-b",
          number: 1,
          title: "Atención al público: acogida e información al ciudadano.",
          section: "II. Actividad administrativa y ofimática",
          study_material_available: true,
        },
      ],
    };
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify(blocks), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );

    render(<ProgrammePage programmeId="programme-1" />);

    expect(await screen.findByRole("heading", { name: "I. Organización pública" })).toBeVisible();
    expect(
      screen.getByRole("heading", { name: "II. Actividad administrativa y ofimática" }),
    ).toBeVisible();
    expect(screen.getByText("1. La Constitución Española de 1978. Características.")).toBeVisible();
    expect(screen.getByRole("link", { name: /1\. Atención al público/ })).toHaveAttribute(
      "href",
      "/study/unit-b",
    );
  });
});
