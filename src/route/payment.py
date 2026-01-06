from fastapi import APIRouter
from src.schema.payment import PaymentSchema
from src.service import payment_service


route = APIRouter(prefix="/payments", tags=["payments"])

@route.post("/")
def to_pay(data: PaymentSchema):
    payment = payment_service.create_payment(data)
    return payment