from src.handler import user_handler
from src.schema.user import UserCreateSchema, FriendRequestSchema

class UserService:
    def get_user(self, username: str):
        user = user_handler.get_user(username)
        return user
    
    def create_user(self, data: UserCreateSchema):
        user = user_handler.create_user(data.name, data.username)
        return user
    
    def add_friend(self, data: FriendRequestSchema):
        result = user_handler.add_friend(data.user_id, data.friend_id)
        return result
    
    def get_friends(self, user_id: int, limit: int = 10, offset: int = 0):
        friends = user_handler.get_friends(user_id, limit, offset)
        return friends