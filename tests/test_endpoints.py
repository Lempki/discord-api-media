import pytest
from fastapi.testclient import TestClient

from media_api.main import app
from media_api.config import get_settings, Settings


def _override_settings():
    return Settings(discord_api_secret="test-secret")


app.dependency_overrides[get_settings] = _override_settings

client = TestClient(app)
AUTH = {"Authorization": "Bearer test-secret"}


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_info_requires_auth():
    r = client.get("/media/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert r.status_code == 403


def test_info_missing_params():
    r = client.get("/media/info", headers=AUTH)
    assert r.status_code == 400


def test_info_conflicting_params():
    r = client.get("/media/info?url=https://x.com&query=test", headers=AUTH)
    assert r.status_code == 400


def test_search_requires_auth():
    r = client.post("/media/search", json={"query": "test"})
    assert r.status_code == 403
