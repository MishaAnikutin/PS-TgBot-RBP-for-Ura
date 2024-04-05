from yookassa import Payment
from yookassa import Configuration

from .base import BasePayment
from ..secrets.config import PAYMENT_TOKEN, PAYMENT_CONF1, PAYMENT_CONF2, RETURN_URL


class paymentFactory(BasePayment):
    payment_token = PAYMENT_TOKEN


    @classmethod
    def create_payment(cls, value: int):
        Configuration.configure(PAYMENT_CONF1, PAYMENT_CONF2)

        payment = Payment.create({
            "amount": {
                "value": str(value),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": RETURN_URL
            },
            "capture": True,
            "description": "Услуги Типографии"
        })
        
        return payment

    def find_payment(payment_id: str):
        return Payment.find_one(payment_id)


