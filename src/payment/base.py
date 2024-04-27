from abc import ABC, abstractmethod, abstractclassmethod


class BasePayment(ABC):
    @classmethod
    @abstractmethod
    async def create_payment(cls, value):
        ...
        
    @classmethod
    @abstractmethod
    async def get_payment_information(cls, payment_id):
        ...
    
    @classmethod
    @abstractmethod
    async def refund_payment(cls, payment_id, amount):
        ...
        
        
class PaymentException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'PaymentException: {self.message}'    