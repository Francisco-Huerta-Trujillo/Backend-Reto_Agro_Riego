from fastapi import APIRouter
from services.predio_service import (
    get_predios,
    get_predio,
    create_predio,
    update_predio,
    delete_predio,
    get_predio_areas
)

router = APIRouter()

@router.get("/")
def read_predios():
    return get_predios()

@router.get("/{predio_id}")
def read_predio(predio_id: int):
    return get_predio(predio_id)

@router.post("/")
def create_predio_endpoint(predio):
    return create_predio(predio)

@router.put("/{predio_id}")
def update_predio_endpoint(predio_id: int, predio):
    return update_predio(predio_id, predio)

@router.delete("/{predio_id}")
def delete_predio_endpoint(predio_id: int):
    return delete_predio(predio_id)

@router.get("/{predio_id}/areas")
def read_predio_areas(predio_id: int):
    return get_predio_areas(predio_id)