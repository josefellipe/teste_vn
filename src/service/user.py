from src.handler import user_handler
from src.schema.user import UserCreateSchema, FriendRequestSchema
from sqlalchemy.orm import Session

class UserService:
    def get_user(self, db: Session, username: str):
        user = user_handler.get_user(db, username)
        return user
    
    def create_user(self, db: Session, data: UserCreateSchema):
        user = user_handler.create_user(db, data.name, data.username)
        return user
    
    def add_friend(self, db: Session, data: FriendRequestSchema):
        result = user_handler.add_friend(db, data.user_id, data.friend_id)
        return result
    
    def get_friends(self, db: Session, user_id: int, limit: int = 10, offset: int = 0):
        friends = user_handler.get_friends(db, user_id, limit, offset)
        return friends
    
    def render_feed(self, db: Session, user_id: int):
        activities = user_handler.get_user_activity_feed(db, user_id)
        
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