from ..secrets.config import PAYMENT_API


if PAYMENT_API == "yookassa":
    from .yo import paymentFactory
else:
    raise KeyError(f'Invalid {PAYMENT_API = }')

    
__all__ = ['paymentFactory']
