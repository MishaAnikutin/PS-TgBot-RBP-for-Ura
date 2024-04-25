from abc import ABC, abstractmethod


class BasePayment(ABC):
    @abstractmethod
    async def create_payment(self, value):
        ...
    
    @abstractmethod
    async def check_payment(cls):
        ...
        
        
class PaymentException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'PaymentException: {self.message}'    