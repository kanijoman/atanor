import { fileURLToPath } from "node:url";

import { expect, test } from "@playwright/test";

// Importing a large PDF runs text extraction and programme discovery on the server.
const IMPORT_TIMEOUT_MS = 60_000;

function sample(name: string): string {
  return fileURLToPath(new URL(`../../backend/tests/samples/${name}`, import.meta.url));
}

test("a candidate can import a convocatoria and see what is not supported yet", async ({
  page,
}) => {
  await page.goto("/calls");

  await page
    .getByLabel("Convocatoria PDF")
    .setInputFiles(sample("BOJA24-138-00046-48048-01_00304998.pdf"));
  await page.getByRole("button", { name: "Import convocatoria" }).click();

  await expect(
    page.getByRole("heading", { name: "BOJA24-138-00046-48048-01_00304998.pdf" }),
  ).toBeVisible({ timeout: IMPORT_TIMEOUT_MS });
  await page.getByRole("link", { name: /^II\.1 —/ }).click();

  await expect(page.getByText("0 of 30 units have study material")).toBeVisible();
  await expect(page.getByText("Study material not available").first()).toBeVisible();
  await expect(page.getByText("Study material available", { exact: true })).toHaveCount(0);
});

test("a document that is not a convocatoria is refused with an explanation", async ({ page }) => {
  await page.goto("/calls");

  await page.getByLabel("Convocatoria PDF").setInputFiles(sample("Programa_Archiveros_0.pdf"));
  await page.getByRole("button", { name: "Import convocatoria" }).click();

  await expect(page.getByRole("alert")).toContainText("could not find a convocatoria", {
    timeout: IMPORT_TIMEOUT_MS,
  });
});
