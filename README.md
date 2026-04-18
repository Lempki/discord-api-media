# discord-api-media

This is a REST API that centralizes media metadata resolution for Discord bots. It wraps [yt-dlp](https://github.com/yt-dlp/yt-dlp) to provide track information, stream URLs, and search results for YouTube and SoundCloud over HTTP. Bots call this API instead of bundling yt-dlp themselves, keeping their dependencies minimal and allowing media support to be updated in a single place. This project is based on the [discord-api-template](https://github.com/Lempki/discord-api-template) repository, which provides the core architecture.

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/media/info` | Resolve a URL or search query to full track metadata including a playable stream URL. |
| `POST` | `/media/search` | Search for tracks and return a list of results. Results do not include stream URLs; call `/media/info` after the user selects a result. |
| `GET` | `/health` | Returns the service name and version. Used for uptime monitoring. |

All endpoints except `/health` require a bearer token in the `Authorization` header.

### GET /media/info

Accepts either a `url` parameter or a `query` + `source` pair. Providing both is an error.

```
GET /media/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ
GET /media/info?query=rick+astley&source=youtube
```

Response fields include `title`, `duration_seconds`, `duration_formatted`, `uploader`, `thumbnail_url`, `webpage_url`, `stream_url`, `stream_url_expires_at`, and `is_live`.

Stream URLs from YouTube expire after a short time. The API caches them for five minutes. Metadata is cached for one hour.

### POST /media/search

```json
{
  "query": "lofi hip hop",
  "source": "youtube",
  "max_results": 5
}
```

Supported sources are `youtube` and `soundcloud`. Spotify URLs passed to `/media/info` are resolved by converting them to a YouTube search.

## Prerequisites

* [Docker](https://docs.docker.com/get-docker/) and Docker Compose.

Running without Docker requires Python 3.12 or newer, and FFmpeg available in the system PATH.

## Setup

Copy the environment template and fill in the required values:

```bash
cp .env.example .env
```

Start the service:

```bash
docker-compose up --build
```

The API listens on port `8001` by default.

To run without Docker:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
uvicorn media_api.main:app --port 8001
```

## Configuration

All configuration is read from environment variables or from a `.env` file in the project root.

| Variable | Required | Default | Description |
|---|---|---|---|
| `DISCORD_API_SECRET` | Yes | — | Shared bearer token. All Discord bots must send this value in the `Authorization` header. |
| `LOG_LEVEL` | No | `INFO` | Log verbosity. Accepts standard Python logging levels. |
| `METADATA_CACHE_TTL` | No | `3600` | How long to cache track metadata in seconds. |
| `STREAM_URL_CACHE_TTL` | No | `300` | How long to cache stream URLs in seconds. YouTube URLs expire, so keep this value short. |
| `YDL_FORMAT` | No | `bestaudio/best` | The yt-dlp format selector used when extracting stream URLs. |
| `MAX_SEARCH_RESULTS` | No | `10` | Upper limit on results returned by `/media/search`. |

## Project structure

```
discord-api-media/
├── src/media_api/
│   ├── main.py         # FastAPI application and route definitions.
│   ├── config.py       # Environment variable reader.
│   ├── auth.py         # Bearer token dependency.
│   ├── models.py       # Pydantic request and response models.
│   ├── extractor.py    # yt-dlp wrapper with asyncio.to_thread and TTL caching.
│   ├── cache.py        # Metadata and stream URL TTL caches.
│   └── sources/        # Per-source helpers for YouTube, SoundCloud, and Spotify.
├── tests/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── .env.example
```
