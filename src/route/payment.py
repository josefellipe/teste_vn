from fastapi import APIRouter, Query
from src.schema.payment import PaymentSchema
from src.service import payment_service


route = APIRouter(prefix="/payments", tags=["payments"])

@route.post("/")
def to_pay(data: PaymentSchema):
    payment = payment_service.create_payment(data)
    return payment

@route.get("/history/")
def get_payment_history(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    sender_id: int = Query(0),
    recipient_id: int = Query(0),
    method: str = Query(None),
):
    history = payment_service.get_payment_history(
        limit=limit,
        offset=offset,
        sender_id=sender_id,
        recipient_id=recipient_id,
        method=method,
    )
    return history