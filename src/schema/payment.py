from pydantic import BaseModel

class PaymentSchema(BaseModel):
    amount: float
    recipient_id: int
    sender_id: int
    reason: str


class PaymentSchemaResponse(BaseModel):
    status: str
    reason: str
    method: str
    sender: str
    recipient: str
    amount: float
