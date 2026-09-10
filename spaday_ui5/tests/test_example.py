import asyncio

import httpx
import pytest

from spaday_ui5 import example


async def request(method: str, path: str, **kwargs):
    transport = httpx.ASGITransport(app=example.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://example") as client:
        return await client.request(method, path, **kwargs)


def run_ticks(monkeypatch, ticks: int):
    """Run the procurement stream for ``ticks`` iterations."""
    sleeps = 0

    class Done(Exception):
        pass

    async def sleep(_delay):
        nonlocal sleeps
        sleeps += 1
        if sleeps > ticks:
            raise Done

    monkeypatch.setattr(example.asyncio, "sleep", sleep)
    with pytest.raises(Done):
        asyncio.run(example.stream_procurement())


def test_example_serves_the_cockpit():
    response = asyncio.run(request("GET", "/tree.json"))
    assert response.status_code == 200
    for tag in ("ui5-table", "ui5-tabcontainer", "ui5-form", "ui5-dialog", "ui5-toast", "spa-each"):
        assert tag in response.text


def test_stream_moves_suppliers_and_brings_requisitions(monkeypatch):
    before = {key: row["on_time"] for key, row in example.feed.suppliers.items()}
    arriving = f"PR-{example.next_number()}"
    run_ticks(monkeypatch, 3)
    assert {key: row["on_time"] for key, row in example.feed.suppliers.items()} != before
    # every third tick a requisition arrives, newest first
    assert (example.feed.requisitions[0]["id"], example.feed.requisitions[0]["status"]) == (arriving, "Pending")
    assert example.feed.pending == str(sum(row["status"] == "Pending" for row in example.feed.requisitions))


def test_submitting_a_requisition_queues_it_for_approval():
    response = asyncio.run(
        request(
            "POST",
            "/api/requisitions",
            json={
                "title": "Monitors",
                "cost_center": "CC-300",
                "amount": 1800,
                "needed_by": "2026-10-01",
                "supplier": "Acme Components",
                "preferred": False,
            },
        )
    )
    assert response.status_code == 200
    row = example.feed.requisitions[0]
    assert (row["title"], row["cost_center"], row["amount_label"], row["status"]) == ("Monitors", "CC-300 · Marketing", "$1,800", "Pending")
    assert response.json()["message"] == f"{row['id']} for $1,800 from Acme Components, needed by 2026-10-01, is awaiting approval."
    assert asyncio.run(request("POST", "/api/requisitions", json={"title": "", "amount": 0})).status_code == 422


def test_approving_spends_budget_and_rejecting_does_not():
    first, second = [row for row in example.feed.requisitions if row["status"] == "Pending"][:2]
    spent = example.feed.spent
    approved = asyncio.run(request("POST", f"/api/requisitions/{first['id']}/approve"))
    assert approved.json()["message"] == f"Approved {first['id']}: {first['title']} ({first['amount_label']})"
    assert example.feed.spent == spent + first["amount"]
    rejected = asyncio.run(request("POST", f"/api/requisitions/{second['id']}/reject"))
    assert rejected.status_code == 200 and example.feed.spent == spent + first["amount"]
    statuses = {row["id"]: (row["status"], row["design"]) for row in example.feed.requisitions}
    assert statuses[first["id"]] == ("Approved", "Positive") and statuses[second["id"]] == ("Rejected", "Negative")
    # a decided requisition can't be decided again
    assert asyncio.run(request("POST", f"/api/requisitions/{first['id']}/reject")).status_code == 409
