import pytest
import requests

pytestmark = pytest.mark.e2e


def test_health(base_url):
    r = requests.get(f"{base_url}/health", timeout=5)
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_ready(base_url):
    r = requests.get(f"{base_url}/ready", timeout=5)
    assert r.status_code == 200
    assert r.json()["status"] == "ready"


def test_metrics(base_url):
    r = requests.get(f"{base_url}/metrics", timeout=5)
    assert r.status_code == 200
    assert "snoonu_mcp_requests_total" in r.text


def test_request_id_header_present(base_url):
    r = requests.get(f"{base_url}/health", timeout=5)
    assert "x-request-id" in r.headers
