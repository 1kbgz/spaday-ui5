import ast
from pathlib import Path

from spaday import element, generate
from spaday.bootstrap import bootstrap

from spaday_ui5 import TOKENS, Ui5Button, Ui5Input, Ui5Tag, package

ROOT = Path(__file__).parent.parent


def test_generated_components_serialize():
    node = element("div").child(Ui5Button(design="Emphasized").text("Save"), Ui5Input(placeholder="Name")).to_node()
    assert [child["tag"] for child in node["slots"]["default"]] == ["ui5-button", "ui5-input"]
    assert node["slots"]["default"][0]["props"]["design"] == {"Str": "Emphasized"}


def test_catalog_covers_the_package():
    tags = {schema.tag for schema in package.catalog}
    assert {"ui5-button", "ui5-input", "ui5-table", "ui5-date-picker"} <= tags
    assert len(tags) == 125
    # UI5 calls its default slot "default"; the catalog uses the "" every other package does
    assert "" in Ui5Button.schema.slots and "default" not in Ui5Button.schema.slots
    design = next(prop for prop in Ui5Tag.schema.props if prop.name == "design")
    assert design.kind == "enum" and "Positive" in design.choices


def test_package_drives_bootstrap_asset_urls():
    html = bootstrap(packages=[package])
    assert 'href="/components/ui5/css/ui5.css"' in html
    assert 'src="/components/ui5/cdn/index.js"' in html
    assert '"@ui5/webcomponents/dist/": "/components/ui5/vendor/@ui5/webcomponents/dist/"' in html
    assert '"@ui5/webcomponents-base/dist/"' in html  # the framework state a library has to share
    # the bundle's own imports resolve through the map, so it must come first
    assert html.index('type="importmap"') < html.index('src="/components/ui5/cdn/index.js"')


def test_published_imports_are_served():
    assert package.imports, "the JS build writes the import map; run it first"
    for specifier, path in package.imports:
        target = package.assets_dir / path
        assert target.is_dir() if path.endswith("/") else target.is_file(), f"{specifier} maps to {path}, which the build did not produce"


def test_tokens_are_ui5_parameters_the_css_kwarg_produces():
    for kwarg, (prop, description) in TOKENS.items():
        assert prop == f"--{kwarg}" and description.startswith("drives --spa-")
        assert element("div").css(**{kwarg: "x"}).to_node()["props"]["style"]["Str"] == f"{prop}: x"


def test_generated_catalog_is_current():
    fresh = generate(str(ROOT / "custom-elements.json"))
    assert ast.dump(ast.parse(fresh)) == ast.dump(ast.parse((ROOT / "components.py").read_text(encoding="utf-8")))
