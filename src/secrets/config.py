import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    

API_TOKEN = os.getenv("API_TOKEN")

PRINTER_HOST = os.getenv("PRINTER_HOST")
PRINTER_PORT = os.getenv("PRINTER_PORT")

ADMIN_ID = [int(uid) for uid in os.getenv("ADMIN_ID").split(',')]

PAGE_PRICE = os.getenv("PAGE_PRICE")

PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")
PAYMENT_CONF1 = os.getenv("PAYMENT_CONF1")
PAYMENT_CONF2 = os.getenv("PAYMENT_CONF2")

RETURN_URL = 'https://t.me/prnt_server_bot'
PAYMENT_API = "yookassa"
PRINTER_API = "kyocera"