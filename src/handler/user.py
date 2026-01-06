from src.database import User, PaymentsHistory, FriendsList, SessionLocal
from src.schema.payment import PaymentSchema
from src.schema.user import FriendRequestSchema


class UserHandler:
    def create_user(self, name: str, username: str) -> User:
        db = SessionLocal()
        new_user = User(name=name, username=username)
        db.add(new_user)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(f"Error creating user: {e}")
        db.refresh(new_user)
        db.close()
        return new_user
    
    def get_user(self, username: str):
        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        db.close()
        return user
    
    def get_user_by_id(self, user_id: int):
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        db.close()
        return user
    
    def create_payment(self, data: PaymentSchema, payment_method: str):
        db = SessionLocal()
        sender = db.query(User).filter(User.id == data.sender_id).first()
        recipient = db.query(User).filter(User.id == data.recipient_id).first()
        
        if payment_method == "funds":
            sender.balance -= data.amount
        else:
            pass  # Handle credit card payment logic here

        recipient.balance += data.amount

        payment_record = PaymentsHistory(
            sender_id=sender.id,
            recipient_id=recipient.id,
            amount=data.amount,
            method=payment_method,
            reason=data.reason
        )
        db.add(payment_record)

        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(f"Error creating payment: {e}")
        
        return {
            "status": "success",
            "method": payment_method,
            "sender": sender.username,
            "recipient": recipient.username,
            "amount": data.amount
        }
    
    def get_payment_history(
            self, limit: int = 10, offset: int = 0, sender_id: int = 0, recipient_id: int = 0, method: str = None
    ):
        db = SessionLocal()
        query = db.query(PaymentsHistory)
        if sender_id:
            query = query.filter(PaymentsHistory.sender_id == sender_id)
        if recipient_id:
            query = query.filter(PaymentsHistory.recipient_id == recipient_id)
        if method:
            query = query.filter(PaymentsHistory.method == method)
        history = query.order_by(PaymentsHistory.id.desc()).limit(limit).offset(offset).all()
        db.close()
        return history
    
    def add_friend(self, user_id: int, friend_id: int):
        db = SessionLocal()

        existing_friendship = db.query(FriendsList).filter(
            FriendsList.user_id == user_id,
            FriendsList.friend_id == friend_id
        ).first()
        if existing_friendship:
            db.close()
            raise Exception("Friendship already exists")

        new_friendship = FriendsList(user_id=user_id, friend_id=friend_id)
        db.add(new_friendship)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(f"Error adding friend: {e}")
        db.close()
        return True
    
    def get_friends(self, user_id: int, limit: int = 10, offset: int = 0):
        db = SessionLocal()
        friends = db.query(FriendsList).filter(FriendsList.user_id == user_id).limit(limit).offset(offset).all()
        db.close()
        return friends