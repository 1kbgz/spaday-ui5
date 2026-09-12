import asyncio
import logging
from datetime import date, timedelta

import transports
import uvicorn
from pydantic import BaseModel
from spaday import CallEndpoint, Sequence, SetProp, by_id, concat, element, eq, field, item, not_, obj
from spaday.backends.starlette import serve
from spaday.components.shell import App, Body, Each, Main, Nav, Row
from starlette.responses import JSONResponse
from starlette.routing import Route, WebSocketRoute

from spaday_ui5 import (
    Ui5Avatar,
    Ui5Bar,
    Ui5Button,
    Ui5Card,
    Ui5CardHeader,
    Ui5CbItem,
    Ui5Checkbox,
    Ui5Combobox,
    Ui5DatePicker,
    Ui5Dialog,
    Ui5Form,
    Ui5FormItem,
    Ui5Input,
    Ui5Label,
    Ui5MessageStrip,
    Ui5Option,
    Ui5ProgressIndicator,
    Ui5RatingIndicator,
    Ui5Select,
    Ui5StepInput,
    Ui5Switch,
    Ui5Tab,
    Ui5Tabcontainer,
    Ui5Table,
    Ui5TableCell,
    Ui5TableHeaderCell,
    Ui5TableHeaderRow,
    Ui5TableRow,
    Ui5Tag,
    Ui5Text,
    Ui5Textarea,
    Ui5Title,
    Ui5Toast,
    package,
)

logger = logging.getLogger("uvicorn.error")

BUDGET = 600_000
TODAY = date(2026, 9, 14)
COST_CENTERS = {"CC-100": "Engineering", "CC-200": "Operations", "CC-300": "Marketing"}
DESIGN = {"Pending": "Information", "Approved": "Positive", "Rejected": "Negative"}
SUPPLIERS = {
    "acme": {"name": "Acme Components", "category": "Hardware", "on_time": 96},
    "globex": {"name": "Globex Logistics", "category": "Freight", "on_time": 88},
    "initech": {"name": "Initech Software", "category": "Licenses", "on_time": 99},
    "umbrella": {"name": "Umbrella Facilities", "category": "Services", "on_time": 81},
}
# how each supplier's on-time rate moves tick by tick
DRIFT = (2, -1, 1, -3, 1)
INCOMING = [
    ("Standing desks for the new floor", "Priya Raman", "CC-200", 18_400),
    ("Load-testing cluster time", "Jonas Weber", "CC-100", 7_250),
    ("Trade show booth", "Amara Okafor", "CC-300", 23_900),
    ("Replacement laptops", "Chen Li", "CC-100", 31_600),
]


def requisition(number: int, title: str, requester: str, cost_center: str, amount: float, status: str = "Pending") -> dict:
    return {
        "id": f"PR-{number}",
        "title": title,
        "requester": requester,
        "initials": "".join(part[0] for part in requester.split()[:2]),
        "cost_center": f"{cost_center} · {COST_CENTERS[cost_center]}",
        "amount": amount,
        "amount_label": f"${amount:,.0f}",
        "status": status,
        "design": DESIGN[status],
    }


def supplier_row(values: dict) -> dict:
    on_time = values["on_time"]
    status = "Preferred" if on_time >= 95 else "Watch" if on_time < 85 else "Approved"
    return {
        **values,
        "rating": max(1, min(5, round((on_time - 70) / 6))),
        "on_time_label": f"{on_time}%",
        "status": status,
        "design": {"Preferred": "Positive", "Watch": "Critical"}.get(status, "Information"),
    }


class ProcurementFeed(BaseModel):
    requisitions: list[dict] = [
        requisition(4101, "GPU workstations", "Chen Li", "CC-100", 42_800),
        requisition(4102, "Warehouse scanners", "Priya Raman", "CC-200", 9_600),
        requisition(4103, "Campaign photography", "Amara Okafor", "CC-300", 12_300),
        requisition(4100, "Office chairs", "Jonas Weber", "CC-200", 6_900, "Approved"),
    ]
    suppliers: dict[str, dict] = {key: supplier_row(values) for key, values in SUPPLIERS.items()}
    spent: float = 412_000
    budget_used: int = 0
    budget_label: str = ""
    budget_state: str = "None"
    pending: str = ""
    avg_rating: float = 0


feed = ProcurementFeed()
session = transports.Session()
session.host(feed)
server = transports.Server(session)


def refresh_totals() -> None:
    feed.budget_used = round(feed.spent / BUDGET * 100)
    feed.budget_label = f"${feed.spent:,.0f} of ${BUDGET:,.0f}"
    feed.budget_state = "Negative" if feed.budget_used >= 90 else "Critical" if feed.budget_used >= 75 else "Positive"
    feed.pending = str(sum(row["status"] == "Pending" for row in feed.requisitions))
    feed.avg_rating = round(sum(row["rating"] for row in feed.suppliers.values()) / len(feed.suppliers), 2)


refresh_totals()


def next_number() -> int:
    return max(int(row["id"].removeprefix("PR-")) for row in feed.requisitions) + 1


def add_requisition(row: dict) -> None:
    """Newest first; past eight rows the oldest decided one drops off."""
    rows = [row, *feed.requisitions]
    decided = [existing for existing in rows if existing["status"] != "Pending"]
    if len(rows) > 8 and decided:
        rows.remove(decided[-1])
    feed.requisitions = rows


async def stream_procurement() -> None:
    """Supplier performance drifts every tick, and every third tick a new requisition arrives."""
    tick = 0
    while True:
        await asyncio.sleep(2)
        tick += 1
        suppliers = {}
        for index, (key, row) in enumerate(feed.suppliers.items()):
            on_time = max(70, min(100, row["on_time"] + DRIFT[(tick + index) % len(DRIFT)]))
            suppliers[key] = supplier_row({**SUPPLIERS[key], "on_time": on_time})
        feed.suppliers = suppliers
        if tick % 3 == 0:
            title, requester, cost_center, amount = INCOMING[(tick // 3) % len(INCOMING)]
            add_requisition(requisition(next_number(), title, requester, cost_center, amount))
        refresh_totals()


async def create_requisition(request):
    body = await request.json()
    logger.info("Requisition from browser: %s", body)
    title = (body.get("title") or "").strip()
    amount = float(body.get("amount") or 0)
    if not title or amount <= 0:
        return JSONResponse({"message": "A requisition needs a title and an amount above zero."}, status_code=422)
    row = requisition(next_number(), title, "You", body.get("cost_center") or "CC-100", amount)
    add_requisition(row)
    refresh_totals()
    supplier = body.get("supplier") or "any supplier"
    preferred = " (preferred suppliers only)" if body.get("preferred") else ""
    return JSONResponse(
        {"message": f"{row['id']} for {row['amount_label']} from {supplier}{preferred}, needed by {body.get('needed_by')}, is awaiting approval."}
    )


async def decide(request):
    decision = request.path_params["decision"]
    status = {"approve": "Approved", "reject": "Rejected"}[decision]
    target = request.path_params["id"]
    row = next((row for row in feed.requisitions if row["id"] == target), None)
    if row is None or row["status"] != "Pending":
        return JSONResponse({"message": f"{target} is no longer pending."}, status_code=409)
    feed.requisitions = [{**existing, "status": status, "design": DESIGN[status]} if existing is row else existing for existing in feed.requisitions]
    if status == "Approved":
        feed.spent += row["amount"]
    refresh_totals()
    return JSONResponse({"message": f"{status} {target}: {row['title']} ({row['amount_label']})"})


def card(title: str, subtitle: str, *body, additional_field: str | None = None):
    header = Ui5CardHeader(title_text=title, subtitle_text=subtitle)
    if additional_field:
        header = header.bind("additional-text", additional_field)
    return Ui5Card(element("div", *body, class_="card-body")).child_in("header", header)


kpis = Row(
    card(
        "Budget used",
        "Q3 · all cost centers",
        Ui5ProgressIndicator(id="budget").bind("value", "budget_used").bind("value-state", "budget_state"),
        element("span", class_="caption").bind("textContent", "budget_label"),
    ),
    card(
        "Awaiting approval",
        "Requisitions",
        element("strong", id="pending", class_="figure").bind("textContent", "pending"),
        Ui5Tag(design="Information").text("Live from Python"),
    ),
    card(
        "Supplier rating",
        "Average across suppliers",
        Ui5RatingIndicator(readonly=True).bind("value", "avg_rating"),
        element("span", class_="caption").text("From on-time delivery, updated every two seconds"),
    ),
    gap="1rem",
    align="stretch",
    class_="kpis",
)

approvals = Each(
    element(
        "div",
        Ui5Avatar(size="S", color_scheme="Accent6").compute("initials", item("initials")),
        element(
            "div",
            Ui5Title(level="H5").compute("textContent", concat(item("id"), " · ", item("title"))),
            Ui5Text().compute("textContent", concat(item("requester"), " · ", item("cost_center"))),
            class_="req-main",
        ),
        element("strong", class_="req-amount").compute("textContent", item("amount_label")),
        Ui5Tag().compute("design", item("design")).compute("textContent", item("status")),
        element(
            "div",
            Ui5Button(design="Positive", icon="accept", accessible_name="Approve")
            .text("Approve")
            .compute("disabled", not_(eq(item("status"), "Pending")))
            .on(
                "click",
                Sequence(
                    CallEndpoint("POST", concat("/api/requisitions/", item("id"), "/approve"), result="decision"),
                    SetProp(by_id("toast"), "open", True),
                ),
            ),
            Ui5Button(design="Transparent", icon="decline", accessible_name="Reject")
            .compute("disabled", not_(eq(item("status"), "Pending")))
            .on(
                "click",
                Sequence(
                    CallEndpoint("POST", concat("/api/requisitions/", item("id"), "/reject"), result="decision"),
                    SetProp(by_id("toast"), "open", True),
                ),
            ),
            class_="req-actions",
        ),
        class_="req",
    ).compute("data-id", item("id")),
    field="requisitions",
    key="id",
)

suppliers = Ui5Table(
    *(
        Ui5TableRow(
            Ui5TableCell().bind("textContent", f"suppliers.{key}.name"),
            Ui5TableCell().bind("textContent", f"suppliers.{key}.category"),
            Ui5TableCell(Ui5RatingIndicator(readonly=True, size="S").bind("value", f"suppliers.{key}.rating")),
            Ui5TableCell(Ui5ProgressIndicator().bind("value", f"suppliers.{key}.on_time").bind("display-value", f"suppliers.{key}.on_time_label")),
            Ui5TableCell(Ui5Tag().bind("design", f"suppliers.{key}.design").bind("textContent", f"suppliers.{key}.status")),
            row_key=key,
        )
        for key in SUPPLIERS
    ),
    id="suppliers",
    alternate_row_colors=True,
    overflow_mode="Popin",
).child_in(
    "headerRow",
    Ui5TableHeaderRow(
        Ui5TableHeaderCell(min_width="12rem").text("Supplier"),
        Ui5TableHeaderCell().text("Category"),
        Ui5TableHeaderCell().text("Rating"),
        Ui5TableHeaderCell(min_width="10rem").text("On time"),
        Ui5TableHeaderCell().text("Status"),
    ),
)


def form_item(label: str, control):
    return Ui5FormItem(control).child_in("labelContent", Ui5Label(show_colon=True).text(label))


request_form = element(
    "section",
    Ui5Form(
        form_item("Title", Ui5Input(id="title", placeholder="What do you need?").bind("value", "title", mode="two-way")),
        form_item(
            "Cost center",
            Ui5Select(*(Ui5Option(value=code).text(f"{code} · {name}") for code, name in COST_CENTERS.items())).bind(
                "value", "cost_center", mode="two-way"
            ),
        ),
        form_item("Amount (USD)", Ui5StepInput(min=0, step=250).bind("value", "amount", mode="two-way")),
        form_item(
            "Needed by",
            Ui5DatePicker(value_format="yyyy-MM-dd", min_date=TODAY.isoformat()).bind("value", "needed_by", mode="two-way"),
        ),
        form_item(
            "Supplier",
            Ui5Combobox(*(Ui5CbItem(text=row["name"]) for row in SUPPLIERS.values()), show_clear_icon=True).bind("value", "supplier", mode="two-way"),
        ),
        form_item("Sourcing", Ui5Checkbox(text="Preferred suppliers only").bind("checked", "preferred", mode="two-way")),
        form_item("Justification", Ui5Textarea(rows=3, growing=True).bind("value", "justification", mode="two-way")),
        header_text="Purchase requisition",
        layout="S1 M2 L2 XL2",
    ),
    Ui5Bar(design="Footer").child_in(
        "endContent",
        Ui5Button(id="submit", design="Emphasized", icon="add")
        .text("Submit requisition")
        .on(
            "click",
            Sequence(
                CallEndpoint(
                    "POST",
                    "/api/requisitions",
                    obj(
                        {
                            "title": field("title"),
                            "cost_center": field("cost_center"),
                            "amount": field("amount"),
                            "needed_by": field("needed_by"),
                            "supplier": field("supplier"),
                            "preferred": field("preferred"),
                            "justification": field("justification"),
                        }
                    ),
                    result="created",
                ),
                SetProp(by_id("submitted"), "open", True),
            ),
        ),
    ),
    class_="request",
)

submitted = Ui5Dialog(
    Ui5Text(id="submitted-message").compute("textContent", field("created.body.message")),
    id="submitted",
    header_text="Requisition submitted",
    state="Positive",
).child_in(
    "footer",
    Ui5Bar(design="Footer").child_in(
        "endContent",
        Ui5Button(design="Emphasized")
        .text("Review approvals")
        .on(
            "click",
            # a tab container does not deselect the other tabs for you
            Sequence(
                SetProp(by_id("submitted"), "open", False),
                SetProp(by_id("request-tab"), "selected", False),
                SetProp(by_id("approvals-tab"), "selected", True),
            ),
        ),
    ),
)

hero = element(
    "section",
    element("span", class_="eyebrow").text("UI5 OPERATIONS · PROCUREMENT"),
    element("h1").text("Control spend without slowing teams"),
    element("p", class_="hero-copy").text("Live approvals, supplier health and purchase requests share one typed Python workflow."),
    element(
        "div",
        Ui5Tag(design="Positive").text("125 typed elements"),
        Ui5Tag(design="Information").text("Live supplier feed"),
        Ui5Tag(design="Set1").text("Python decisions"),
        class_="hero-tags",
    ),
    class_="hero",
)

page = App(
    Nav(
        Ui5Title(level="H4").text("Procurement cockpit"),
        element(
            "label",
            Ui5Label(for_="dark").text("Dark theme"),
            Ui5Switch(id="dark", accessible_name="Dark theme").bind("checked", "dark", mode="two-way"),
            class_="dark-toggle",
        ),
    ),
    Body(
        Main(
            hero,
            Ui5MessageStrip(design="Information", hide_close_button=True).text(
                "Budgets, approvals and supplier performance stream from Python; every control is a typed UI5 Web Component."
            ),
            kpis,
            Ui5Tabcontainer(
                Ui5Tab(element("div", approvals, id="approvals", class_="approvals"), id="approvals-tab", text="Approvals", selected=True).bind(
                    "additional-text", "pending"
                ),
                Ui5Tab(suppliers, text="Suppliers"),
                Ui5Tab(request_form, id="request-tab", text="New request"),
                content_background_design="Transparent",
                tab_layout="Inline",
            ),
            submitted,
            Ui5Toast(id="toast", placement="BottomEnd").compute("textContent", field("decision.body.message")),
            class_="page",
        ),
    ),
).bind_root_class("wa-dark", "dark")

styles = """
<style>
  * { box-sizing: border-box; }
  body { margin: 0; font-family: var(--sapFontFamily); color: var(--sapTextColor);
    background: radial-gradient(circle at 12% 0%, color-mix(in srgb, var(--sapBrandColor) 13%, transparent), transparent 32rem),
      var(--sapBackgroundColor); }
  spa-nav { position: sticky; z-index: 20; top: 0; justify-content: space-between; border-bottom: 1px solid var(--spa-border);
    background: var(--sapBaseColor); }
  .dark-toggle { display: inline-flex; align-items: center; gap: .5rem; }
  .page { box-sizing: border-box; width: 100%; max-width: 76rem; margin: 0 auto; padding: 1.5rem 1rem;
    display: grid; align-content: start; gap: 1rem; }
  .hero { overflow: hidden; padding: clamp(1.5rem, 5vw, 3.5rem); border: 1px solid color-mix(in srgb, var(--sapBrandColor) 24%, var(--spa-border));
    border-radius: 1.25rem; color: white; background: linear-gradient(125deg, #063b62 0%, #075f8f 54%, #0b75b7 100%);
    box-shadow: 0 1.5rem 3rem color-mix(in srgb, #063b62 20%, transparent); }
  .eyebrow { display: block; margin-bottom: .75rem; font-size: .75rem; font-weight: 700; letter-spacing: .12em; opacity: .76; }
  .hero h1 { max-width: 15ch; margin: 0; font: 700 clamp(2rem, 5vw, 3.5rem)/1.02 var(--sapFontHeaderFamily); letter-spacing: -.035em; }
  .hero-copy { max-width: 42rem; margin: 1rem 0 1.25rem; font-size: clamp(1rem, 2vw, 1.2rem); line-height: 1.55; opacity: .88; }
  .hero-tags { display: flex; flex-wrap: wrap; gap: .5rem; }
  .kpis { flex-wrap: wrap; }
  .kpis ui5-card { flex: 1 1 16rem; min-width: 0; border-radius: 1rem; box-shadow: 0 .5rem 1.5rem color-mix(in srgb, #001b2e 8%, transparent); }
  .card-body { display: grid; gap: .5rem; padding: 0 1rem 1rem; }
  .caption { color: var(--sapContent_LabelColor); font-size: var(--sapFontSmallSize); }
  .figure { font-size: 2.25rem; font-family: var(--sapFontHeaderFamily); color: var(--sapTile_TitleTextColor, var(--sapTextColor)); }
  .card-body ui5-tag { justify-self: start; }
  .approvals { display: grid; gap: .5rem; }
  .req { display: grid; grid-template-columns: auto 1fr auto auto auto; align-items: center; gap: 1rem; padding: .75rem 1rem;
    border: 1px solid var(--spa-border); border-radius: var(--sapElement_BorderCornerRadius); background: var(--spa-surface); }
  .req-main { display: grid; gap: .15rem; min-width: 0; }
  .req-amount { font-variant-numeric: tabular-nums; }
  .req-actions { display: flex; gap: .25rem; }
  .request { display: grid; gap: .5rem; }
  @media (max-width: 720px) {
    spa-nav { position: static; flex-wrap: wrap; gap: .75rem; }
    .page { padding: .75rem; }
    .hero { border-radius: 1rem; }
    .req { grid-template-columns: auto 1fr; }
    .req-amount, .req ui5-tag, .req-actions { grid-column: 2; justify-self: start; }
    .req-actions { flex-wrap: wrap; }
  }
</style>
"""

initial_store = {
    "dark": False,
    "title": "Ergonomic keyboards",
    "cost_center": "CC-100",
    "amount": 2_500,
    "needed_by": (TODAY + timedelta(days=14)).isoformat(),
    "supplier": "Acme Components",
    "preferred": True,
    "justification": "Replacing worn-out keyboards for the platform team.",
    "created": {"body": {"message": ""}},
    "decision": {"body": {"message": ""}},
}

app = serve(
    page,
    packages=[package],
    wire="transports",
    routes=[
        WebSocketRoute("/ws", transports.ws_endpoint(server)),
        Route("/api/requisitions", create_requisition, methods=["POST"]),
        Route("/api/requisitions/{id}/{decision:str}", decide, methods=["POST"]),
    ],
    background=[transports.autosync(server), stream_procurement()],
    store=initial_store,
    head=styles,
    title="spaday-ui5 example",
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8026)
