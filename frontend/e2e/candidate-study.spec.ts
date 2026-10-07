import { expect, test } from "@playwright/test";

test("allows a candidate to go from a real BOE call to study material", async ({ page }) => {
  await page.goto("/calls");

  await expect(page.getByRole("heading", { name: "Calls" })).toBeVisible();
  await page.getByRole("link", { name: "BOE-A-2024-14098.pdf" }).click();

  await expect(page.getByRole("heading", { name: "BOE-A-2024-14098.pdf" })).toBeVisible();

  await page.getByRole("link", { name: /^I —/ }).click();

  await expect(page.getByRole("heading", { name: "Programme I" })).toBeVisible();

  await expect(page.getByText("13 of 28 units have study material")).toBeVisible();
  await expect(page.getByRole("heading", { name: "I. Organización pública" })).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "II. Actividad administrativa y ofimática" }),
  ).toBeVisible();
  await expect(
    page.getByText(/Derechos y deberes fundamentales\. Su garantía y suspensión\./),
  ).toBeVisible();

  const studyUnit = page.getByRole("link", {
    name: /11\.\s+Las Leyes del Procedimiento Administrativo Común.*Administraciones/i,
  });

  await expect(studyUnit).toBeVisible();
  await studyUnit.click();

  await expect(
    page.getByRole("heading", {
      name: "Las Leyes del Procedimiento Administrativo Común de las Administraciones",
    }),
  ).toBeVisible();

  await expect(page.getByText("Knowledge need: Procedimiento administrativo común")).toBeVisible();

  await expect(page.getByRole("heading", { name: "Study material" })).toBeVisible();
  await expect(page.getByText(/Artículo 1/)).toBeVisible();
  await expect(
    page.getByText("Acquired from an authoritative source · not yet reviewed by an expert"),
  ).toBeVisible();

  await expect(page.getByRole("heading", { name: "Sources" })).toBeVisible();
  const canonicalSource = page.getByRole("link", {
    name: "Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las Administraciones Públicas",
  });
  await expect(canonicalSource).toBeVisible();
  await expect(canonicalSource).toHaveAttribute(
    "href",
    "https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565",
  );

  await expect(page.getByRole("heading", { name: "Study coverage" })).toBeVisible();
  await expect(page.getByText("Covered · 8 of 8 aspects covered (100%)")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Study aspects" })).toBeVisible();
  await expect(
    page.getByText(/^Covered · Objeto y finalidad del procedimiento administrativo común/),
  ).toBeVisible();
  await expect(
    page.getByText(/^Covered · Interesados, capacidad, representación y derechos/),
  ).toBeVisible();
});
