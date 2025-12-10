# app/services/bike_routing.py

def calculate_bike_safety_index(route):
    """
    Calcula un índice de seguridad simple para ciclistas basado en:
    - Tipo de vía (highway)
    - Presencia de arcenes o carriles bici (shoulder/cycleway)
    - Superficie
    """
    total_distance = 0
    weighted_score = 0

    for leg in route.get("legs", []):
        for step in leg.get("steps", []):
            print('step', step)
            distance = step.get("distance", 0)

            highway_type = step.get("name", "").lower()
            if "motorway" in highway_type or "trunk" in highway_type:
                road_score = 0.1
            elif "primary" in highway_type:
                road_score = 0.4
            elif "secondary" in highway_type:
                road_score = 0.7
            else:
                road_score = 1.0

            surface_score = 1.0
            if step.get("surface") in ["unpaved", "gravel", "dirt"]:
                surface_score = 0.5

            shoulder_score = 1.0
            if step.get("shoulder") == "yes" or step.get("cycleway") in ["lane", "track"]:
                shoulder_score = 1.0
            else:
                shoulder_score = 0.7

            segment_score = road_score * 0.5 + surface_score * 0.3 + shoulder_score * 0.2
            weighted_score += segment_score * distance
            total_distance += distance

    if total_distance == 0:
        return 0.5

    return round(weighted_score / total_distance, 2)
