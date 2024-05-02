from enum import Enum


class HandleFileCallback(str, Enum):
    PrintingColor = 'printing_color'
    FakePyrchase = 'fake_purchase' # для тестов, фейковая оплата 
    MakePurchase = 'make_purchase'
    CancelPurchase = 'cancel_purchase'
    CheckPayment = 'check_payment'
    Reset = 'user:reset'

