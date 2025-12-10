import httpx
from app.core.config import OSRM_URL

async def get_osrm_routes(start, end):
    """
    start = (lat, lon)
    end   = (lat, lon)
    """
    url = f"{OSRM_URL}/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}"
    params = {
        "alternatives": "true",
        "geometries": "geojson",
        "steps": "true"
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
        r.raise_for_status()  # <-- Esto lanza error si OSRM no responde

    data = r.json()
    return data.get("routes", [])
