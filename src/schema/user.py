from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    username: str

    class Config:
        orm_mode = True