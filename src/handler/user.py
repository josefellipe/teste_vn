from src.database import User, session

class UserHandler:
    def create_user(self, username: str):
        new_user = User(username=username)
        new_user.save()
        new_user.commit()
        return new_user
    