import json

import pytest
from spaday import Alert, Button, DateInput, Dialog, NumberInput, Progress, Select, TextInput, ToggleSwitch, validate
from spaday.ui import conformance, resolve
from spaday.ui.design import _plain

from spaday_ui5 import DESIGN, package


def _props(node: dict) -> dict:
    return {key: _plain(value) for key, value in node.get("props", {}).items()}


def _find(node: dict, tag: str) -> dict:
    if node["tag"] == tag:
        return node
    for children in node.get("slots", {}).values():
        for child in children:
            if isinstance(child, dict):
                try:
                    return _find(child, tag)
                except LookupError:
                    pass
    raise LookupError(tag)


def test_find_walks_all_slots_and_reports_missing_tags():
    tree = {"tag": "root", "slots": {"first": ["text", {"tag": "other"}], "second": [{"tag": "target"}]}}
    assert _find(tree, "target")["tag"] == "target"
    with pytest.raises(LookupError):
        _find(tree, "missing")


def test_the_package_publishes_its_design():
    assert package.design is DESIGN
    assert set(DESIGN.controls) == {
        "alert",
        "button",
        "checkbox",
        "date-input",
        "dialog",
        "input",
        "number-input",
        "progress",
        "select",
        "slider",
        "switch",
        "textarea",
    }


def test_fields_and_buttons_map_to_ui5():
    button = resolve(Button(label="Save", intent="danger", appearance="plain", size="lg").to_node(), DESIGN)
    assert button["tag"] == "ui5-button"
    assert _props(button) == {"textContent": "Save", "design": "Negative"}

    text = resolve(TextInput(label="Name", help="Hint", error="Bad", type="email").to_node(), DESIGN)
    control = _find(text, "ui5-input")
    assert _props(control) == {"accessible-name": "Name", "value-state": "Negative", "type": "Email"}
    assert _props(text["slots"]["default"][0]) == {"textContent": "Name"}
    assert _props(text["slots"]["default"][1]) == {"textContent": "Hint"}
    assert _props(text["slots"]["default"][-1]) == {
        "style": "color: var(--sapNegativeTextColor)",
        "textContent": "Bad",
    }

    number = _find(resolve(NumberInput(label="Count", min=0, max=10, step=1).to_node(), DESIGN), "ui5-step-input")
    assert _props(number) == {"accessible-name": "Count", "min": 0, "max": 10, "step": 1}

    date = _find(resolve(DateInput(label="Date", min="2026-01-01", max="2026-12-31").to_node(), DESIGN), "ui5-date-picker")
    assert _props(date) == {
        "value-format": "yyyy-MM-dd",
        "accessible-name": "Date",
        "min-date": "2026-01-01",
        "max-date": "2026-12-31",
    }

    progress = resolve(Progress(label="Upload", value=25, max=50).to_node(), DESIGN)
    assert _props(progress) == {"accessible-name": "Upload", "value": 50.0}
    default_progress = resolve(Progress(label="Upload", value=0.5).to_node(), DESIGN)
    assert _props(default_progress) == {"accessible-name": "Upload", "value": 50.0}
    neutral_alert = resolve(Alert("Notice", intent="neutral").to_node(), DESIGN)
    assert _props(neutral_alert)["design"] == "Information"


def test_choices_switch_and_dialog_keep_ui5_state_contracts():
    select = _find(resolve(Select(label="Plan", options=["a", {"value": 2, "label": "Two"}], value=2).to_node(), DESIGN), "ui5-select")
    assert select["bindings"]["value"] == {
        "compute": {"expr": "lit", "value": 2},
        "mode": "one-way",
        "defer": True,
        "codec": "json",
    }
    assert [(option["tag"], _props(option)) for option in select["slots"]["default"]] == [
        ("ui5-option", {"value": '"a"', "textContent": "a"}),
        ("ui5-option", {"value": "2", "selected": True, "textContent": "Two"}),
    ]

    switch = _find(resolve(ToggleSwitch(label="Dark").bind("value", "dark", mode="two-way").to_node(), DESIGN), "ui5-switch")
    assert switch["bindings"]["checked"] == {"field": "dark", "mode": "two-way"}

    dialog = resolve(Dialog(label="Confirm").bind("open", "open", mode="two-way").to_node(), DESIGN)
    assert dialog["tag"] == "ui5-dialog"
    assert _props(dialog) == {"header-text": "Confirm"}
    assert dialog["bindings"] == {"open": {"field": "open", "mode": "two-way", "event": "close"}}


def test_the_conformance_page_only_falls_back_for_radio_group():
    node = resolve(conformance.page().to_node(), DESIGN)
    validate(node)
    rendered = json.dumps(node)
    assert '"tag": "ui-' not in rendered
    assert rendered.count("data-ui-fallback") == 1
