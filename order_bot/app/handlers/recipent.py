from aiogram import F, Router, Bot
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext
from app.keyboards.reply import main_markup, menu
from app.states.order_states import ReceivedInvoiceScreenshot
from app.db.db import Repo

recipent_router = Router()

@recipent_router.message(ReceivedInvoiceScreenshot.screenshot)
async def add_screen_nvoices(message: Message, state: FSMContext, bot: Bot):
    if message.content_type == ContentType.PHOTO:
        img_id = message.photo[-1].file_id
        await bot.download(img_id, f"images/{img_id}_photo.png")
        await Repo().add_record(user_id=message.from_user.id, open_=True, screenshot=f"images/{img_id}_photo.png")
        await message.answer(text="Ваша накладная сохранена", reply_markup=menu)

    else:
        await message.answer(text="Отправьте тип файла фото")