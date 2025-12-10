import os

APP_NAME = "Ciclo-Triplo API"
ENV = os.getenv("ENV", "development")
DEBUG = ENV == "development"

# URL del OSRM público (puedes cambiarla si más adelante usas un servidor propio)
OSRM_URL = os.getenv("OSRM_URL", "http://router.project-osrm.org")
