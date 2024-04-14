import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .secrets.config import API_TOKEN, PRINTER_HOST, PRINTER_PORT
from .bot_handlers import router

from .database import CRUDActions

logging.basicConfig(level=logging.INFO)
    

async def main():
    logging.info('creating table')
    CRUDActions.create_table()
    
    bot = Bot(token=API_TOKEN)
    
    dp = Dispatcher(storage=MemoryStorage())    
    dp.include_router(router)
    
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
    )
    
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
        
    except KeyboardInterrupt:
        logging.warning('--PROGRAM STOPPED--')
