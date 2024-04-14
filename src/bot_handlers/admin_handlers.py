from typing import Optional, Generator, AsyncGenerator
import asyncio

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, ContentType, CallbackQuery

from ..utils.keyboards import admin_keyboard, stop_keyboard
from ..database import CRUDActions, UserCRUDModel

from ..filters.admin_filter import UserInAdminsFilter
from ..callback_data import AdminCallback
from ..states import MailingStates

admin_router = Router()


@admin_router.message(StateFilter(None), Command("admin"), UserInAdminsFilter())
async def admin(message: Message, state: FSMContext):
    user = UserCRUDModel(uid=message.chat.id, username=message.chat.username)
    
    if (not CRUDActions.check_user_in_db(user)):
        CRUDActions.add_user(user=user)
        
    await message.answer(
        text = f'Привет, {message.chat.username}.\n' \
               f'Ты в админке',
          reply_markup=await admin_keyboard()
        )


@admin_router.callback_query(F.data == AdminCallback.Reset)
async def cancel(call: CallbackQuery, state: FSMContext):
    '''Cancel handle and return to start'''
    await call.message.answer(text='Отмена...')
    await state.clear()
    await admin(call.message, state) 
    

@admin_router.callback_query(F.data == AdminCallback.Mailing, UserInAdminsFilter())
async def start_mailing(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        text = f'Введите текст рассылки\n\nМожно текст и/или фото',
        reply_markup = await stop_keyboard(callback_factory=AdminCallback)
    )

    await state.set_state(MailingStates.GetMailingMessageState)
    

@admin_router.callback_query(F.data == AdminCallback.CountUsers, UserInAdminsFilter())
async def start_mailing(call: CallbackQuery, state: FSMContext):
    n = CRUDActions.count_users()
    
    await call.message.answer(
        text = f'Количество пользователей: {n}',
        reply_markup = await stop_keyboard(callback_factory=AdminCallback, text='Назад')
    )

    await state.set_state(MailingStates.GetMailingMessageState)


@admin_router.message(
    MailingStates.GetMailingMessageState, 
    UserInAdminsFilter(), 
    F.content_type == ContentType.PHOTO
)
async def get_mailing_message_photo(message: Message, state: FSMContext, bot: Bot):
    photo = message.photo[-1].file_id
    text = message.caption
    
    await mail_users(message=message, text=text, photo=photo, bot=bot)
    await state.clear()


@admin_router.message(
    MailingStates.GetMailingMessageState, 
    UserInAdminsFilter(), 
    F.content_type == ContentType.TEXT
)
async def get_mailing_message_text(message: Message, state: FSMContext, bot: Bot):    
    text= message.text     
    
    await mail_users(message=message, text=text, bot=bot)
    await state.clear()
    

async def mail_users(
    message: Message,
    bot: Bot,
    text: Optional[str] = None, 
    photo: Optional[str] = None 
):
    await message.answer(text = f'Начинаем рассылку')

    if CRUDActions.Metadata.SYNC:
        await send_all_users_sg(text=text, bot=bot, photo=photo, usersGenerator=CRUDActions.usersGenerator)
    else:
        await send_all_users_ag(text=text, bot=bot, photo=photo, usersGenerator=CRUDActions.usersGenerator)
    
    await message.answer(text='Рассылка отправлена!')
    
    
async def send_all_users_sg(
        bot: Bot, 
        usersGenerator: Generator[UserCRUDModel, None, None],
        text: Optional[str] = None, 
        photo: Optional[str] = None
    ):
    
    if photo is not None:
        await asyncio.gather(*[bot.send_photo(chat_id=user.uid, caption=text, photo=photo)
                               for user in usersGenerator()])
    else:
        await asyncio.gather(*[bot.send_message(chat_id=user.uid, text=text)
                               for user in usersGenerator()])
           
    
async def send_all_users_ag(
        bot: Bot, 
        usersGenerator: AsyncGenerator[UserCRUDModel, None],
        text: Optional[str] = None, 
        photo: Optional[str] = None
    ):
    
    if photo is not None:
        await asyncio.gather(*[bot.send_photo(chat_id=user.uid, caption=text, photo=photo)
                               async for user in usersGenerator()])
    else:
        await asyncio.gather(*[bot.send_message(chat_id=user.uid, text=text)
                               async for user in usersGenerator()])
