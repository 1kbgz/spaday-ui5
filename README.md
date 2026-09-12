# spaday-ui5

Typed [UI5 Web Components](https://ui5.github.io/webcomponents/) and browser assets for [spaday](https://github.com/1kbgz/spaday).

[![Build Status](https://github.com/1kbgz/spaday-ui5/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/1kbgz/spaday-ui5/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/1kbgz/spaday-ui5/branch/main/graph/badge.svg)](https://codecov.io/gh/1kbgz/spaday-ui5)
[![License](https://img.shields.io/github/license/1kbgz/spaday-ui5)](https://github.com/1kbgz/spaday-ui5)
[![PyPI](https://img.shields.io/pypi/v/spaday-ui5.svg)](https://pypi.python.org/pypi/spaday-ui5)

[![Preview of UI5 components in spaday rendering a procurement cockpit](https://raw.githubusercontent.com/1kbgz/spaday-ui5/main/docs/img/preview.webp)](https://1kbgz.github.io/spaday-ui5/lite/)

## Overview

```python
from spaday import SetField, element, serve
from spaday_ui5 import Ui5Button, Ui5Tag

page = element("div").child(
    Ui5Button(design="Positive").text("Approve").on("click", SetField("state", "approved")),
    Ui5Tag(design="Information").bind("textContent", "state"),
)
serve(page, packages=["ui5"], store={"state": "pending"})
```

Every element of `@ui5/webcomponents` has a typed class — 125 of them — generated from its Custom
Elements Manifest, so props, events and slots are checked when you author the tree; enum props such as
`design` carry their choices. Installing the package does not inject assets; select it with
`packages=["ui5"]` or pass the exported `package` descriptor.

## Browser examples

- [Procurement cockpit](https://1kbgz.github.io/spaday-ui5/lite/) — complete interactive example, with Python running in Pyodide.
- [Component gallery](https://1kbgz.github.io/spaday-ui5/lite/?example=gallery) — all 125 generated UI5 wrappers and their Python source.

## Run the local example

```bash
python -m pip install -e ".[examples]"
python -m spaday_ui5.example
```

Open `http://127.0.0.1:8026` for the [procurement cockpit](spaday_ui5/example.py): KPI cards with a
progress indicator and rating fed live from Python, a list of requisitions streamed over transports and
approved or rejected through Python endpoints with a toast, a supplier table whose cells update in place,
a requisition form of input, select, step input, date picker, combo box, checkbox and text area two-way
bound to spaday state and confirmed in a dialog, and a dark switch that moves UI5 and the spaday shell to
`sap_horizon_dark` together.

Run `python -m spaday_ui5.gallery` and open `http://127.0.0.1:8027` for the exhaustive local component gallery.

## Theming

The stylesheet maps spaday's `--spa-*` shell palette onto UI5's theme parameters, so a UI5 theme
restyles the shell and every other spaday component package with it. `TOKENS` lists the parameters
wired to the palette that `css()` can set:

```python
App().css(sapBrandColor="#0C4253")
```

The theme follows spaday's page mode: a `wa-dark` class on the root (for example
`App(...).bind_root_class("wa-dark", "dark")`) switches to `sap_horizon_dark` and back. UI5 themes
the whole document at once, so a `wa-dark` island inside a light page stays light. A page that never
uses `wa-dark` keeps whatever theme it configures, and every UI5 theme is available to `setTheme()`.

## Sharing UI5 with your own library

UI5 registers global custom element names, and its framework keeps the configuration, theme and
icon and translation registries every element reads. The package serves UI5's modules under their
own bare specifiers — `@ui5/webcomponents/dist/…`, `@ui5/webcomponents-base/dist/…`, the icon,
theming and localization packages — through the page's import map. A library built on UI5 that
leaves those imports out of its bundle (`external: ["@ui5/*"]` with esbuild) gets this copy: its
elements register once, and its `setTheme()` and icon imports reach these.

Serving every module those packages export makes the tree large, and a page that loads the whole
catalog makes several hundred module requests; serve it over HTTP/2 or with compression.

> [!NOTE]
> This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).
