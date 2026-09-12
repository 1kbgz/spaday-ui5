import asyncio
import re

import httpx

from spaday_ui5 import gallery, package


def _tags(value):
    if isinstance(value, dict):
        if isinstance(value.get("tag"), str):
            yield value["tag"]
        for child in value.values():
            yield from _tags(child)
    elif isinstance(value, list):
        for child in value:
            yield from _tags(child)


def test_gallery_shows_every_generated_component_with_a_snippet():
    expected_names = set(gallery.COMPONENT_NAMES)
    expected_tags = {schema.tag for schema in package.catalog}
    gallery_tags = {tag for tag in _tags(gallery.page.to_node()) if tag.startswith("ui5-")}
    snippet_names = set(re.findall(r"\bUi5[A-Z][A-Za-z]+\b", "\n".join(gallery.COMPONENT_SNIPPETS)))

    assert gallery_tags == expected_tags
    assert snippet_names == expected_names


def test_python_snippets_highlight_each_token_kind():
    node = gallery._code('from ui import card\ncount = 3\nlabel = "Ready"  # status\n').to_node()
    children = node["slots"]["default"][0]["slots"]["default"]
    classes = {child.get("props", {}).get("class", {}).get("Str") for child in children}

    assert {"token-keyword", "token-string", "token-number", "token-comment", "token-operator"} <= classes


def test_gallery_app_serves_the_component_tree():
    async def request():
        transport = httpx.ASGITransport(app=gallery.app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get("/tree.json")

    response = asyncio.run(request())
    assert response.status_code == 200
    assert "ui5-yearrangepicker" in response.text
