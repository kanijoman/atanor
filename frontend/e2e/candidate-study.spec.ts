import { expect, test } from "@playwright/test";

test("allows a candidate to go from a real BOE call to study material", async ({
  page,
}) => {
  await page.goto("/calls");

  await expect(page.getByRole("heading", { name: "Calls" })).toBeVisible();
  await page
    .getByRole("link", { name: "BOE-A-2024-14098.pdf" })
    .click();

  await expect(
    page.getByRole("heading", { name: "BOE-A-2024-14098.pdf" }),
  ).toBeVisible();

  await page.getByRole("link", { name: /^I —/ }).click();

  await expect(
    page.getByRole("heading", { name: "Programme I" }),
  ).toBeVisible();

  const studyUnit = page.getByRole("link", {
    name: /Ley 19\/2013.*transparencia/i,
  });

  await expect(studyUnit).toBeVisible();
  await studyUnit.click();

  await expect(
    page.getByRole("heading", {
      name: /Ley 19\/2013.*transparencia/i,
    }),
  ).toBeVisible();

  await expect(
    page.getByText(
      "Knowledge need: Derecho de acceso a la información pública",
    ),
  ).toBeVisible();

  await expect(
    page.getByRole("heading", { name: "Study material" }),
  ).toBeVisible();
  await expect(page.getByText(/Artículo 12/)).toBeVisible();

  await expect(
    page.getByRole("heading", { name: "Study coverage" }),
  ).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Covered aspects" }),
  ).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Pending aspects" }),
  ).toBeVisible();
});
