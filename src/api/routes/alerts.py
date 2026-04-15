from fastapi import APIRouter
from services.alert_service import (
    get_alerts,
    get_alert,
    create_alert,
    mark_alert_as_read,
    get_area_alerts
)

router = APIRouter()

@router.get("/")
def read_alerts():
    return get_alerts()

@router.get("/{alert_id}")
def read_alert(alert_id: int):
    return get_alert(alert_id)

@router.post("/")
def create_alert_endpoint(alert):
    return create_alert(alert)

@router.put("/{alert_id}/read")
def mark_as_read(alert_id: int):
    return mark_alert_as_read(alert_id)

@router.get("/area/{area_id}")
def read_area_alerts(area_id: int):
    return get_area_alerts(area_id)