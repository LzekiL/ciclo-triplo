#!/usr/bin/env python3
import csv
import os
import sqlite3
import rasterio
import numpy as np
from rasterio.transform import from_origin
from rasterio.enums import Resampling
from tqdm import tqdm

# Configuración
NODES_CSV = "data/nodes.csv"              # Path a nodes.csv
SRTM_FOLDER = "data/srtm/"                # Carpeta con mosaicos SRTM
OUTPUT_DB = "data/elevation.sqlite"       # SQLite de salida

# Función para cargar todos los mosaicos SRTM en memoria
def load_srtm_tiles(folder):
    tiles = []
    for f in os.listdir(folder):
        if f.endswith(".tif") or f.endswith(".hgt"):
            path = os.path.join(folder, f)
            ds = rasterio.open(path)
            tiles.append(ds)
    return tiles

# Función para obtener altitud desde mosaicos (simple búsqueda, toma primer tile que contenga el punto)
def get_altitude(lat, lon, tiles):
    for ds in tiles:
        left, bottom, right, top = ds.bounds
        if left <= lon <= right and bottom <= lat <= top:
            row, col = ds.index(lon, lat)
            value = ds.read(1)[row, col]
            if ds.nodata is not None and value == ds.nodata:
                return None
            return float(value)
    return None

def main():
    tiles = load_srtm_tiles(SRTM_FOLDER)
    print(f"{len(tiles)} mosaicos SRTM cargados.")

    # Crear SQLite
    conn = sqlite3.connect(OUTPUT_DB)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS nodes")
    cur.execute("""
        CREATE TABLE nodes (
            id INTEGER PRIMARY KEY,
            lat REAL,
            lon REAL,
            altitude REAL
        )
    """)

    # Leer CSV y calcular altitudes
    with open(NODES_CSV, newline='') as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, desc="Procesando nodos"):
            node_id = int(row["id"])
            lat = float(row["lat"])
            lon = float(row["lon"])
            alt = get_altitude(lat, lon, tiles)
            cur.execute("INSERT INTO nodes (id, lat, lon, altitude) VALUES (?, ?, ?, ?)",
                        (node_id, lat, lon, alt))

    conn.commit()
    conn.close()
    print(f"elevation.sqlite creado en {OUTPUT_DB}")

if __name__ == "__main__":
    main()
