from fastapi import APIRouter, HTTPException, Query
from src.service import user_service
from src.schema.user import UserCreateSchema, FriendRequestSchema

route = APIRouter(prefix="/users", tags=["users"])

@route.post("/")
def create_user(data: UserCreateSchema):
    result = user_service.create_user(data)
    if not result:
        raise HTTPException(status_code=400, detail="Username already exists")
    return result

    
@route.get("/friends")
def get_friends(
        user_id: int = Query(...),
        limit: int = Query(10, ge=1),
        offset: int = Query(0, ge=0)
    ):
    return user_service.get_friends(user_id, limit, offset)


@route.post("/friends")
def add_friend(data: FriendRequestSchema):
    result = user_service.add_friend(data)
    if not result:
        raise HTTPException(status_code=400, detail="Could not add friend")
    return result


@route.get("/{username}")
def get_user(username: str):
    user = user_service.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

