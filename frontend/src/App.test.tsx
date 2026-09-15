import "@testing-library/jest-dom/vitest";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { App, resolveRoute } from "./App";

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("resolveRoute", () => {
  it("resolves the root route to calls", () => {
    expect(resolveRoute("/")).toEqual({ name: "calls" });
  });

  it("resolves the calls route", () => {
    expect(resolveRoute("/calls")).toEqual({ name: "calls" });
  });

  it("resolves a call route", () => {
    expect(resolveRoute("/calls/call-1")).toEqual({
      name: "call",
      callId: "call-1",
    });
  });

  it("resolves a programme route", () => {
    expect(resolveRoute("/programmes/programme-1")).toEqual({
      name: "programme",
      programmeId: "programme-1",
    });
  });

  it("resolves a study route", () => {
    expect(resolveRoute("/study/unit-1")).toEqual({
      name: "study",
      unitId: "unit-1",
    });
  });

  it("rejects unknown routes", () => {
    expect(resolveRoute("/unknown")).toEqual({ name: "not-found" });
  });
});

describe("App", () => {
  it("renders the calls page for the root route", () => {
    window.history.pushState({}, "", "/");

    render(<App />);

    expect(screen.getByRole("heading", { name: "Calls" })).toBeInTheDocument();
  });

  it("renders the study page for a study route", async () => {
    window.history.pushState({}, "", "/study/unit-1");

    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            programme_unit: {
              id: "unit-1",
              number: 1,
              title: "Derecho de acceso a la información pública",
            },
            knowledge_need: {
              title: "Derecho de acceso a la información pública",
            },
            study_material:
              "1. Concepto y titulares\nEl derecho de acceso permite a las personas solicitar información pública.",
          }),
          {
            status: 200,
            headers: { "Content-Type": "application/json" },
          },
        ),
      ),
    );

    render(<App />);

    expect(
      await screen.findByRole("heading", {
        name: "Derecho de acceso a la información pública",
      }),
    ).toBeInTheDocument();
    expect(screen.getByText(/derecho de acceso permite/)).toBeInTheDocument();
  });
});
