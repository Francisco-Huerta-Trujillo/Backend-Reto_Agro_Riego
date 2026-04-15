from fastapi import APIRouter
from services.user_service import (
    login,
    get_users,
    get_user,
    create_user,
    delete_user,
    get_user_areas
)

router = APIRouter()

@router.post("/login")
def login_user(user):
    return login(user)

@router.get("/")
def read_users():
    return get_users()

@router.get("/{user_id}")
def read_user(user_id: int):
    return get_user(user_id)

@router.post("/")
def create_user_endpoint(user):
    return create_user(user)

@router.delete("/{user_id}")
def delete_user_endpoint(user_id: int):
    return delete_user(user_id)

@router.get("/{user_id}/areas")
def read_user_areas(user_id: int):
    return get_user_areas(user_id)