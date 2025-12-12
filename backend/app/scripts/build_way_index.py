import osmium
import json

# Archivo de entrada
OSM_FILE = "spain-latest.osm.pbf"
# Archivo de salida
OUTPUT_FILE = "way_index.json"

# Definimos qué tags nos interesan
TAGS_TO_KEEP = ["highway", "surface", "cycleway", "shoulder", "lanes", "lit", "maxspeed"]

class WayHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.ways = {}

    def way(self, w):
        tags = {k: v for k, v in w.tags.items() if k in TAGS_TO_KEEP}
        if tags:
            self.ways[w.id] = tags

handler = WayHandler()
print("Procesando PBF, esto puede tardar un poco...")
handler.apply_file(OSM_FILE)

print(f"Procesados {len(handler.ways)} ways, guardando en {OUTPUT_FILE}...")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(handler.ways, f, ensure_ascii=False)

print("¡Índice generado!")
