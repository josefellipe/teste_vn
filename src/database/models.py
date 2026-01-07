from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    balance = Column(Integer, default=0)

class PaymentsHistory(Base):
    __tablename__ = "payments_history"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, nullable=False)
    recipient_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    method = Column(String, nullable=False)
    reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

class FriendsList(Base):
    __tablename__ = "friends_list"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    friend_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

uri = "sqlite:///./minivenmo.db"

engine = create_engine(uri, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


