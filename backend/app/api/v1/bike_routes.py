from fastapi import APIRouter, Query
from typing import List
from app.services.osrm_service import get_osrm_routes

router = APIRouter(tags=["routes"])

@router.get("/", summary="Obtener rutas entre dos puntos")
async def get_routes(start: str = Query(..., description="lat,lon"),
                     end: str = Query(..., description="lat,lon")):
    lat1, lon1 = map(float, start.split(","))
    lat2, lon2 = map(float, end.split(","))

    osrm_routes = await get_osrm_routes((lat1, lon1), (lat2, lon2))

    processed_routes = []
    for route in osrm_routes:
        processed_routes.append({
            "distance": route["distance"],
            "duration": route["duration"],
            "geometry": route["geometry"],
            "safety_index": 0.7  # placeholder, luego puedes mejorar
        })

    return processed_routes
