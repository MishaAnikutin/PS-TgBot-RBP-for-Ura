# import threading
# import time

# from . import paymentFactory


# class PaymentChecker:
#     def __init__(self, payment_id: str, payment: paymentFactory):        
#         self.payment = payment
#         self.payment_id = payment_id
#         self.payment_successful = False
        
#         payment_thread = threading.Thread(target=self.run)
#         payment_thread.start()
        

    # def run(self):
    #     for i in range(60):
    #         response = self.payment.find_payment(self.payment_id)
    #         if response.status == "succeeded" and user["summa"] == res.amount.value:
                
    #         self.payment_successful = True