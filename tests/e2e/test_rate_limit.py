"""Exercises the real Redis-backed order rate limiter end-to-end.

Skipped by default since it creates up to SNOONU_ORDER_MAX_PER_HOUR real orders and
consumes the shared hourly quota for an hour. Opt in with:
    RUN_RATE_LIMIT_E2E=1 pytest tests/e2e/test_rate_limit.py
"""
import json
import os

import pytest

from tests.e2e.conftest import call_mcp_tool

pytestmark = pytest.mark.e2e

CART_ARGS = {
    "cart": [{"product_id": "snu-00001", "quantity": 1}],
    "recipient": {"name": "Load Test"},
    "delivery": {"city": "Doha"},
    "sender": {"name": "Load Test"},
}


@pytest.mark.skipif(
    os.environ.get("RUN_RATE_LIMIT_E2E") != "1",
    reason="Consumes the real hourly order quota; opt in with RUN_RATE_LIMIT_E2E=1",
)
def test_order_rate_limit_eventually_rejects(base_url):
    max_per_hour = int(os.environ.get("SNOONU_ORDER_MAX_PER_HOUR", "25"))
    last_result = None
    for _ in range(max_per_hour + 1):
        last_result = call_mcp_tool(base_url, "snoonu_create_order", CART_ARGS)
        if last_result.isError:
            break

    assert last_result.isError is True
    assert "Too many orders" in last_result.content[0].text
