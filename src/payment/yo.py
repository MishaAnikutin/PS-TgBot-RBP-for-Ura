import aiohttp
from dataclasses import dataclass, field, asdict

from typing import List

from .base import BasePayment, PaymentException
from ..secrets.config import PAYMENT_TOKEN, REDIRECT_URL, CUSTOMER_CODE
from .models import (
        create_model,
        CreatePaymentModel,
        PaymentInfoModel,
        PaymentRefundModel
    )


@dataclass
class PaymentData:    
    amount: str 
    purpose: str = "Услуги типографии"
    redirectUrl: str = REDIRECT_URL
    customerCode: str = CUSTOMER_CODE
    paymentMode: List[str] = field(default_factory=lambda : ["sbp", "card"])

    
    def __post_init__(self):
        self.amount = '{:.02f}'.format(float(self.amount))

@dataclass
class Payment:
    """Модель для создания параметров запроса для создания платежа"""
    
    Data: PaymentData


class paymentFactory(BasePayment):
    __create_payment_url = 'https://enter.tochka.com/uapi/acquiring/v1.0/payments'
    __payment_info_url   = 'https://enter.tochka.com/uapi/acquiring/v1.0/payments/%s'
    __payment_refund_url = 'https://enter.tochka.com/uapi/acquiring/v1.0/payments/%s/refund'
    __headers = {'Authorization': f'Bearer {PAYMENT_TOKEN}', 'Content-Type': 'application/json'}
    
    
    @classmethod
    async def create_payment(cls, value: int) -> CreatePaymentModel:
        """Создает платеж и возвращает на него ссылку и ID"""
        
        payment_params = Payment(Data=PaymentData(amount=str(value)))
        payload = asdict(payment_params)
            
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    cls.__create_payment_url,
                    headers=cls.__headers,
                    json=payload
                ) as response:
                
                print(await response.json())
                
                try:           
                    result: CreatePaymentModel = create_model(CreatePaymentModel, await response.json())
                except (KeyError, TypeError, ValueError) as exc: 
                    raise PaymentException(f'Ошибка при создании ссылки на оплату: {exc}')
                return result
    
    @classmethod     
    async def get_payment_information(cls, payment_id: str) -> PaymentInfoModel:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    cls.__payment_info_url % payment_id,
                    headers=cls.__headers
                ) as response:      
                
                return create_model(PaymentInfoModel, await response.json())
                
    @classmethod     
    async def refund_payment(cls, payment_id: str, amount: int):
        refund_params = {'Data': {'amount': f'{amount:.02f}'}}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                cls.__payment_refund_url % payment_id,
                headers=cls.__headers,
                json=refund_params
            ) as response:
                
                return create_model(PaymentRefundModel, await response.json())
