from fastapi import APIRouter
from services.mediciones_service import (
    get_mediciones,
    get_mediciones,
    create_mediciones,
    get_area_mediciones
)

router = APIRouter()

@router.get("/")
def read_mediciones():
    return get_mediciones()

@router.get("/{mediciones_id}")
def read_mediciones(mediciones_id: int):
    return get_mediciones(mediciones_id)

@router.post("/")
def create_mediciones_endpoint(mediciones):
    return create_mediciones(mediciones)

@router.get("/area/{area_id}")
def read_area_mediciones(area_id: int):
    return get_area_mediciones(area_id)