from fastapi import APIRouter
from services.historial_service import (
    get_historial,
    get_historial_item
)

router = APIRouter()

@router.get("/")
def read_historial():
    return get_historial()

@router.get("/{historial_id}")
def read_historial_item(historial_id: int):
    return get_historial_item(historial_id)