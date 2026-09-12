"""Gallery of every UI5 component wrapped by spaday-ui5."""

from __future__ import annotations

import io
import keyword
import textwrap
import tokenize

from spaday import SetProp, by_id, element
from spaday.backends.starlette import serve
from spaday.components.shell import App, Body, Main, Nav

from . import (
    Ui5Avatar,
    Ui5AvatarGroup,
    Ui5Breadcrumbs,
    Ui5BreadcrumbsItem,
    Ui5BusyIndicator,
    Ui5Button,
    Ui5Checkbox,
    Ui5DatePicker,
    Ui5Input,
    Ui5Li,
    Ui5List,
    Ui5MessageStrip,
    Ui5Option,
    Ui5ProgressIndicator,
    Ui5RatingIndicator,
    Ui5Select,
    Ui5Slider,
    Ui5Switch,
    Ui5Tab,
    Ui5Tabcontainer,
    Ui5Tag,
    Ui5Title,
    Ui5ToggleButton,
    Ui5Toolbar,
    Ui5ToolbarButton,
    Ui5ToolbarSpacer,
    components as _components,
    package,
)

COMPONENT_NAMES = tuple(_components.__all__)
COMPONENT_SNIPPETS: list[str] = []


def _snippet(names: str, body: str) -> str:
    source = f"from spaday_ui5 import {names}\n\n{textwrap.dedent(body).strip()}\n"
    COMPONENT_SNIPPETS.append(source)
    return source


def _offsets(source: str) -> list[int]:
    offsets = [0]
    for line in source.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))
    return offsets


def _code(source: str):
    """Render dependency-free highlighted Python."""
    offsets = _offsets(source)
    children = []
    cursor = 0
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type == tokenize.ENDMARKER:
            continue
        start = offsets[token.start[0] - 1] + token.start[1]
        end = offsets[token.end[0] - 1] + token.end[1]
        if start > cursor:
            children.append(source[cursor:start])
        token_class = None
        if token.type == tokenize.NAME and keyword.iskeyword(token.string):
            token_class = "keyword"
        elif token.type == tokenize.STRING:
            token_class = "string"
        elif token.type == tokenize.NUMBER:
            token_class = "number"
        elif token.type == tokenize.COMMENT:
            token_class = "comment"
        elif token.type == tokenize.OP:
            token_class = "operator"
        children.append(element("span", class_=f"token-{token_class}").text(token.string) if token_class else token.string)
        cursor = end
    return element("pre", element("code", *children), class_="code-block")


def _demo(title: str, description: str, source: str, preview):
    return element(
        "article",
        element(
            "header",
            element("div", element("h2").text(title), element("p").text(description)),
            element("span", class_="language-pill").text("Python"),
            class_="demo-heading",
        ),
        element("div", preview, class_="preview"),
        _code(source),
        class_="gallery-card",
    )


def _catalog_component(name: str, schema):
    """Create a visible, labeled instance instead of an empty hidden probe."""
    label = schema.tag.removeprefix("ui5-").replace("-", " ").title()
    props = {prop.name for prop in schema.props}
    values = {
        "display-value": "64%",
        "header-text": label,
        "initials": "UI",
        "subtitle-text": "Live preview",
        "text": label,
        "title-text": label,
    }
    kwargs = {prop.replace("-", "_"): value for prop, value in values.items() if prop in props}
    kwargs.update(
        {
            "Ui5AvatarBadge": {"icon": "employee", "state": "Positive"},
            "Ui5BusyIndicator": {"active": True, "text": "Loading"},
            "Ui5ButtonBadge": {"text": "3"},
            "Ui5Checkbox": {"checked": True, "text": "Selected"},
            "Ui5ColorPaletteItem": {"value": "#0a6ed1"},
            "Ui5Date": {"value": "2026-09-14"},
            "Ui5DateRange": {"start_value": "2026-09-14", "end_value": "2026-09-18"},
            "Ui5Icon": {"name": "employee"},
            "Ui5InputIcon": {"name": "search"},
            "Ui5ProgressIndicator": {"value": 64, "display_value": "64%"},
            "Ui5RadioButton": {"checked": True, "text": "Selected"},
            "Ui5RangeSlider": {"value": 28, "end_value": 72},
            "Ui5RatingIndicator": {"value": 4},
            "Ui5Slider": {"value": 64},
            "Ui5SpecialDate": {"value": "2026-09-14"},
            "Ui5Switch": {"checked": True, "text_on": "On", "text_off": "Off"},
            "Ui5Token": {"text": "Token"},
        }.get(name, {})
    )
    component = getattr(_components, name)(**kwargs)
    if "" in schema.slots and "text" not in props:
        component.text(label)
    return component


def _catalog_preview(name: str, schema):
    """Render a component directly or through the parent context it requires."""
    component = _catalog_component(name, schema)
    label = schema.tag.removeprefix("ui5-").replace("-", " ").title()

    if name == "Ui5AvatarBadge":
        parent = Ui5Avatar(initials="UI").child_in("badge", component)
        return element("div", parent, class_="structural-preview")
    if name in {"Ui5Date", "Ui5DateRange"}:
        return element("div", _components.Ui5Calendar(component), class_="structural-preview")
    if name == "Ui5SpecialDate":
        parent = _components.Ui5Calendar().child_in("specialDates", component)
        return element("div", parent, class_="structural-preview")
    if name == "Ui5Form":
        parent = _components.Ui5Form(
            _components.Ui5FormItem(_components.Ui5Input(value="Live preview")).child_in("labelContent", _components.Ui5Label().text("Field"))
        )
        return element("div", parent, class_="structural-preview")
    if name in {"Ui5Tab", "Ui5TabSeparator"}:
        return element(
            "div",
            Ui5Tabcontainer(
                Ui5Tab(text="Overview", selected=True),
                component,
                Ui5Tab(text="Activity"),
            ),
            class_="structural-preview",
        )
    if name in {
        "Ui5TableHeaderRow",
        "Ui5TableRow",
        "Ui5TableSelection",
        "Ui5TableSelectionMulti",
        "Ui5TableSelectionSingle",
        "Ui5TableVirtualizer",
    }:
        table = _components.Ui5Table(_components.Ui5TableRow(_components.Ui5TableCell().text("Live row"))).child_in(
            "headerRow",
            _components.Ui5TableHeaderRow(_components.Ui5TableHeaderCell().text("Component")),
        )
        if name in {"Ui5TableHeaderRow", "Ui5TableRow"}:
            table = _components.Ui5Table(_components.Ui5TableRow(_components.Ui5TableCell().text("Live row"))).child_in(
                "headerRow",
                _components.Ui5TableHeaderRow(_components.Ui5TableHeaderCell().text("Component")),
            )
        else:
            table = table.child_in("features", component)
        return element("div", table, class_="structural-preview")
    if name == "Ui5ToolbarSpacer":
        return element(
            "div",
            Ui5Toolbar(Ui5ToolbarButton(text="Start"), component, Ui5ToolbarButton(text="End")),
            class_="structural-preview",
        )
    if name == "Ui5DropIndicator":
        target_id = "catalog-drop-indicator"
        return element(
            "div",
            element("span").text("Drop target"),
            _components.Ui5DropIndicator(id=target_id, placement="After"),
            class_="drop-indicator-preview",
        )
    if name == "Ui5SliderTooltip":
        target_id = "catalog-slider-tooltip"
        return element(
            "div",
            Ui5Button(id=f"{target_id}-opener").text("Open Slider Tooltip").on("click", SetProp(by_id(target_id), "open", True)),
            _components.Ui5SliderTooltip(id=target_id, value="64", editable=True),
            class_="overlay-preview",
        )
    if name == "Ui5TimePickerClock":
        return _components.Ui5TimePickerClock(
            **{
                "active": True,
                "display-step": 1,
                "item-max": 12,
                "item-min": 1,
                "selected-value": 10,
                "value-step": 1,
            }
        )
    if name == "Ui5MenuSeparator":
        target_id = "catalog-menu-separator"
        opener_id = f"{target_id}-opener"
        menu = _components.Ui5Menu(
            _components.Ui5MenuItem(text="First item"),
            component,
            _components.Ui5MenuItem(text="Second item"),
            id=target_id,
            opener=opener_id,
        )
        return element(
            "div",
            Ui5Button(id=opener_id).text("Open Menu Separator").on("click", SetProp(by_id(target_id), "open", True)),
            menu,
            class_="overlay-preview",
        )
    if name in {
        "Ui5ColorPalettePopover",
        "Ui5Dialog",
        "Ui5Menu",
        "Ui5Popover",
        "Ui5ResponsivePopover",
        "Ui5Toast",
    }:
        target_id = f"catalog-{schema.tag.removeprefix('ui5-')}"
        opener_id = f"{target_id}-opener"
        if name == "Ui5ColorPalettePopover":
            component = _components.Ui5ColorPalettePopover(
                _components.Ui5ColorPaletteItem(value="#0a6ed1"),
                id=target_id,
                opener=opener_id,
            )
        elif name == "Ui5Menu":
            component = _components.Ui5Menu(
                _components.Ui5MenuItem(text="Live menu item"),
                _components.Ui5MenuSeparator(),
                _components.Ui5MenuItem(text="Second item"),
                id=target_id,
                opener=opener_id,
            )
        else:
            component = getattr(_components, name)(
                element("p").text(f"Live {label.lower()} content"),
                id=target_id,
                opener=opener_id if name in {"Ui5Popover", "Ui5ResponsivePopover"} else None,
                header_text=label if name in {"Ui5Dialog", "Ui5Popover", "Ui5ResponsivePopover"} else None,
            )
        return element(
            "div",
            Ui5Button(id=opener_id).text(f"Open {label}").on("click", SetProp(by_id(target_id), "open", True)),
            component,
            class_="overlay-preview",
        )
    return component


actions = _demo(
    "Actions and status",
    "Pair UI5 action hierarchy with compact, semantic status feedback.",
    _snippet(
        "Ui5BusyIndicator, Ui5Button, Ui5Tag, Ui5ToggleButton",
        """
        controls = [
            Ui5Button(design="Emphasized").text("Create request"),
            Ui5Button(design="Transparent").text("Save draft"),
            Ui5ToggleButton(pressed=True).text("Following"),
            Ui5Tag(design="Positive").text("Approved"),
            Ui5BusyIndicator(active=True, size="S"),
        ]
        """,
    ),
    element(
        "div",
        Ui5Button(design="Emphasized", icon="add").text("Create request"),
        Ui5Button(design="Transparent").text("Save draft"),
        Ui5ToggleButton(pressed=True).text("Following"),
        Ui5Tag(design="Positive").text("Approved"),
        Ui5BusyIndicator(active=True, size="S"),
        class_="preview-row",
    ),
)

inputs = _demo(
    "Input and selection",
    "Compose familiar enterprise inputs without leaving typed Python.",
    _snippet(
        "Ui5Checkbox, Ui5DatePicker, Ui5Input, Ui5Option, Ui5Select, Ui5Slider, Ui5Switch",
        """
        fields = [
            Ui5Input(value="Quarterly planning"),
            Ui5DatePicker(value="2026-10-01"),
            Ui5Select(Ui5Option(selected=True).text("Operations")),
            Ui5Checkbox(checked=True, text="Preferred suppliers"),
            Ui5Switch(checked=True),
            Ui5Slider(value=64),
        ]
        """,
    ),
    element(
        "div",
        Ui5Input(value="Quarterly planning", show_clear_icon=True),
        Ui5DatePicker(value="2026-10-01"),
        Ui5Select(Ui5Option(selected=True).text("Operations"), Ui5Option().text("Engineering")),
        Ui5Checkbox(checked=True, text="Preferred suppliers"),
        element("div", Ui5Switch(checked=True), Ui5Slider(value=64), class_="switch-slider"),
        class_="form-preview",
    ),
)

navigation = _demo(
    "Navigation and tools",
    "Breadcrumbs, tabs and toolbars establish location and keep actions close.",
    _snippet(
        "Ui5Breadcrumbs, Ui5BreadcrumbsItem, Ui5Tab, Ui5Tabcontainer, Ui5Toolbar, Ui5ToolbarButton, Ui5ToolbarSpacer",
        """
        navigation = Ui5Tabcontainer(
            Ui5Tab(text="Overview", selected=True),
            Ui5Tab(text="Activity"),
        )
        """,
    ),
    element(
        "div",
        Ui5Breadcrumbs(Ui5BreadcrumbsItem().text("Workspace"), Ui5BreadcrumbsItem().text("Procurement")),
        Ui5Tabcontainer(
            Ui5Tab(element("p").text("Portfolio health is on plan."), text="Overview", selected=True),
            Ui5Tab(element("p").text("Recent approval activity."), text="Activity"),
        ),
        Ui5Toolbar(
            Ui5ToolbarButton(icon="filter", text="Filter"),
            Ui5ToolbarSpacer(),
            Ui5ToolbarButton(icon="download", text="Export"),
        ),
        class_="stack-preview",
    ),
)

data_display = _demo(
    "People and progress",
    "Use avatars, lists, ratings and progress to make operational state scannable.",
    _snippet(
        "Ui5Avatar, Ui5AvatarGroup, Ui5Li, Ui5List, Ui5MessageStrip, Ui5ProgressIndicator, Ui5RatingIndicator",
        """
        status = [
            Ui5Avatar(initials="AR"),
            Ui5ProgressIndicator(value=78),
            Ui5RatingIndicator(value=4, readonly=True),
        ]
        """,
    ),
    element(
        "div",
        Ui5AvatarGroup(
            Ui5Avatar(initials="AR", color_scheme="Accent6"),
            Ui5Avatar(initials="JL", color_scheme="Accent2"),
            Ui5Avatar(initials="PO", color_scheme="Accent8"),
        ),
        Ui5List(
            Ui5Li(description="Operations").text("Quarterly planning"),
            Ui5Li(description="Engineering").text("Platform renewal"),
        ),
        Ui5ProgressIndicator(value=78, display_value="78% on time", value_state="Positive"),
        Ui5RatingIndicator(value=4, readonly=True),
        Ui5MessageStrip(design="Information", hide_close_button=True).text("Supplier scores update from Python."),
        class_="stack-preview",
    ),
)

catalog_source = "from spaday_ui5 import (\n" + "\n".join(f"    {name}," for name in COMPONENT_NAMES) + "\n)\n\ncomponents = [\n"
catalog_source += "\n".join(f"    {name}()," for name in COMPONENT_NAMES) + "\n]\n"
COMPONENT_SNIPPETS.append(catalog_source)

catalog = element(
    "article",
    element(
        "header",
        element(
            "div",
            element("h2").text("Complete generated catalog"),
            element("p").text(
                "Every wrapper in the UI5 Main package is rendered below, including interactive overlays and structural parent contexts."
            ),
        ),
        element("span", class_="catalog-count").text(f"{len(COMPONENT_NAMES)} / {len(COMPONENT_NAMES)}"),
        class_="demo-heading",
    ),
    element(
        "div",
        *(
            element(
                "div",
                element("code").text(schema.tag),
                element("div", _catalog_preview(name, schema), class_="catalog-probe"),
                class_="catalog-item",
            )
            for name, schema in zip(COMPONENT_NAMES, package.catalog, strict=True)
        ),
        class_="catalog-grid",
    ),
    element("details", element("summary").text("View exhaustive Python source"), _code(catalog_source)),
    class_="gallery-card catalog-card",
)

page = App(
    Nav(Ui5Title(level="H4").text("spaday · UI5"), Ui5Tag(design="Information").text("Python component gallery")),
    Body(
        Main(
            element(
                "section",
                element("span", class_="eyebrow").text("UI5 WEB COMPONENTS · MAIN PACKAGE"),
                element("h1").text("Component gallery"),
                element("p").text("A polished working set up front, followed by an auditable index of every generated Python wrapper."),
                element(
                    "div",
                    element("span").text("125 typed elements"),
                    element("span").text("UI5 2.26.0"),
                    element("span").text("Runs in Pyodide"),
                    class_="hero-facts",
                ),
                class_="hero",
            ),
            element("section", actions, inputs, navigation, data_display, class_="gallery-grid"),
            catalog,
            class_="gallery-page",
        )
    ),
)

styles = """
<script type="module">import "@ui5/webcomponents-icons/dist/AllIcons.js";</script>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; font-family: var(--sapFontFamily); color: var(--sapTextColor);
    background: radial-gradient(circle at 10% 0%, color-mix(in srgb, var(--sapBrandColor) 12%, transparent), transparent 34rem),
      var(--sapBackgroundColor); }
  spa-nav { position: sticky; z-index: 20; top: 0; justify-content: space-between; border-bottom: 1px solid var(--spa-border);
    background: color-mix(in srgb, var(--sapShellColor, var(--sapBaseColor)) 92%, transparent); backdrop-filter: blur(16px); }
  .gallery-page { display: grid; gap: 1rem; width: min(100%, 78rem); margin: 0 auto; padding: 1.5rem 1rem 3rem; }
  .hero { padding: clamp(1.5rem, 5vw, 3.5rem); border-radius: 1.25rem; color: white;
    background: linear-gradient(125deg, #063b62 0%, #075f8f 54%, #0b75b7 100%);
    box-shadow: 0 1.5rem 3rem color-mix(in srgb, #063b62 20%, transparent); }
  .eyebrow { display: block; margin-bottom: .75rem; font-size: .75rem; font-weight: 700; letter-spacing: .12em; opacity: .75; }
  .hero h1 { max-width: 15ch; margin: 0; font: 700 clamp(2rem, 5vw, 3.5rem)/1.02 var(--sapFontHeaderFamily); letter-spacing: -.035em; }
  .hero > p { max-width: 45rem; margin: 1rem 0 1.25rem; font-size: clamp(1rem, 2vw, 1.2rem); line-height: 1.55; opacity: .88; }
  .hero-facts, .preview-row { display: flex; flex-wrap: wrap; align-items: center; gap: .65rem; }
  .hero-facts span { padding: .4rem .65rem; border: 1px solid #ffffff45; border-radius: 999px; background: #ffffff16; font-size: .8rem; font-weight: 700; }
  .gallery-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }
  .gallery-card { min-width: 0; overflow: hidden; border: 1px solid var(--spa-border); border-radius: 1rem; background: var(--sapBaseColor);
    box-shadow: 0 .6rem 1.6rem color-mix(in srgb, #001b2e 8%, transparent); }
  .demo-heading { display: flex; justify-content: space-between; gap: 1rem; padding: 1.1rem 1.2rem; border-bottom: 1px solid var(--spa-border); }
  .demo-heading h2 { margin: 0; font-size: 1.05rem; }
  .demo-heading p { margin: .35rem 0 0; color: var(--sapContent_LabelColor); font-size: .875rem; line-height: 1.45; }
  .language-pill, .catalog-count { flex: none; align-self: start; padding: .28rem .55rem; border-radius: 999px; color: var(--sapInformativeTextColor);
    background: var(--sapInformativeBackground); font-size: .72rem; font-weight: 700; }
  .preview { min-height: 11rem; padding: 1.25rem; background: color-mix(in srgb, var(--sapBackgroundColor) 65%, var(--sapBaseColor)); }
  .form-preview { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .75rem; }
  .form-preview > *, .switch-slider > * { min-width: 0; }
  .switch-slider { display: flex; align-items: center; gap: 1rem; }
  .switch-slider ui5-slider { flex: 1; }
  .stack-preview { display: grid; gap: .75rem; }
  .code-block { max-width: 100%; min-height: 8rem; max-height: 20rem; margin: 0; overflow: auto; padding: 1rem 1.2rem; color: #dbeafe;
    background: #071a2a; font: .78rem/1.65 ui-monospace, SFMono-Regular, Menlo, monospace; white-space: pre; }
  .token-keyword { color: #7dd3fc; } .token-string { color: #a7f3d0; } .token-number { color: #fcd34d; }
  .token-comment { color: #94a3b8; } .token-operator { color: #c4b5fd; }
  .catalog-card { overflow: visible; }
  .catalog-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: .55rem; padding: 1.2rem; }
  .catalog-item { display: grid; align-content: start; gap: .5rem; min-width: 0; padding: .65rem .75rem; border: 1px solid var(--spa-border); border-radius: .6rem;
    background: color-mix(in srgb, var(--sapBackgroundColor) 72%, var(--sapBaseColor)); }
  .catalog-item code { display: block; overflow: hidden; color: var(--sapLinkColor); font-size: .74rem; text-overflow: ellipsis; white-space: nowrap; }
  .catalog-probe { display: flex; align-items: center; min-width: 0; min-height: 3.5rem; max-height: 20rem; overflow: auto;
    padding: .5rem; border: 1px dashed var(--spa-border); border-radius: .4rem; background: var(--sapBaseColor); }
  .catalog-probe > * { max-width: 100%; }
  .overlay-preview, .structural-preview { display: grid; gap: .5rem; min-width: 0; width: 100%; }
  .structural-preview small { color: var(--sapContent_LabelColor); line-height: 1.35; }
  .drop-indicator-preview { position: relative; min-height: 2.5rem; padding: .65rem; border: 1px solid var(--spa-border); }
  .drop-indicator-preview ui5-drop-indicator { display: block !important; position: absolute; inset: auto 0 0 !important; width: 100%; height: .2rem !important; }
  details { border-top: 1px solid var(--spa-border); }
  summary { padding: 1rem 1.2rem; cursor: pointer; color: var(--sapLinkColor); font-weight: 700; }
  @media (max-width: 760px) {
    spa-nav { position: static; flex-wrap: wrap; gap: .75rem; }
    .gallery-page { padding: .75rem .75rem 2rem; }
    .hero { border-radius: 1rem; }
    .gallery-grid, .form-preview { grid-template-columns: 1fr; }
    .catalog-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .demo-heading { align-items: start; }
  }
  @media (max-width: 380px) { .catalog-grid { grid-template-columns: 1fr; } }
</style>
"""

app = serve(page, packages=[package], head=styles, title="spaday-ui5 gallery")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8027)
