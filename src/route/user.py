from fastapi import APIRouter
from src.service import user_service
from src.schema.user import UserCreate

route = APIRouter(prefix="/test")

@route.post("/")
def create_user(data: UserCreate):
    user_service.create_user(data)
    return {"test": "ok"}