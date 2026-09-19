import { expect, test } from "@playwright/test";

const PAGE = "http://127.0.0.1:8031";

test("renders UI5 controls and one explicit fallback", async ({ page }) => {
  await page.goto(PAGE);
  await page.locator("#dialog").waitFor({ state: "attached" });
  expect(
    await page.evaluate(() =>
      [
        "save",
        "name",
        "notes",
        "count",
        "date",
        "agree",
        "dark",
        "plan",
        "volume",
        "alert",
        "progress",
        "dialog",
      ].map((id) => document.getElementById(id).localName),
    ),
  ).toEqual([
    "ui5-button",
    "ui5-input",
    "ui5-textarea",
    "ui5-step-input",
    "ui5-date-picker",
    "ui5-checkbox",
    "ui5-switch",
    "ui5-select",
    "ui5-slider",
    "ui5-message-strip",
    "ui5-progress-indicator",
    "ui5-dialog",
  ]);
  await expect(page.locator("[data-ui-fallback]")).toHaveCount(1);
  await expect(page.locator("#progress")).toHaveJSProperty("value", 50);
});

test("UI5 values round-trip through the shared store", async ({ page }) => {
  await page.goto(PAGE);
  const state = page.locator("#state");
  await page.locator("#name").evaluate((element) => {
    element.value = "Ada";
    element.dispatchEvent(new Event("input", { bubbles: true }));
  });
  await page.locator("#count").evaluate((element) => {
    element.value = 4;
    element.dispatchEvent(new Event("input", { bubbles: true }));
  });
  await page.locator("#agree").click();
  await page.locator("#dark").click();
  await expect(state).toContainText("Ada||4|2026-09-14|true|true|");
  await page.locator("#save").click();
  await expect(state).toContainText("|true|false");
});

test("dialog and validation state remain bound", async ({ page }) => {
  await page.goto(PAGE);
  const dialog = page.locator("#dialog");
  await expect(dialog).toHaveJSProperty("open", false);
  await page.locator("#open").click();
  await expect(dialog).toHaveJSProperty("open", true);
  await dialog.evaluate((element) => {
    element.open = false;
    element.dispatchEvent(new Event("close"));
  });
  await expect(page.locator("#state")).toContainText("|false");
  await expect(page.locator("#email")).toHaveJSProperty(
    "valueState",
    "Negative",
  );
  await expect(page.getByText("Required")).toBeVisible();
});
