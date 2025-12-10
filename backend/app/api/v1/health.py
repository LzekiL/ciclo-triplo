# app/api/v1/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health_check():
    return {"status": "ok", "message": "API está viva"}
