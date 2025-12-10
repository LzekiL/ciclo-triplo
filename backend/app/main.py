from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1 import bike_routes, health

# Calcular la raíz del proyecto automáticamente
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # sube desde backend/app/main.py hasta ciclo-triplo/

app = FastAPI(title="Ciclo-Triplo API", version="1.0.0")

# Usar ruta relativa a /app, que es el cwd dentro del contenedor
frontend_path = Path("frontend")  # /app/frontend dentro del contenedor
app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

# Routers de la API
app.include_router(health.router, prefix="/health")
app.include_router(bike_routes.router, prefix="/api/v1/routes")
