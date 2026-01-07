from fastapi import APIRouter, Query, Depends
from src.database.models import get_db
from src.schema.payment import PaymentSchema
from src.service import payment_service
from sqlalchemy.orm import Session



route = APIRouter(prefix="/payments", tags=["payments"])

@route.post("/")
def to_pay(data: PaymentSchema, db: Session = Depends(get_db)):
    payment = payment_service.create_payment(db, data)
    return payment

@route.get("/history/")
def get_payment_history(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    sender_id: int = Query(0),
    recipient_id: int = Query(0),
    method: str = Query(None),
):
    history = payment_service.get_payment_history(
        db,
        limit=limit,
        offset=offset,
        sender_id=sender_id,
        recipient_id=recipient_id,
        method=method,
    )
    return history