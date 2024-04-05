from typing import Callable, Dict, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import Message

from ..secrets.config import ADMIN_ID
from ..printer_api import PrinterAPI


class CheckCartridgeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        flag = await PrinterAPI.check_printer_cartridge()
        
        if not flag:
            await event.bot.send_message(chat_id=ADMIN_ID, text="WARNING: Картридж закончился")
            return await event.answer("К сожалению, у принтера закончился картирдж")
        
        return await handler(event, data)
    
    
class CheckPagesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        printer_capacity = await PrinterAPI.get_printer_capacity()
        
        if 25 < printer_capacity < 100:
            await event.bot.send_message(chat_id=ADMIN_ID, text="Осталось менее 100 листов бумаги")
        if 0 < printer_capacity <= 25:
            await event.bot.send_message(chat_id=ADMIN_ID, text="Осталось менее 25 листов бумаги")
        if printer_capacity == 0:
            await event.bot.send_message(chat_id=ADMIN_ID, text="Бумага для принтера закончилась")
            
        return await handler(event, data)
    
