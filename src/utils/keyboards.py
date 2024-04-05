from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder, KeyboardButton,
    InlineKeyboardBuilder, InlineKeyboardButton
)


async def yesno_keyboard():
    menu_builder = InlineKeyboardBuilder()

    menu_builder.button(text='Продолжить', callback_data='make_purchase')
    menu_builder.button(text='Отменить', callback_data='cancel_purchase')

    return menu_builder.as_markup()
    
    
async def reset_keyboard():
    return InlineKeyboardBuilder().button(text='Заново', callback_data='reset').as_markup()


async def stop_keyboard():
    return InlineKeyboardBuilder().button(text='Отмена', callback_data='reset').as_markup()


async def payment_keyboard(link):
    menu_builder = InlineKeyboardBuilder()
    
    menu_builder.button(text='Ссылка на оплату', url=link)
    menu_builder.button(text='Проверить оплату', callback_data='check_payment')

    return menu_builder.as_markup()
 