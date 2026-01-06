from src.handler import user_handler
from src.schema.user import UserCreate

class UserService:
    def get_user(self, username: str):
        user = user_handler.get_user(username)
        return {"username": user.username, "id": user.id, "balance": user.balance}
    
    def create_user(self, data: UserCreate):
        user = user_handler.create_user(data.username)
        return {"username": user.username, "id": user.id, "status": "created"}
    