from pydantic import BaseModel

class UserCreateSchema(BaseModel):
    name: str
    username: str

    class Config:
        orm_mode = True

class FriendRequestSchema(BaseModel):
    user_id: int
    friend_id: int
