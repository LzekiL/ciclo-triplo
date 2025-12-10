from fastapi import APIRouter, Query
from app.services.osrm_service import get_osrm_routes
from app.services.bike_routing import calculate_bike_safety_index

router = APIRouter(tags=["routes"])

@router.get("/", summary="Obtener rutas entre dos puntos")
async def get_routes(start: str = Query(..., description="lat,lon"),
                     end: str = Query(..., description="lat,lon")):

    lat1, lon1 = map(float, start.split(","))
    lat2, lon2 = map(float, end.split(","))

    osrm_routes = await get_osrm_routes((lat1, lon1), (lat2, lon2))

    processed_routes = []

    for idx, route in enumerate(osrm_routes):
        processed_routes.append({
            "id": route.get("route_id", idx),
            "distance": route["distance"],
            "duration": route["duration"],
            "geometry": route["geometry"],
            "safety_index": calculate_bike_safety_index(route)  # <-- aquí va tu función
        })
    print('processed_routes', processed_routes )
    return processed_routes


