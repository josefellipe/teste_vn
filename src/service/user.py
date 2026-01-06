from src.handler import user_handler
from src.schema.user import UserCreate

class UserService:
    def create_user(self, data: UserCreate):
        user_handler.create_user(data.username)
        return {"username": data.username, "status": "created"}
    