from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from ..secrets.config import ADMIN_ID


class UserInAdminsFilter(BaseFilter):
    def __init__(self):
        self.admin_list: tuple[int] = ADMIN_ID

    async def __call__(self, response) -> bool:
        if isinstance(response, Message):
            message: Message = response
            return message.chat.id in self.admin_list
        
        elif isinstance(response, CallbackQuery):
            call: CallbackQuery = response
            return call.message.chat.id in self.admin_list
