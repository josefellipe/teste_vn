import pytest
from src.database.models import User
from src.service.payment import PaymentService
from src.schema.payment import PaymentSchema


@pytest.fixture
def service():
    return PaymentService()


@pytest.fixture
def create_user_with_balance(db):
    def _create_user_with_balance(name, username, balance):
        user = User(name=name, username=username, balance=balance)
        db.add(user)
        db.commit()
        return user
    return _create_user_with_balance


def test_create_payment_with_funds(service, create_user_with_balance, db):
    sender = create_user_with_balance("John", "john", 100)
    recipient = create_user_with_balance("Mary", "mary", 0)
    
    data = PaymentSchema(sender_id=sender.id, recipient_id=recipient.id, amount=50, reason="Lunch")
    result = service.create_payment(db, data)
    
    assert result['method'] == 'funds'
    assert result['amount'] == 50


def test_create_payment_with_credit_card(service, create_user_with_balance, db):
    sender = create_user_with_balance("John", "john", 10)
    recipient = create_user_with_balance("Mary", "mary", 0)
    
    data = PaymentSchema(sender_id=sender.id, recipient_id=recipient.id, amount=50, reason="Lunch")
    result = service.create_payment(db, data)
    
    assert result['method'] == 'credit_card'


def test_sender_have_funds_true(create_user_with_balance, db):
    sender = create_user_with_balance("John", "john", 100)
    
    result = PaymentService.sender_have_funds(db, sender_id=sender.id, amount=50)
    
    assert result == True


def test_sender_have_funds_false(create_user_with_balance, db):
    sender = create_user_with_balance("John", "john", 10)
    
    result = PaymentService.sender_have_funds(db, sender_id=sender.id, amount=50)
    
    assert result == False


def test_get_payment_history(service, create_user_with_balance, db):
    sender = create_user_with_balance("John", "john", 100)
    recipient = create_user_with_balance("Mary", "mary", 0)
    
    service.create_payment(db, PaymentSchema(sender_id=sender.id, recipient_id=recipient.id, amount=10, reason="Coffee"))
    service.create_payment(db, PaymentSchema(sender_id=sender.id, recipient_id=recipient.id, amount=20, reason="Lunch"))
    service.create_payment(db, PaymentSchema(sender_id=sender.id, recipient_id=recipient.id, amount=30, reason="Dinner"))
    
    result = service.get_payment_history(db, limit=10, offset=0, sender_id=sender.id)
    
    assert len(result) == 3

