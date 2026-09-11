import "@testing-library/jest-dom/vitest";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { App, resolveRoute } from "./App";

afterEach(() => {
  cleanup();
});

describe("resolveRoute", () => {
  it("resolves the programmes route", () => {
    expect(resolveRoute("/programmes")).toEqual({ name: "programmes" });
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
  it("renders the study page for a study route", () => {
    window.history.pushState({}, "", "/study/unit-1");

    render(<App />);

    expect(screen.getByRole("heading", { name: "Study" })).toBeInTheDocument();
    expect(screen.getByText(/unit-1/)).toBeInTheDocument();
  });
});
