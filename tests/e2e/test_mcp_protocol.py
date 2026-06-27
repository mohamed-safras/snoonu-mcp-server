import asyncio
import json

import pytest

from tests.e2e.conftest import mcp_session, call_mcp_tool

pytestmark = pytest.mark.e2e


def _json(result):
    assert result.isError is False, result.content
    return json.loads(result.content[0].text)


def test_initialize_and_list_tools(base_url):
    async def run():
        async with mcp_session(base_url) as session:
            tools = await session.list_tools()
            return [t.name for t in tools.tools]

    names = asyncio.run(run())
    assert set(names) == {
        "snoonu_search_products",
        "snoonu_get_product",
        "snoonu_list_categories",
        "snoonu_list_delivery_cities",
        "snoonu_check_delivery",
        "snoonu_create_order",
        "snoonu_track_order",
    }


def test_list_categories_returns_seeded_categories(base_url):
    out = _json(call_mcp_tool(base_url, "snoonu_list_categories", {"depth": 1}))
    assert len(out["categories"]) > 0


def test_search_products_finds_seeded_item(base_url):
    out = _json(call_mcp_tool(base_url, "snoonu_search_products", {"q": "rose", "limit": 5}))
    assert len(out["results"]) > 0


def test_list_delivery_cities_finds_doha(base_url):
    out = _json(call_mcp_tool(base_url, "snoonu_list_delivery_cities", {"query": "Doha"}))
    assert any(c["name"] == "Doha" for c in out["cities"])


def test_check_delivery_known_city(base_url):
    out = _json(call_mcp_tool(base_url, "snoonu_check_delivery", {"city": "Doha"}))
    assert out["available"] is True


def test_create_and_track_order_roundtrip(base_url):
    search = _json(call_mcp_tool(base_url, "snoonu_search_products", {"q": "rose", "limit": 1}))
    assert search["results"], "seed data must contain at least one product matching 'rose'"
    product_id = search["results"][0]["id"]

    created = _json(call_mcp_tool(base_url, "snoonu_create_order", {
        "cart": [{"product_id": product_id, "quantity": 1}],
        "recipient": {"name": "E2E Test"},
        "delivery": {"city": "Doha"},
        "sender": {"name": "E2E Test"},
    }))
    assert created["order_ref"].startswith("SNU-")

    tracked = _json(call_mcp_tool(base_url, "snoonu_track_order", {"order_number": created["order_ref"]}))
    assert tracked["status"] != "not_found"
