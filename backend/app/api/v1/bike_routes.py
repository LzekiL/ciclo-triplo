# app/api/v1/bike_routes.py
from fastapi import APIRouter, Query
from app.services.osrm_service import get_osrm_routes
from app.services.bike_routing import calculate_bike_safety_index_async
import asyncio

router = APIRouter(tags=["routes"])

async def process_route(idx, route):
    """
    Procesa una ruta individual: calcula el índice de seguridad y devuelve el dict final.
    """
    safety_index = await calculate_bike_safety_index_async(route)
    return {
        "id": route.get("route_id", idx),
        "distance": route["distance"],
        "duration": route["duration"],
        "geometry": route["geometry"],
        "safety_index": safety_index
    }

@router.get("/", summary="Obtener rutas entre dos puntos")
async def get_routes(start: str = Query(..., description="lat,lon"),
                     end: str = Query(..., description="lat,lon")):

    # Convertir coordenadas a float
    lat1, lon1 = map(float, start.split(","))
    lat2, lon2 = map(float, end.split(","))

    # Obtener rutas desde OSRM
    osrm_routes = await get_osrm_routes((lat1, lon1), (lat2, lon2))

    # Procesar todas las rutas en paralelo
    processed_routes = await asyncio.gather(
        *[process_route(idx, route) for idx, route in enumerate(osrm_routes)]
    )

    return processed_routes
