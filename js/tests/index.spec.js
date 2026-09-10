import { expect, test } from "@playwright/test";

test("registers and renders the UI5 catalog", async ({ page }) => {
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto("/dist/index.html");
  await page.evaluate(() => {
    const button = document.createElement("ui5-button");
    button.textContent = "Run";
    document.body.appendChild(button);
  });
  await expect
    .poll(() =>
      page.locator("ui5-button").evaluate((button) => !!button.shadowRoot),
    )
    .toBe(true);
  expect(
    await page.evaluate(() => ({
      table: !!customElements.get("ui5-table"),
      datePicker: !!customElements.get("ui5-date-picker"),
    })),
  ).toEqual({ table: true, datePicker: true });
  expect(errors).toEqual([]);
});

test("survives an application that already registered a UI5 element", async ({
  page,
}) => {
  // an app shipping its own copy of UI5 registers `ui5-button` first; without the define-guard this
  // bundle throws from `customElements.define` and the page renders no UI5 at all
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.addInitScript(() => {
    customElements.define("ui5-button", class extends HTMLElement {});
  });
  await page.goto("/dist/index.html");
  await page.waitForFunction(() => !!customElements.get("ui5-input"));
  expect(errors).toEqual([]);
  expect(
    await page.evaluate(() => ({
      theirs: !document.createElement("ui5-button").shadowRoot,
      restored: String(customElements.define).includes("native code"),
    })),
  ).toEqual({ theirs: true, restored: true });
});

test("publishes the UI5 version it serves", async ({ page }) => {
  await page.goto("/dist/index.html");
  await page.waitForFunction(() => !!globalThis.__spadayUi5);
  expect(await page.evaluate(() => globalThis.__spadayUi5.version)).toMatch(
    /^\d+\.\d+\.\d+/,
  );
});

test("follows spaday's page mode on the root", async ({ page }) => {
  await page.goto("/dist/index.html");
  await page.waitForFunction(() => !!globalThis.__spadayUi5);
  const token = (name) =>
    page.evaluate(
      (name) =>
        getComputedStyle(document.documentElement).getPropertyValue(name),
      name,
    );
  const light = {
    ui5: await token("--sapBaseColor"),
    spa: await token("--spa-surface"),
  };
  await page.evaluate(() => document.documentElement.classList.add("wa-dark"));
  // setTheme loads the dark parameters asynchronously
  await expect.poll(() => token("--sapBaseColor")).not.toBe(light.ui5);
  expect(await token("--spa-surface")).not.toBe(light.spa); // the shell palette follows
  await page.evaluate(() =>
    document.documentElement.classList.remove("wa-dark"),
  );
  await expect.poll(() => token("--sapBaseColor")).toBe(light.ui5);
});
