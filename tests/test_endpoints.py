import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DISCORD_API_SECRET", "test-secret")

from media_api.main import app  # noqa: E402

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


def test_playlist_requires_auth():
    r = client.get("/media/playlist?url=https://www.youtube.com/playlist?list=PL123")
    assert r.status_code == 403


def test_playlist_missing_url():
    r = client.get("/media/playlist", headers=AUTH)
    assert r.status_code == 422


def test_playlist_rejects_spotify_track():
    r = client.get(
        "/media/playlist?url=https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh",
        headers=AUTH,
    )
    assert r.status_code == 400


def test_playlist_rejects_plain_youtube_url():
    r = client.get(
        "/media/playlist?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        headers=AUTH,
    )
    assert r.status_code == 400
