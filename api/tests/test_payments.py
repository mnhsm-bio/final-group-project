from fastapi.testclient import TestClient
from ..controllers import payments as controller
from ..main import app
import pytest
from ..models import payments as model

client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_payment(db_session):
    # Sample payment data
    payment_data = {
        "order_id": 1,
        "amount": 25.50,
        "payment_method": "credit_card",
        "status": "completed"
    }

    payment_object = model.Payment(**payment_data)

    # Call the create function
    created_payment = controller.create(db_session, payment_object)

    # Assertions
    assert created_payment is not None
    assert created_payment.order_id == 1
    assert created_payment.amount == 25.50
    assert created_payment.payment_method == "credit_card"
    assert created_payment.status == "completed"