from fastapi import APIRouter
from services.area_service import (
    get_areas,
    get_area,
    create_area,
    update_area,
    delete_area,
    get_area_sensors,
    get_area_alerts
)

router = APIRouter()

@router.get("/")
def read_areas():
    return get_areas()

@router.get("/{area_id}")
def read_area(area_id: int):
    return get_area(area_id)

@router.post("/")
def create_area_endpoint(area):
    return create_area(area)

@router.put("/{area_id}")
def update_area_endpoint(area_id: int, area):
    return update_area(area_id, area)

@router.delete("/{area_id}")
def delete_area_endpoint(area_id: int):
    return delete_area(area_id)

@router.get("/{area_id}/sensors")
def read_area_sensors(area_id: int):
    return get_area_sensors(area_id)

@router.get("/{area_id}/alerts")
def read_area_alerts(area_id: int):
    return get_area_alerts(area_id)