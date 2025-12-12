import httpx
from app.core.config import OSRM_URL


def normalize_route(route, index=0):
    """
    Limpia y normaliza la estructura de una ruta de OSRM.
    """
    return {
        "id": index,
        "distance": route.get("distance"),
        "duration": route.get("duration"),
        "geometry": route.get("geometry"),  # GeoJSON
        "legs": route.get("legs", []),
        "weight": route.get("weight"),
        "weight_name": route.get("weight_name")
    }


async def get_osrm_routes(start, end):
    """
    Obtiene 1–3 rutas de OSRM.
    start = (lat, lon)
    end   = (lat, lon)
    """
    url = f"http://osrm-bike:5000/route/v1/bicycle/{start[1]},{start[0]};{end[1]},{end[0]}"
    params = {
        "alternatives": "true",
        "geometries": "geojson",
        "steps": "true",
        "overview": "full"
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            data = r.json()

    except Exception as e:
        print("❌ Error al conectar con OSRM:", e)
        return []

    routes = data.get("routes", [])
    print('routes en services', len(routes), routes)
    if not routes:
        return []

    normalized = [normalize_route(r, idx) for idx, r in enumerate(routes)]

    # Generar alternativa artificial si solo hay una ruta
    if len(normalized) == 1:
        alt_route = normalized[0].copy()
        alt_route["id"] = 1
        alt_route["distance"] *= 1.04
        alt_route["duration"] *= 1.05
        normalized.append(alt_route)

    return normalized[:3]
