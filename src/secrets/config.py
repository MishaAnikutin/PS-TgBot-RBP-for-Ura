import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    

TEST_PURCHASE_FLAG = os.getenv("TEST_PURCHASE_FLAG")
API_TOKEN = os.getenv("API_TOKEN")

PRINTER_HOST = os.getenv("PRINTER_HOST")
PRINTER_PORT = os.getenv("PRINTER_PORT")

ADMIN_ID = [int(uid) for uid in os.getenv("ADMIN_ID").split(',')]

BW_PAGE_PRICE = os.getenv("BW_PAGE_PRICE")
COLORED_PAGE_PRICE = os.getenv("COLORED_PAGE_PRICE")
BW2_PAGE_PRICE = os.getenv("BW2_PAGE_PRICE")
COLORED2_PAGE_PRICE = os.getenv("COLORED2_PAGE_PRICE")

PAYMENT_API = os.getenv("PAYMENT_API")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")
CUSTOMER_CODE = os.getenv("CUSTOMER_CODE")
REDIRECT_URL = os.getenv("REDIRECT_URL")

PRINTER_API = os.getenv("PRINTER_API")