"""How UI5 renders spaday's generic controls (:mod:`spaday.ui`)."""

from spaday.ui import ControlSpec, Design, Open, Options, Part, Value, Wrap

_BUTTON_INTENTS = {
    "neutral": "Default",
    "primary": "Emphasized",
    "info": "Emphasized",
    "success": "Positive",
    "warning": "Attention",
    "danger": "Negative",
}
_STATES = {
    "neutral": "Information",
    "primary": "Information",
    "info": "Information",
    "success": "Positive",
    "warning": "Critical",
    "danger": "Negative",
}
_FIELD = {"disabled": "disabled", "required": "required", "readonly": "readonly", "name": "name", "size": None}
_WRAP = Wrap(tag="div", props={"class": "ui-field"})
_LABEL = (Part(kind="attr", name="accessible-name"), Part(kind="sibling", tag="ui5-label"))
_HELP = Part(kind="sibling", tag="ui5-text")
_ERROR = Part(kind="sibling", tag="ui5-text", props={"style": "color: var(--sapNegativeTextColor)"}, after=True)
_INVALID = {"value-state": "Negative"}

DESIGN = Design(
    name="ui5",
    controls={
        "button": ControlSpec(
            tag="ui5-button",
            label=Part(kind="text"),
            props={"intent": "design", "appearance": None, "size": None, "disabled": "disabled", "name": None},
            values={"intent": _BUTTON_INTENTS},
        ),
        "input": ControlSpec(
            tag="ui5-input",
            wrap=_WRAP,
            label=_LABEL,
            help=_HELP,
            error=_ERROR,
            invalid=_INVALID,
            props={**_FIELD, "placeholder": "placeholder", "type": "type"},
            values={"type": {"text": "Text", "password": "Password", "email": "Email", "search": "Search", "tel": "Tel", "url": "URL"}},
        ),
        "textarea": ControlSpec(
            tag="ui5-textarea",
            wrap=_WRAP,
            label=_LABEL,
            help=_HELP,
            error=_ERROR,
            invalid=_INVALID,
            props={**_FIELD, "placeholder": "placeholder", "rows": "rows", "minlength": None, "maxlength": "maxlength"},
        ),
        "number-input": ControlSpec(
            tag="ui5-step-input",
            wrap=_WRAP,
            label=_LABEL,
            help=_HELP,
            error=_ERROR,
            invalid=_INVALID,
            props={**_FIELD, "placeholder": "placeholder", "min": "min", "max": "max", "step": "step"},
            value=Value(codec="number"),
        ),
        "date-input": ControlSpec(
            tag="ui5-date-picker",
            fixed={"value-format": "yyyy-MM-dd"},
            wrap=_WRAP,
            label=_LABEL,
            help=_HELP,
            error=_ERROR,
            invalid=_INVALID,
            props={**_FIELD, "min": "min-date", "max": "max-date"},
        ),
        "checkbox": ControlSpec(
            tag="ui5-checkbox",
            wrap=_WRAP,
            label=Part(kind="attr", name="text"),
            help=_HELP,
            error=_ERROR,
            invalid=_INVALID,
            props={**_FIELD},
            value=Value(prop="checked"),
        ),
        "switch": ControlSpec(
            tag="ui5-switch",
            wrap=_WRAP,
            label=_LABEL,
            help=_HELP,
            error=_ERROR,
            invalid={"aria-invalid": "true"},
            props={**_FIELD},
            value=Value(prop="checked"),
        ),
        "select": ControlSpec(
            tag="ui5-select",
            wrap=_WRAP,
            label=_LABEL,
            help=_HELP,
            error=_ERROR,
            invalid=_INVALID,
            props={**_FIELD, "placeholder": None},
            options=Options(kind="children", tag="ui5-option", value="value", label="text", selected="selected"),
            value=Value(codec="json", defer=True),
        ),
        "slider": ControlSpec(
            tag="ui5-slider",
            wrap=_WRAP,
            label=_LABEL,
            help=_HELP,
            error=_ERROR,
            invalid={"aria-invalid": "true"},
            props={
                "disabled": "disabled",
                "required": None,
                "readonly": None,
                "name": "name",
                "size": None,
                "min": "min",
                "max": "max",
                "step": "step",
            },
            value=Value(codec="number"),
        ),
        "alert": ControlSpec(
            tag="ui5-message-strip",
            fixed={"hide-close-button": True},
            label=Part(kind="child", tag="strong"),
            props={"intent": "design"},
            values={"intent": _STATES},
        ),
        "progress": ControlSpec(
            tag="ui5-progress-indicator",
            label=Part(kind="attr", name="accessible-name"),
            props={"max": None},
            value=Value(scale_by="max", scale_to=100, scale_default=1),
        ),
        "dialog": ControlSpec(
            tag="ui5-dialog",
            label=Part(kind="attr", name="header-text"),
            open=Open(prop="open", event="close"),
        ),
    },
)

__all__ = ["DESIGN"]
