import asyncio
import os
from contextlib import asynccontextmanager

import pytest
import requests
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

BASE_URL = os.environ.get("SNOONU_E2E_URL", "http://localhost:8000")


@asynccontextmanager
async def mcp_session(base_url):
    async with streamable_http_client(f"{base_url}/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


def call_mcp_tool(base_url: str, name: str, arguments: dict):
    """Open a fresh MCP session, call one tool, and return the raw CallToolResult."""
    async def run():
        async with mcp_session(base_url) as session:
            return await session.call_tool(name, arguments)
    return asyncio.run(run())


@pytest.fixture(scope="session", autouse=True)
def _require_live_server():
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=2)
        r.raise_for_status()
    except Exception as exc:
        pytest.skip(f"No live server reachable at {BASE_URL} ({exc}). Run `docker compose up -d` first.")


@pytest.fixture
def base_url():
    return BASE_URL
