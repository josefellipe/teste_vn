from fastapi import APIRouter, HTTPException
from src.service import user_service
from src.schema.user import UserCreate

route = APIRouter(prefix="/users", tags=["users"])

@route.post("/")
def create_user(data: UserCreate):
    try:
        result = user_service.create_user(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@route.get("/{username}")
def get_user(username: str):
    user = user_service.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
