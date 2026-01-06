from fastapi import APIRouter, HTTPException, Query
from src.service import user_service, payment_service
from src.schema.user import UserCreateSchema

route = APIRouter(prefix="/activis", tags=["activis"])

@route.get("/")
def get_activis(
    user_id: int = Query(...),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    friends_activis = user_service.get_friends(
        user_id=user_id,
        limit=limit,
        offset=offset
    )
    payments_activis_sender = payment_service.get_payment_history(
        sender_id=user_id,
        limit=limit,
        offset=offset
    )
    payments_activis_recipient = payment_service.get_payment_history(
        recipient_id=user_id,
        limit=limit,
        offset=offset
    )

    return {
        "friends_activis": friends_activis,
        "payments_activis_sender": payments_activis_sender,
        "payments_activis_recipient": payments_activis_recipient
    }