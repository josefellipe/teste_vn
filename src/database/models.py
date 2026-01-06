from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    balance = Column(Integer, default=0)

class PaymentsHistory(Base):
    __tablename__ = "payments_history"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, nullable=False)
    recipient_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    method = Column(String, nullable=False)

uri = "sqlite:///./test.db"

engine = create_engine(uri, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


