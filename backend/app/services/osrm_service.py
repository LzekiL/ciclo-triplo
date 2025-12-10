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
    url = f"{OSRM_URL}/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}"

    params = {
        "alternatives": "true",
        "geometries": "geojson",
        "steps": "true"
    }

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            data = r.json()

    except Exception as e:
        print("❌ Error al conectar con OSRM:", e)
        return []

    routes = data.get("routes", [])
    print("OSRM devolvió rutas:", len(routes))


    # Si OSRM no devuelve nada
    if not routes:
        return []

    # Normalizamos rutas
    normalized = [normalize_route(r, idx) for idx, r in enumerate(routes)]

    # Si solo hay una ruta → generamos una alternativa artificial
    if len(normalized) == 1:
        alt_route = normalized[0].copy()
        alt_route["id"] = 1
        alt_route["distance"] *= 1.04  # +4% distancia
        alt_route["duration"] *= 1.05  # +5% tiempo
        normalized.append(alt_route)

    # Maximum 3 routes
    return normalized[:3]
