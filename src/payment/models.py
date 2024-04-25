from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, Any


@dataclass
class BasePaymentResponse:
    @dataclass
    class PaymentRLink:
        self: str

    @dataclass
    class PaymentRMeta:
        totalPages: int
    
    Links: PaymentRLink
    Meta: PaymentRMeta

    
@dataclass
class CreatePaymentModel(BasePaymentResponse):
    @dataclass
    class CreatePaymentData:
        purpose: str
        amount: float 
        status: str
        operationId: str 
        paymentLink: str 
        
    Data: CreatePaymentData


class PaymentStatus:
    CREATED = "CREATED"      # Операция создана
    APPROVED = "APPROVED"    # Операция одобрена (оплата прошла успешно)
    ON_REFUND = "ON-REFUND"  # Операция заблокирована на время выполнения возврата
    REFUNDED = "REFUNDED"    # Осуществлен возврат
    EXPIRED = "EXPIRED"      # Истек срок действия


@dataclass
class PaymentOperationModel:
    purpose: str
    amount: str
    status: PaymentStatus
    operationId: str
    paymentLink: str
    customerCode: str
    paymentType: str
    paymentId: str
    transactionId: str
    createdAt: str


@dataclass
class PaymentInfoModel(BasePaymentResponse):
    @dataclass
    class PaymentInfoData:
        Operation: PaymentOperationModel
    
    Data: PaymentInfoData



@dataclass
class PaymentRefundModel(BasePaymentResponse):
    @dataclass
    class PaymentRefundData:
        isRefund: bool
    
    Data: PaymentRefundData
    
    
def create_model(model, response: Dict[str, Any]):
    """Создает инстатнс модели датакласса из словаря"""

    return model(**{
        field: response.get(field) 
        if not isinstance(response.get(field) , dict)
        else create_model(model.__dataclass_fields__[field].type, response.get(field))
        for field in model.__dataclass_fields__
    })
