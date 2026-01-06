from src.schema.payment import PaymentSchema, PaymentSchemaResponse
from src.handler import user_handler

class PaymentService:
    def create_payment(self, data: PaymentSchema) -> PaymentSchemaResponse:
        if data.amount <= 0:
            raise ValueError("Amount must be greater than zero")
        
        payment_method = "credit_card"
        if PaymentService.sender_have_funds(data.sender_id, data.amount):
            payment_method = "funds"
        
        payment = user_handler.create_payment(data, payment_method)

        return payment
    
    @staticmethod
    def sender_have_funds(sender_id: int, amount: float) -> bool:
        sender = user_handler.get_user_by_id(sender_id)
        if not sender:
            return ValueError("Sender not found")
        
        return sender.balance >= amount
