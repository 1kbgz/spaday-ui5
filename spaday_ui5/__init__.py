import json
from pathlib import Path

from spaday import ComponentPackage

from . import components as _components
from .components import *
from .components import __all__ as _component_names

__version__ = "0.1.0"

_EXTENSION = Path(__file__).parent / "extension"
# UI5's modules, and the framework, icon, theming and localization packages they share state
# through, under their own bare specifiers, written by the JS build (js/tools/vendor.mjs): a library
# on the page that imports UI5 resolves to this copy instead of registering the same tags a second
# time
_IMPORTS = _EXTENSION / "vendor" / "imports.json"

# the exact version of each JS library the package serves, written by its JS build
_VERSIONS = _EXTENSION / "versions.json"

package = ComponentPackage(
    name="ui5",
    assets_dir=_EXTENSION,
    assets=(("css", "css/ui5.css"), ("js", "cdn/index.js")),
    components=tuple(getattr(_components, name) for name in _component_names),
    imports=tuple(json.loads(_IMPORTS.read_text(encoding="utf-8")).items()) if _IMPORTS.exists() else (),
    provides=json.loads(_VERSIONS.read_text(encoding="utf-8")) if _VERSIONS.exists() else {},
)

#: ``css()`` kwarg → (CSS custom property, what it controls), in the shape of
#: :data:`spaday.theme.SHELL_TOKENS`.
#:
#: UI5 is a design system, so this package themes the *other* way round from a rendering package:
#: rather than exposing ``--spa-ui5-*`` tokens of its own, its stylesheet maps UI5's theme
#: parameters onto the ``--spa-*`` palette that spaday's shell and every other component package
#: reads. Set these and the whole page follows — shell, graphs, tables, trees::
#:
#:     App().css(sapBrandColor="#0C4253")
#:
#: ``--sapList_BorderColor`` (driving ``--spa-border``) and ``--sapContent_LabelColor`` (driving
#: ``--spa-muted``) are wired too, but a ``css()`` kwarg spells ``_`` as ``-``, so those two are set
#: with plain CSS instead.
TOKENS = {
    "sapBaseColor": ("--sapBaseColor", "drives --spa-surface"),
    "sapBackgroundColor": ("--sapBackgroundColor", "drives --spa-surface-2"),
    "sapBrandColor": ("--sapBrandColor", "drives --spa-accent"),
    "sapInformativeColor": ("--sapInformativeColor", "drives --spa-info"),
    "sapPositiveColor": ("--sapPositiveColor", "drives --spa-success"),
    "sapCriticalColor": ("--sapCriticalColor", "drives --spa-warning"),
    "sapNegativeColor": ("--sapNegativeColor", "drives --spa-danger"),
}

__all__ = [*_component_names, "TOKENS", "package"]  # noqa: PLE0604
