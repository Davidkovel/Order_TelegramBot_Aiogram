from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.keyboards.reply import main_markup, order_markup, admin_markup, menu
from app.states.order_states import (ShippingInvoice,
                                 NovaPoshtaTtn, 
                                 PaymentReceipt, 
                                 ReceivedInvoiceScreenshot,
                                 GetOpen, GetClose)
from app.config import ADMIN_LIST

basic_router = Router()

@basic_router.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer(text=f'Здравствуйте, {message.from_user.full_name}!\nВыберите действие', reply_markup=menu)

@basic_router.message(F.text == 'Меню')
async def menu_command(message: Message):
    if str(message.from_user.id) in ADMIN_LIST:
        markup = admin_markup
    else:
        markup = main_markup
    await message.answer("Выберите пункт ниже", reply_markup=markup)


@basic_router.message(F.text == 'Создать накладную')
async def choise_invoices(message: Message):
    await message.reply('Выберите форму', reply_markup=order_markup)

@basic_router.message(F.text == 'Открытые накладные')
async def open_invoices(message: Message, state: FSMContext):
    if str(message.from_user.id) in ADMIN_LIST:
        await message.reply('Введите айди пользователя')
        await state.set_state(GetOpen.user)
    else:
        return await message.answer(text="Вы не админ")

@basic_router.message(F.text == 'Закрытые накладные')
async def close_invoices(message: Message, state: FSMContext):
    if str(message.from_user.id) in ADMIN_LIST:
        await message.reply('Введите айди пользователя')
        await state.set_state(GetClose.user)
    else:
        return await message.answer(text="Вы не админ")
    
@basic_router.message(F.text == 'Накладная с товаром')
async def create_invoice_good(message: Message, state: FSMContext):
    await message.reply('Отправьте фото', reply_markup=order_markup)
    await state.set_state(ShippingInvoice.photo)

@basic_router.message(F.text == 'Квитанция об оплате')
async def create_invoice_payment(message: Message, state: FSMContext):
    await message.reply('Отправьте фото', reply_markup=order_markup)
    await state.set_state(PaymentReceipt.photo)

@basic_router.message(F.text == 'ТТН новой почты')
async def create_invoice_ttn(message: Message, state: FSMContext):
    await message.reply('Отправьте фото', reply_markup=order_markup)
    await state.set_state(NovaPoshtaTtn.photo)

@basic_router.message(F.text == 'Скрин оприходованной накладной\nпосле получения на почте')
async def create_invoic_post(message: Message, state: FSMContext):
    await message.reply('Отправьте скрин', reply_markup=order_markup)
    await state.set_state(ReceivedInvoiceScreenshot.screenshot)