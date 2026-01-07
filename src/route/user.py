from fastapi import APIRouter, HTTPException, Query
from src.service import user_service
from src.schema.user import UserCreateSchema, FriendRequestSchema
from src.exceptions import UserNotFoundException, FriendshipAlreadyExistsException

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
    try:
        result = user_service.add_friend(data)
        return result
    except FriendshipAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@route.get("/{username}")
def get_user(username: str):
    user = user_service.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@route.get("/{user_id}/feed")
def render_feed(user_id: int):
    try:
        feed = user_service.render_feed(user_id)
        return feed
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    

