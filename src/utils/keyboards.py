from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder, KeyboardButton,
    InlineKeyboardBuilder, InlineKeyboardButton
)
from enum import Enum
from ..callback_data import HandleFileCallback, AdminCallback
from ..secrets.config import TEST_PURCHASE_FLAG

from ..models.page_model import PageColors

async def yesno_keyboard():
    menu_builder = InlineKeyboardBuilder()
    
    menu_builder.button(
            text='Продолжить',
            callback_data=HandleFileCallback.FakePyrchase if TEST_PURCHASE_FLAG else HandleFileCallback.MakePurchase
        )
    
    menu_builder.button(text='Отменить', callback_data=HandleFileCallback.CancelPurchase)

    return menu_builder.as_markup()


async def bw_print_keyboard():
    """Black/white printing or colored"""
    menu_builder = InlineKeyboardBuilder()
    
    # TODO: это костыль, надо исправить, чтобы клавиатура не 
    # зависела от количества вариантов
    
    callback = HandleFileCallback.PrintingColor
    
    menu_builder.row(
        InlineKeyboardButton(text='Черно-белая', callback_data=callback + ':Черно-белая'),
        InlineKeyboardButton(text='Цветная', callback_data=callback + ':Цветная'),
    )
    
    menu_builder.row(
        InlineKeyboardButton(text='Черно-белая (с двух сторон)', callback_data=callback + ':Черно-белая (с двух сторон)'),
        InlineKeyboardButton(text='Цветная (с двух сторон)', callback_data=callback + ':Цветная (с двух сторон)'),
    )
    
    # потомкам
    # [
    #     menu_builder.button(text=getattr(PageColors, color), callback_data=HandleFileCallback.PrintingColor + ':' + getattr(PageColors, color))
    #     for color in PageColors.__dict__.keys() if not (color.startswith('__'))
    # ]
    
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
    
    menu_builder.row(
        InlineKeyboardButton(text='Узнать число пользователей', callback_data=AdminCallback.CountUsers),
        InlineKeyboardButton(text='Сделать рассылку', callback_data=AdminCallback.Mailing),

    )
    
    menu_builder.row(
        InlineKeyboardButton(text='Получить sqlite', callback_data=AdminCallback.GetSQLite)
    )

    return menu_builder.as_markup()
