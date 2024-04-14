from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder, KeyboardButton,
    InlineKeyboardBuilder, InlineKeyboardButton
)
from enum import Enum
from ..callback_data import HandleFileCallback, AdminCallback


async def yesno_keyboard():
    menu_builder = InlineKeyboardBuilder()

    menu_builder.button(text='Продолжить', callback_data=HandleFileCallback.MakePurchase)
    menu_builder.button(text='Отменить', callback_data=HandleFileCallback.CancelPurchase)

    return menu_builder.as_markup()


async def stop_keyboard(callback_factory: Enum, text='Отмена'):
    menu_builder = InlineKeyboardBuilder()

    try:
        menu_builder.button(text=text, callback_data=callback_factory.Reset)
    except:
        raise KeyError(f'Invalid callback_factory: {callback_factory}, {type(callback_factory)}')
    
    return menu_builder.as_markup()


async def payment_keyboard(link):
    menu_builder = InlineKeyboardBuilder()
    
    menu_builder.button(text='Ссылка на оплату', url=link)
    menu_builder.button(text='Проверить оплату', callback_data=HandleFileCallback.CheckPayment)

    return menu_builder.as_markup()

async def admin_keyboard():
    menu_builder = InlineKeyboardBuilder()
    
    menu_builder.button(text='Узнать число пользователей', callback_data=AdminCallback.CountUsers)
    menu_builder.button(text='Сделать рассылку', callback_data=AdminCallback.Mailing)

    return menu_builder.as_markup()
