from src.database import User, SessionLocal

class UserHandler:
    def create_user(self, username: str):
        db = SessionLocal()
        new_user = User(username=username)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.close()
        return new_user
    