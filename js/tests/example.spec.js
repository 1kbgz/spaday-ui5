import { expect, test } from "@playwright/test";

/* The procurement cockpit in spaday_ui5/example.py, run as its own server. */

const PAGE = "http://127.0.0.1:8026";

test("streams requisitions and supplier performance from Python", async ({
  page,
}) => {
  await page.goto(PAGE);
  const rows = page.locator(".req");
  await expect(rows.first()).toBeVisible();
  const initial = await rows.count();
  // a requisition arrives every few seconds
  await expect
    .poll(() => rows.count(), { timeout: 10_000 })
    .toBeGreaterThan(initial);
  await page.getByRole("tab", { name: /Suppliers/ }).click();
  const onTime = page.locator("#suppliers ui5-progress-indicator").first();
  const before = await onTime.evaluate((el) => el.value);
  await expect
    .poll(() => onTime.evaluate((el) => el.value), { timeout: 5_000 })
    .not.toBe(before);
});

test("approves a requisition through Python", async ({ page }) => {
  await page.goto(PAGE);
  const pending = page
    .locator(".req")
    .filter({ has: page.locator("ui5-tag", { hasText: "Pending" }) })
    .first();
  const id = await pending.getAttribute("data-id");
  await pending.getByRole("button", { name: "Approve" }).click();
  await expect(page.locator("#toast")).toContainText(`Approved ${id}`);
  const row = page.locator(`.req[data-id="${id}"]`);
  // the tag's own text: its shadow root adds an accessibility label of its own
  await expect(row.locator("ui5-tag")).toHaveJSProperty(
    "textContent",
    "Approved",
  );
  await expect(row.getByRole("button", { name: "Approve" })).toBeDisabled();
});

test("submits the requisition form and confirms it in a dialog", async ({
  page,
}) => {
  await page.goto(PAGE);
  await page.getByRole("tab", { name: /New request/ }).click();
  await page.locator("#title input").fill("Conference passes");
  await page.locator("#submit").click();
  const message = page.locator("#submitted-message");
  await expect(message).toContainText("from Acme Components");
  const id = (await message.textContent()).split(" ")[0];
  await page.getByRole("button", { name: "Review approvals" }).click();
  await expect(page.locator(`.req[data-id="${id}"]`)).toContainText(
    "Conference passes",
  );
});

test("the dark switch moves UI5 and the spaday shell to the dark theme", async ({
  page,
}) => {
  await page.goto(PAGE);
  const base = () =>
    page.evaluate(() =>
      getComputedStyle(document.documentElement)
        .getPropertyValue("--sapBaseColor")
        .trim(),
    );
  const light = await base();
  await page.locator("#dark").click();
  await expect(page.locator("html")).toHaveClass(/wa-dark/);
  await expect.poll(base).not.toBe(light);
  // the shell's surface is UI5's base color
  const nav = await page
    .locator("spa-nav")
    .evaluate((el) => getComputedStyle(el).backgroundColor);
  expect(
    await page.evaluate(() => {
      const probe = document.createElement("div");
      probe.style.color = "var(--sapBaseColor)";
      document.body.append(probe);
      return getComputedStyle(probe).color;
    }),
  ).toBe(nav);
});
