from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, ContentType, CallbackQuery

from ..models.page_model import Page
from ..models.user_model import FileModel, UserData
from .states import HandleFileStates
from ..printer_api import PrinterAPI
from ..file_handlers import create_document, ALLOWED_FORMATS
from ..payment import paymentFactory

from ..utils.keyboards import yesno_keyboard, reset_keyboard, stop_keyboard, payment_keyboard
from ..database import CRUDActions, UserCRUDModel


user_router = Router()


@user_router.message(StateFilter(None), Command("start"))
async def start(message: Message, state: FSMContext):
    user = UserCRUDModel(uid=message.chat.id, username=message.chat.username)
    
    if (not CRUDActions.check_user_in_db(user)):
        CRUDActions.add_user(user=user)
        
    await message.answer(
        text = f'Привет, {message.chat.username}.\n' \
               f'Я бот типографии РАНХиГС. ' \
               f'Здесь ты можешь создать онлайн-заказ, оплатить его и забрать в типографии в удобное время!\n\n' \
               f'Доступные услуги:\n' \
               f'1) Чёрно-белая печать - 8 руб/стр',
          reply_markup=ReplyKeyboardRemove()
        )
    
    await message.answer(text="Пришли сюда файл в формате PDF, который нужно распечатать")
    await state.set_state(HandleFileStates.HandleFilesState)


@user_router.message(F.content_type == ContentType.DOCUMENT, HandleFileStates.HandleFilesState)
async def handle_files(message: Message, state: FSMContext, bot: Bot):
    filename = message.document.file_name
    file_info = await bot.get_file(message.document.file_id)
    file_bytes = await bot.download_file(file_path=file_info.file_path)

    try:
        document = create_document(file_path=file_info.file_path, file_bytes=file_bytes)
        
    except ValueError:
        return await message.answer(f'Неверный формат файлов, файл должен быть формата: {ALLOWED_FORMATS}')
    
    num_pages = document.get_number_pages()
         
    file_data = FileModel(filename=filename,document=document, num_pages=num_pages, file_bytes=file_bytes)
    user_data = UserData(uid=message.chat.id, username=message.chat.username, file_data=file_data)
        
    await state.set_data({'user_data': user_data})
    await state.set_state(HandleFileStates.NumberOfCopiesState)
    
    await message.answer(
        text='Отлично, файл получен. Сколько копий файла вам нужно распечатать?\n\n'
             '(введите просто число, без лишних символов)',
        reply_markup=await stop_keyboard()
    )


@user_router.message(~(F.content_type == ContentType.DOCUMENT), HandleFileStates.HandleFilesState)
async def handle_files_error(message: Message):
    return await message.answer("Пришлите файл!")


@user_router.message(HandleFileStates.NumberOfCopiesState)
async def handle_number_of_copies(message: Message, state: FSMContext):
    try:
        num_of_copies = int(message.text)
    except ValueError:
        return await message.answer("Введите число!")
    
    data: UserData = (await state.get_data())['user_data']
    printer_capacity = await PrinterAPI.get_printer_capacity()
    total_pages = data.file_data.num_pages * num_of_copies
    
    if printer_capacity < total_pages:
        await state.clear()
        
        return await message.answer(
            f"К сожалению, мы не можем сейчас распечатать столько файлов\n\n"\
            f"В принтере не хватает листов, нужно {total_pages}, когда имеется {printer_capacity}",
            reply_markup=await reset_keyboard()
        )

    data: UserData = (await state.get_data())['user_data']
    data.value = Page.total_value(total_pages)
    
    await message.answer(
        f"Отлично! Тогда, получается:\n\n"\
        f"- {num_of_copies} копии(-й) файла {data.file_data.filename} ({data.file_data.num_pages} страниц)\n\n"
        f"Итого выйдет: {data.value} руб.",
        reply_markup=await yesno_keyboard()
    )
    

@user_router.callback_query(F.data == 'reset')
async def reset_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await start(call.message, state)


@user_router.callback_query(F.data == 'cancel_purchase')
async def reset_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(text='Покупка отменена')


@user_router.callback_query(F.data == 'make_purchase')
async def make_purchase_handler(call: CallbackQuery, state: FSMContext):
    data: UserData = (await state.get_data())['user_data']
    value = data.value
    
    payment = paymentFactory.create_payment(value=value)
    data.payment_action = payment
    link = payment.confirmation.confirmation_url
    
    await call.message.answer(
        text=f"Сумма к оплате: {value}\n"
             f"После оплаты, нажмите «Проверить оплату»",
        reply_markup=await payment_keyboard(link)
    )
        
    
@user_router.callback_query(F.data == "check_payment")
async def check_payment_handler(call: CallbackQuery, state: FSMContext):
    data: UserData = (await state.get_data())['user_data']
    payment: paymentFactory = data.payment_action
    payment_id = data.payment_id
    
    response = payment.find_payment(payment_id)
    print(f'{response.status = }\t{response.amount.value = }')
    
    if response.status == "succeeded" and data.value == response.amount.value:
        await state.clear()
        await PrinterAPI.print_files(file=data.file_data.file_bytes, num_copies=data.num_copies)
        
        return await call.message.answer(
            text="Оплата прошла успешно!\n\n"\
                 "Отправили ваш заказ в Типографию ✅\n"
            )
        
