/* A stand-in for a downstream component library built on UI5.
 *
 * It imports UI5 the way a library built on it does, by UI5's own bare specifiers, left as imports
 * in its bundle. spaday-ui5 publishes its copy under those specifiers in the page's import map, so
 * they resolve to the modules that already registered the catalog: the page keeps one copy, and
 * nothing registers the same tag names twice.
 */

import Button from "@ui5/webcomponents/dist/Button.js";

class DemoAction extends HTMLElement {
  connectedCallback() {
    if (this.firstElementChild) return;
    const button = document.createElement("ui5-button");
    button.textContent = this.getAttribute("label") ?? "Go";
    // only true when the class this library imported is the one the page registered
    this.dataset.sharedClass = String(button instanceof Button);
    this.append(button);
  }
}

if (!customElements.get("demo-action")) {
  customElements.define("demo-action", DemoAction);
}
