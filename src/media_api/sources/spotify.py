import re

from ..config import Settings
from ..extractor import fetch_info, search

_TRACK_RE = re.compile(r"spotify\.com/track/")


def is_spotify_url(url: str) -> bool:
    return "spotify.com" in url


async def get_info(url: str, settings: Settings) -> dict:
    # Spotify URLs aren't directly supported by yt-dlp.
    # Fall back to a YouTube search using the track title extracted from the URL path.
    # For accurate metadata, integrate the Spotify public API and use the track name + artist.
    track_id = url.rstrip("/").split("/")[-1].split("?")[0]
    search_query = f"spotify track {track_id}"
    results = await search(search_query, "youtube", 1, settings)
    if not results:
        raise ValueError(f"Could not resolve Spotify URL: {url}")
    return await fetch_info(results[0]["webpage_url"], settings)
