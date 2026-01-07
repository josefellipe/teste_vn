from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from src.database.models import get_db
from src.service import user_service, payment_service
from src.schema.user import UserCreateSchema

route = APIRouter(prefix="/activis", tags=["activis"])

@route.get("/")
def get_activis(
    db: Session = Depends(get_db),
    user_id: int = Query(...),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    friends_activis = user_service.get_friends(
        db=db,
        user_id=user_id,
        limit=limit,
        offset=offset
    )
    payments_activis_sender = payment_service.get_payment_history(
        db=db,
        sender_id=user_id,
        limit=limit,
        offset=offset
    )
    payments_activis_recipient = payment_service.get_payment_history(
        db=db,
        recipient_id=user_id,
        limit=limit,
        offset=offset
    )

    return {
        "friends_activis": friends_activis,
        "payments_activis_sender": payments_activis_sender,
        "payments_activis_recipient": payments_activis_recipient
    }