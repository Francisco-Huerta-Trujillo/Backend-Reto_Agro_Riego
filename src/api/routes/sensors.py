from fastapi import APIRouter
from services.sensor_service import (
    get_sensors,
    get_sensor,
    create_sensor,
    get_area_sensors
)

router = APIRouter()

@router.get("/")
def read_sensors():
    return get_sensors()

@router.get("/{sensor_id}")
def read_sensor(sensor_id: int):
    return get_sensor(sensor_id)

@router.post("/")
def create_sensor_endpoint(sensor):
    return create_sensor(sensor)

@router.get("/area/{area_id}")
def read_area_sensors(area_id: int):
    return get_area_sensors(area_id)