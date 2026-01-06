from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str

    class Config:
        orm_mode = True