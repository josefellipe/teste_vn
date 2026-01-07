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
    
    def render_feed(self, user_id: int):
        activities = user_handler.get_user_activity_feed(user_id)
        
        feed = []
        for activity in activities:
            if activity['type'] == 'payment':
                data = activity['data']
                message = f"{data['sender']} paid {data['recipient']} ${data['amount']:.2f} for {data['reason']}"
                feed.append(message)
            elif activity['type'] == 'friendship':
                data = activity['data']
                message = f"{data['user1']} and {data['user2']} are now friends"
                feed.append(message)
        
        return feed