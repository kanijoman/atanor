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

  await expect(page.getByText(/^Knowledge need: Las Leyes del Procedimiento/)).toBeVisible();

  await expect(page.getByRole("heading", { name: "Study material" })).toBeVisible();
  await expect(page.getByText(/Ley 29\/1998, Artículo 25\./)).toBeVisible();
  await expect(
    page.getByText("Acquired from an authoritative source · not yet reviewed by an expert"),
  ).toBeVisible();

  await expect(page.getByRole("heading", { name: "Sources" })).toBeVisible();
  for (const [title, id] of [
    ["Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común", "BOE-A-2015-10565"],
    ["Ley 40/2015, de 1 de octubre, de Régimen Jurídico del Sector Público", "BOE-A-2015-10566"],
    ["Ley 29/1998, de 13 de julio, reguladora de la Jurisdicción", "BOE-A-1998-16718"],
  ]) {
    const source = page.getByRole("link", { name: new RegExp(`^${title}`) });
    await expect(source).toBeVisible();
    await expect(source).toHaveAttribute("href", `https://www.boe.es/buscar/act.php?id=${id}`);
  }

  await expect(page.getByRole("heading", { name: "Study coverage" })).toBeVisible();
  await expect(page.getByText("Covered · 6 of 6 aspects covered (100%)")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Study aspects" })).toBeVisible();
  await expect(
    page.getByText(/^Covered · El procedimiento administrativo común y sus fases/),
  ).toBeVisible();
  await expect(page.getByText(/^Covered · El recurso contencioso-administrativo/)).toBeVisible();
  await expect(
    page.getByText(/^Covered · Las partes: capacidad, legitimación, representación y defensa/),
  ).toBeVisible();
});
