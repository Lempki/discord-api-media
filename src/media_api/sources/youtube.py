from ..config import Settings
from ..extractor import fetch_info, search


async def get_info(url: str, settings: Settings) -> dict:
    return await fetch_info(url, settings)


async def search_tracks(query: str, max_results: int, settings: Settings) -> list[dict]:
    return await search(query, "youtube", max_results, settings)
