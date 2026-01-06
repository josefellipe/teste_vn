from pydantic import BaseModel

class PaymentSchema(BaseModel):
    amount: float
    recipient_id: int
    sender_id: int

    class Config:
        orm_mode = True

class PaymentSchemaResponse(BaseModel):
    status: str
    method: str
    sender: str
    recipient: str
    amount: float
