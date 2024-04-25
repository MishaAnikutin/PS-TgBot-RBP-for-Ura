import io 
from typing import Optional
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, ContentType, CallbackQuery

from ..models.page_model import Page
from ..models.user_model import FileModel, PhotoModel, UserData
from ..file_handlers.base import BasePhoto, BaseFile

from ..states.user_states import HandleFileStates
from ..printer_api import PrinterAPI
from ..file_handlers import create_document, ALLOWED_FORMATS

from ..utils.keyboards import yesno_keyboard, stop_keyboard, payment_keyboard
from ..database import CRUDActions, UserCRUDModel

from ..states.user_states import HandleFileStates
from ..callback_data import HandleFileCallback

from ..payment import paymentFactory
from ..payment.models import CreatePaymentModel, PaymentInfoModel, PaymentStatus


user_router = Router()


@user_router.message(StateFilter(None), Command("start"))
async def start(message: Message, state: FSMContext):
    user = UserCRUDModel(uid=message.chat.id, username=message.chat.username)
    
    if (not CRUDActions.check_user_in_db(user)):
        CRUDActions.add_user(user=user)
        
    await message.answer(
        text = f'Привет, {message.chat.username}.\n' \
               f'Я бот типографии . ' \
               f'Здесь ты можешь создать онлайн-заказ, оплатить его и забрать в типографии в удобное время!\n\n' \
               f'Доступные услуги:\n' \
               f'1) Чёрно-белая печать - 8 руб/стр',
          reply_markup=ReplyKeyboardRemove()
        )
    
    await message.answer(text=f"Пришли сюда файл в формате: {', '.join(ALLOWED_FORMATS)}, который нужно распечатать")
    await state.set_state(HandleFileStates.HandleFilesState)


@user_router.callback_query(F.data == HandleFileCallback.Reset)
async def cancel(callback_query: CallbackQuery, state: FSMContext):
    '''Cancel handle and return to start'''
    await state.clear()
    return await start(callback_query.message, state) 


@user_router.message(F.content_type == ContentType.PHOTO, HandleFileStates.HandleFilesState)
async def handle_photos(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Отправьте файлом')
    # if photo_info := message.photo:
    #     photo_bytes: io.BytesIO = await bot.download(photo_info[-1])
    
    # else:
    #     await message.answer(
    #         text='Отлично, фотографии получены. Сколько копий вам нужно распечатать?\n\n'
    #             '(введите просто число, без лишних символов)',
    #         reply_markup=await stop_keyboard(callback_factory=HandleFileCallback)
    #     )

    #     return await state.set_state(HandleFileStates.NumberOfCopiesState)

    # user_data: Optional[UserData] = (await state.get_data()).get('user_data', None)
    
    # try:
    #     document: BasePhoto = create_document(file_bytes=photo_bytes, file_path='.png', num_pages=1)
    # except ValueError:
    #     await message.answer(f'Неверный формат файлов, файл должен быть формата: {", ".join(ALLOWED_FORMATS)}')
    #     return await state.clear()
        
    
    # if user_data is None:
    #     file_data = PhotoModel(filename='photo.png', document=[document], num_pages=1)
    #     user_data = UserData(uid=message.chat.id, username=message.chat.username, file_data=file_data)
    
    # else:
    #     documents: list = user_data.file_data.document + [document]
    #     num_pages = user_data.file_data.num_pages + 1
    #     file_data = PhotoModel(filename='photo.png', document=documents, num_pages=num_pages)
    #     user_data.file_data = file_data
    
    # print(user_data.file_data)
    # await state.set_data({'user_data': user_data})
    

@user_router.message(F.content_type == ContentType.DOCUMENT, HandleFileStates.HandleFilesState)
async def handle_files(message: Message, state: FSMContext, bot: Bot):
    filename = message.document.file_name
    file_info = await bot.get_file(message.document.file_id)
    file_bytes: io.BytesIO = await bot.download_file(file_path=file_info.file_path)

    try:
        document = create_document(file_path=file_info.file_path, file_bytes=file_bytes)
    
    except ValueError as exc:
        await message.answer(f'Неверный формат файлов, файл должен быть формата: {", ".join(ALLOWED_FORMATS)}')
        return await state.clear()
        
    num_pages = document.get_number_pages()

    file_data = FileModel(filename=filename,document=document, num_pages=num_pages, file_bytes=file_bytes)
    user_data = UserData(uid=message.chat.id, username=message.chat.username, file_data=file_data)
        
    await state.set_data({'user_data': user_data})
    
    await message.answer(
        text=f'Отлично, файл {filename} получен. Сколько копий файла вам нужно распечатать?\n\n'
             f'(введите просто число, без лишних символов)',
        reply_markup=await stop_keyboard(callback_factory=HandleFileCallback)
    )

    await state.set_state(HandleFileStates.NumberOfCopiesState)


async def get_document(message: Message, bot: Bot):
    filename = message.document.file_name
    file_info = await bot.get_file(message.document.file_id)
    file_bytes: io.BytesIO = await bot.download_file(file_path=file_info.file_path)

    document = create_document(file_path=file_info.file_path, file_bytes=file_bytes)
    num_pages = document.get_number_pages()

    file_data = FileModel(filename=filename,document=document, num_pages=num_pages, file_bytes=file_bytes)
    return file_data


@user_router.message(~(F.content_type == ContentType.DOCUMENT), HandleFileStates.HandleFilesState)
async def handle_files_error(message: Message):
    return await message.answer("Пришлите файл!", reply_markup=await stop_keyboard(callback_factory=HandleFileCallback))


@user_router.message(HandleFileStates.NumberOfCopiesState)
async def handle_number_of_copies(message: Message, state: FSMContext):
    try:
        num_of_copies = int(message.text)
    except ValueError:
        return await message.answer("Введите число!")
    
    data: UserData = (await state.get_data())['user_data']
    data.num_copies = num_of_copies
    
    printer_capacity = await PrinterAPI.get_printer_capacity()
    total_pages = data.file_data.num_pages * num_of_copies
    data.value = Page.total_value(total_pages)
    
    if printer_capacity < total_pages:
        await state.clear()
        
        return await message.answer(
            f"К сожалению, мы не можем сейчас распечатать столько файлов\n\n"\
            f"В принтере не хватает листов, нужно {total_pages}, когда имеется {printer_capacity}",
            reply_markup=await stop_keyboard(callback_factory=HandleFileCallback, text='Назад')
        )

    await state.set_data({'user_data': data})
    await message.answer(
        f"Отлично! Тогда, получается:\n\n"\
        f"- {num_of_copies} копии(-й) файла {data.file_data.filename} ({data.file_data.num_pages} страниц)\n\n"
        f"Итого выйдет: {data.value} руб.",
        reply_markup=await yesno_keyboard()
    )
    

@user_router.callback_query(F.data == HandleFileCallback.CancelPurchase)
async def reset_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(text='Покупка отменена')


@user_router.callback_query(F.data == HandleFileCallback.MakePurchase)
async def make_purchase_handler(call: CallbackQuery, state: FSMContext):
    data: UserData = (await state.get_data())['user_data']
    value = data.value
    
    payment: CreatePaymentModel = await paymentFactory.create_payment(value=value)
    
    link = payment.Data.paymentLink
    data.payment_id = payment.Data.operationId
    
    await call.message.answer(
        text=f"Сумма к оплате: {value}\n"
             f"После оплаты, нажмите «Проверить оплату»",
        reply_markup=await payment_keyboard(link)
    )
        
    
@user_router.callback_query(F.data == HandleFileCallback.CheckPayment)
async def check_payment_handler(call: CallbackQuery, state: FSMContext):
    data: UserData = (await state.get_data())['user_data']
    payment_information = await paymentFactory.get_payment_information(payment_id=data.payment_id)

    # FIXME: неправильно парсится Operation, как list
    payment_status = payment_information.Data.Operation[0]['status'] 
        
    match payment_status:
        case PaymentStatus.APPROVED:            
            try:
                await PrinterAPI.print_files(file=data.file_data.file_bytes, num_copies=data.num_copies)
            except Exception as exc:
                await call.message.answer(f"Произошла непредвиденная ошибка:\n\n{exc}\nОтправили запрос на возврат средств, напишите в техподдержку")
                await paymentFactory.refund_payment(payment_id=data.payment_id, amount=data.value) 
            else:
                await call.message.answer(text="Оплата прошла успешно!\n\nОтправили файлы на принтер ✅")
            await state.clear()
        
        case PaymentStatus.CREATED:
            await call.message.answer(text="Оплата еще не прошла прошла")
            
        case PaymentStatus.EXPIRED:
            await call.message.answer(text="Истек срок действия оплаты, перенаправляем новую ссылку")
            await state.set_state(HandleFileCallback.MakePurchase)
            await make_purchase_handler(call=call, state=state)
        
        case _:
            print('ээээээ хз че это')
            
