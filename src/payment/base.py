from abc import ABC, abstractmethod


class BasePayment(ABC):
    @abstractmethod
    def create_payment(self, value):
        ...
    