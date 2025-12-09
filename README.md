# ciclo-triplo
Backend + Web prototype for the Bike Safety Routing App (Phase 1 — OSRM + FastAPI).

Structure:
ciclo-triplo/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   └── services/
│   │       ├── osrm_service.py
│   │       ├── safety_index_service.py
│   │       └── weather_service.py   (futuro)
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── index.html
│   ├── main.js
│   ├── styles.css
│   └── (opcional) Dockerfile
│
├── docker-compose.yml
└── README.md
