import { expect, test } from "@playwright/test";

/* spaday-ui5 authored from Python, on a page it shares with a downstream library that imports
 * UI5 by its bare specifiers. See spaday_ui5/tests/integration.py.
 */

const PAGE = "http://127.0.0.1:8021";

test("spaday state wires the generated catalog together", async ({ page }) => {
  await page.goto(PAGE);
  // the tag's own text: its shadow root adds an accessibility label of its own
  const badge = page.locator("#badge");
  await expect(badge).toHaveJSProperty("textContent", "pending");
  await page.locator("#approve").click();
  await expect(badge).toHaveJSProperty("textContent", "approved");
  await page.locator("#reject").click();
  await expect(badge).toHaveJSProperty("textContent", "rejected");
});

test("a library importing UI5 by name gets the page's copy", async ({
  page,
}) => {
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto(PAGE);
  const downstream = page.locator("#downstream");
  await expect(downstream.locator("ui5-button")).toBeAttached();
  // the downstream library's imported Button is the class the page registered
  await expect(downstream).toHaveAttribute("data-shared-class", "true");
  // a second copy registering the same tags would have thrown from customElements.define
  expect(errors).toEqual([]);
});

test("the package's own bundle satisfies its generated catalog", async ({
  page,
}) => {
  await page.goto(PAGE);
  const script = await (
    await page.request.get(`${PAGE}/conformance.js`)
  ).text();
  await expect(page.locator("#approve")).toBeAttached();
  expect(await page.evaluate(script)).toEqual([]);
});
