from src.database import User, SessionLocal
from src.schema.payment import PaymentSchema


class UserHandler:
    def create_user(self, username: str):
        db = SessionLocal()
        new_user = User(username=username)
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