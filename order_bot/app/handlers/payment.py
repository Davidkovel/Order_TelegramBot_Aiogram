from aiogram import F, Router, Bot
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext
from app.keyboards.reply import main_markup, menu
from app.states.order_states import PaymentReceipt  # Импортируйте правильный класс состояния
from app.db.db import Repo

payment_receipt_router = Router()

@payment_receipt_router.message(PaymentReceipt.photo)
async def add_photo(message: Message, state: FSMContext, bot: Bot):
    if message.content_type == ContentType.PHOTO:
        img_id = message.photo[-1].file_id
        await bot.download(img_id, f"images/{img_id}_photo.png")
        order = await Repo().add_record(user_id=message.from_user.id, open_=True, photo=f"images/{img_id}_photo.png")
        await message.answer(text="Отправьте скриншот")
        await state.set_state(PaymentReceipt.screenshot)
        await state.update_data({"order": order})
    else:
        await message.answer(text="Отправьте тип файла фото")

@payment_receipt_router.message(PaymentReceipt.screenshot)
async def add_screenshot(message: Message, state: FSMContext, bot: Bot):
    if message.content_type == ContentType.PHOTO:
        data = await state.get_data()
        order = data["order"]
        img_id = message.photo[-1].file_id
        await bot.download(img_id, f"images/{img_id}_screen.png")
        await Repo().add_screen(id=order[0], value=f"images/{img_id}_screen.png")
        await message.answer(text="Введите текст")
        await state.set_state(PaymentReceipt.text)
    else:
        await message.answer(text="Отправьте тип файла фото")


@payment_receipt_router.message(PaymentReceipt.text)
async def add_text(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    order = data["order"]
    await Repo().add_text(id=order[0], value=f"{message.text}")
    await message.answer(text="Ваша квитанция сохранена", reply_markup=menu)
    await state.clear()
