# app/services/bike_routing.py
import asyncio
import httpx

# Cache simple en memoria
OSM_TAGS_CACHE = {}

async def fetch_osm_tags_async(lat, lon):
    """
    Consulta Overpass de forma asíncrona y cachea resultados.
    """
    key = (round(lat, 5), round(lon, 5))  # redondeamos para cache
    if key in OSM_TAGS_CACHE:
        return OSM_TAGS_CACHE[key]

    query = f"""
    [out:json];
    (
      way(around:10,{lat},{lon});
    );
    out tags center;
    """
    url = "https://overpass-api.de/api/interpreter"

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            res = await client.get(url, params={"data": query})
            res.raise_for_status()
            data = res.json()
            if not data.get("elements"):
                tags = {}
            else:
                tags = data["elements"][0].get("tags", {})
            OSM_TAGS_CACHE[key] = tags
            return tags
    except Exception:
        return {}  # fallback rápido

async def calculate_bike_safety_index_step_async(step):
    """
    Calcula un índice de seguridad para un step usando información de OSM de forma asíncrona.
    """
    lat, lon = step["geometry"]["coordinates"][0][1], step["geometry"]["coordinates"][0][0]
    tags = await fetch_osm_tags_async(lat, lon)
    print('tags', tags)

    score = 1.0
    highway = tags.get("highway", "")
    if highway in ["motorway", "trunk"]:
        score *= 0.1
    elif highway == "primary":
        score *= 0.4
    elif highway == "secondary":
        score *= 0.7

    surface = tags.get("surface", "paved")
    if surface in ["unpaved", "gravel", "dirt"]:
        score *= 0.7

    cycleway = tags.get("cycleway")
    shoulder = tags.get("shoulder")
    if cycleway in ["lane", "track"] or shoulder == "yes":
        score *= 1.0
    else:
        score *= 0.8

    return score

# async def calculate_bike_safety_index_async(route):
#     """
#     Calcula el índice de seguridad ponderado por distancia de forma asíncrona para toda la ruta.
#     """
#     tasks = []
#     distances = []
#     print('legs', len(route.get("legs", [])))
#     for leg in route.get("legs", []):
#         print('steps', len(leg.get("steps", [])))
#         for step in leg.get("steps", []):
#             tasks.append(calculate_bike_safety_index_step_async(step))
#             distances.append(step.get("distance", 0))

#     if not tasks:
#         return 0.5

#     scores = await asyncio.gather(*tasks)
#     weighted_score = sum(s * d for s, d in zip(scores, distances))
#     total_distance = sum(distances)
#     return round(weighted_score / total_distance, 2) if total_distance > 0 else 0.5

# Con cache
async def calculate_bike_safety_index_async(route):
    tasks = []
    distances = []
    local_cache = {}

    async def cached_step(step):
        lat, lon = step["geometry"]["coordinates"][0][1], step["geometry"]["coordinates"][0][0]

        key = (round(lat, 3), round(lon, 3))  # cache más amplia

        if key in local_cache:
            print("HIT CACHE:", key)
            return local_cache[key]

        print("MISS:", key)
        score = await calculate_bike_safety_index_step_async(step)
        local_cache[key] = score
        return score

    for leg in route.get("legs", []):
        for step in leg.get("steps", []):
            tasks.append(cached_step(step))
            distances.append(step.get("distance", 0))

    scores = await asyncio.gather(*tasks)

    weighted_score = sum(s * d for s, d in zip(scores, distances))
    total_distance = sum(distances)

    return round(weighted_score / total_distance, 2) if total_distance > 0 else 0.5

