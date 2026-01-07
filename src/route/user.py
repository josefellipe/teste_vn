from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from src.service import user_service
from src.schema.user import UserCreateSchema, FriendRequestSchema
from src.exceptions import UserNotFoundException, FriendshipAlreadyExistsException
from src.database.models import get_db

route = APIRouter(prefix="/users", tags=["users"])

@route.post("/")
def create_user(data: UserCreateSchema, db: Session = Depends(get_db)):
    result = user_service.create_user(db, data)
    if not result:
        raise HTTPException(status_code=400, detail="Username already exists")
    return result

    
@route.get("/friends")
def get_friends(
        user_id: int = Query(...),
        limit: int = Query(10, ge=1),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
    ):
    return user_service.get_friends(db, user_id, limit, offset)


@route.post("/friends")
def add_friend(data: FriendRequestSchema, db: Session = Depends(get_db)):
    try:
        result = user_service.add_friend(db, data)
        return result
    except FriendshipAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@route.get("/{username}")
def get_user(username: str, db: Session = Depends(get_db)):
    user = user_service.get_user(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@route.get("/{user_id}/feed")
def render_feed(user_id: int, db: Session = Depends(get_db)):
    try:
        feed = user_service.render_feed(db, user_id)
        return feed
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    

