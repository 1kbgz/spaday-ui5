import fs from "fs";
import { expect, test } from "@playwright/test";

const built = fs.existsSync("dist/lite/index.html");

async function waitForPython(page) {
  await page.waitForFunction(
    () =>
      document.documentElement.dataset.ready === "true" ||
      document.querySelector("#pyodide-status")?.textContent ===
        "Unable to start",
    undefined,
    { timeout: 180_000 },
  );
  await expect(page.locator("html")).toHaveAttribute("data-ready", "true");
}

function collectErrors(page) {
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("console", (message) => {
    if (message.type() === "error") errors.push(message.text());
  });
  return errors;
}

async function expectNoHorizontalOverflow(page) {
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - window.innerWidth,
  );
  expect(overflow).toBeLessThanOrEqual(1);
}

async function expectTabNavigationToKeepScrollPosition(page) {
  const tabContainer = page.locator("ui5-tabcontainer");

  for (const name of ["Suppliers", "New request", "Approvals"]) {
    await tabContainer.evaluate((element) => {
      window.scrollTo({
        behavior: "instant",
        top: element.getBoundingClientRect().top + window.scrollY - 120,
      });
    });
    const before = await page.evaluate(() => window.scrollY);
    await page.getByRole("tab", { name }).click();
    await expect
      .poll(() => page.evaluate(() => window.scrollY))
      .toBeCloseTo(before, 0);
  }
}

test("runs the complete procurement example in Pyodide", async ({ page }) => {
  test.skip(!built, "run `make pyodide-example` first");
  test.setTimeout(240_000);
  await page.setViewportSize({ width: 320, height: 800 });
  const errors = collectErrors(page);

  await page.goto("/dist/lite/index.html");
  await waitForPython(page);
  await expect(page.locator(".hero h1")).toHaveText(
    "Control spend without slowing teams",
  );

  const rows = page.locator(".req");
  const initial = await rows.count();
  await expect
    .poll(() => rows.count(), { timeout: 10_000 })
    .toBeGreaterThan(initial);
  const pending = rows
    .filter({ has: page.locator("ui5-tag", { hasText: "Pending" }) })
    .first();
  const id = await pending.getAttribute("data-id");
  await pending.getByRole("button", { name: "Approve" }).click();
  await expect(page.locator("#toast")).toContainText(`Approved ${id}`);

  await expectTabNavigationToKeepScrollPosition(page);

  await expectNoHorizontalOverflow(page);
  expect(errors).toEqual([]);
});

test("runs the complete component gallery in Pyodide", async ({ page }) => {
  test.skip(!built, "run `make pyodide-example` first");
  test.setTimeout(240_000);
  await page.setViewportSize({ width: 320, height: 800 });
  const errors = collectErrors(page);

  await page.goto("/dist/lite/?example=gallery");
  await waitForPython(page);
  await expect(page.locator(".hero h1")).toHaveText("Component gallery");
  await expect(page.locator(".catalog-item")).toHaveCount(125);
  await expect(
    page.locator(".catalog-item > .catalog-probe > ui5-yearrangepicker"),
  ).toBeAttached();
  await expect(page.locator(".token-keyword").first()).toHaveText("from");

  await expectNoHorizontalOverflow(page);
  expect(errors).toEqual([]);
});
