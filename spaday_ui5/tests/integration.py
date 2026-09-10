"""A spaday page on spaday-ui5, shared with a downstream library through the import map.

The integration this exercises end to end:

* the generated catalog authored in Python and wired with spaday's own state -- two
  ``Ui5Button``\\ s drive a store field that a ``Ui5Tag`` reads;
* a downstream library that imports UI5 by its bare specifiers, left as imports in its bundle,
  which the page's import map resolves to spaday-ui5's copy, so nothing registers the same tags
  twice. It has no Python of its own beyond a schema-carrying :class:`~spaday.Component` and a
  :class:`~spaday.ComponentPackage` serving its bundle.

Served for the browser tests; ``/conformance.js`` hands back the check that the package's own
bundle implements the catalog generated for it.
"""

from pathlib import Path

import uvicorn
from spaday import Component, ComponentPackage, ComponentSchema, PropertySchema, SetField, check_script, element
from spaday.backends.starlette import serve
from starlette.responses import PlainTextResponse
from starlette.routing import Route

from spaday_ui5 import Ui5Button, Ui5Tag, package as ui5_package


class DemoAction(Component):
    """The downstream library's element, bound from Python with no Python of its own."""

    tag = "demo-action"
    schema = ComponentSchema(
        tag="demo-action",
        class_name="DemoAction",
        summary="An action built from UI5's button.",
        props=(PropertySchema(name="label", kind="string", description="Button label."),),
    )


downstream_package = ComponentPackage(
    name="demo-downstream",
    assets_dir=Path(__file__).parent / "downstream",
    assets=(("js", "downstream.js"),),
    components=(DemoAction,),
)

page = element("div", id="app").child(
    element("section", id="card").child(
        Ui5Button(id="approve", design="Positive").text("Approve").on("click", SetField("state", "approved")),
        Ui5Button(id="reject", design="Negative").text("Reject").on("click", SetField("state", "rejected")),
        Ui5Tag(id="badge", design="Information").bind("textContent", "state"),
    ),
    DemoAction(id="downstream", label="Downstream"),
)


async def conformance(request) -> PlainTextResponse:
    """The browser-side check of spaday-ui5's own bundle against its generated catalog."""
    return PlainTextResponse(check_script([ui5_package]), media_type="text/plain")


app = serve(
    page,
    packages=[ui5_package, downstream_package],
    routes=[Route("/conformance.js", conformance)],
    store={"state": "pending"},
    title="spaday-ui5 integration",
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8021)
