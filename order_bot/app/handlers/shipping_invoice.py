from aiogram import F, Router, Bot
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext
from app.keyboards.reply import main_markup, menu
from app.states.order_states import ShippingInvoice
from app.db.db import Repo

shipping_invoice_router = Router()


@shipping_invoice_router.message(ShippingInvoice.photo)
async def add_photo(message: Message, state: FSMContext, bot: Bot):
    if message.content_type == ContentType.PHOTO:
        img_id = message.photo[-1].file_id
        await bot.download(img_id, f"images/{img_id}_photo.png")
        order = await Repo().add_record(user_id=message.from_user.id, open_=True, photo=f"images/{img_id}_photo.png")
        await message.answer(text="Отправьте скриншот")
        await state.set_state(ShippingInvoice.screenshot)
        await state.update_data({"order": order})
    else:
        await message.answer(text="Отправьте тип файла фото")

@shipping_invoice_router.message(ShippingInvoice.screenshot)
async def add_photo(message: Message, state: FSMContext, bot: Bot):
    if message.content_type == ContentType.PHOTO:
        data = await state.get_data()
        order = data["order"]
        img_id = message.photo[-1].file_id
        await bot.download(img_id, f"images/{img_id}_screen.png")
        await Repo().add_screen(id=order[0], value=f"images/{img_id}_screen.png")
        await message.answer(text="Ваша накладная записана", reply_markup=menu)
        await state.clear()
    else:
        await message.answer(text="Отправьте тип файла фото")