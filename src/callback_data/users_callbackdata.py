from enum import Enum


class HandleFileCallback(str, Enum):
    MakePurchase = 'make_purchase'
    CancelPurchase = 'cancel_purchase'
    CheckPayment = 'check_payment'
    Reset = 'user:reset'

