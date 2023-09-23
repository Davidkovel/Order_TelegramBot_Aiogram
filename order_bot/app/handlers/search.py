from aiogram import F, Router, Bot
from aiogram.types import Message, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext
from app.keyboards.reply import main_markup, menu
from app.states.order_states import GetClose, GetOpen
from app.db.db import Repo

search_router = Router()

@search_router.message(GetOpen.user)
async def get_open(message: Message, state: FSMContext, bot: Bot):
    try:
        int(message.text)
    except KeyError:
        return await message.answer(text="Айди некоректный")
    # orders = await Repo().get_all_records(open_=True, id=int(message.text))
    a = int(message.text)
    # if print(Repo().check(user_id=a)):
    #     a = await Repo().set_all_records_open(user_id=a)
    #     print('---\n', a)
    #     await message.answer("У этого пользователя нету открытых накладных", reply_markup=menu)
    #     return
    # else:
    orders = await Repo().get_all_records(open_=True, id=int(message.text))
    print(len(orders))

    if orders == [] or orders is None:
        return await message.answer("У этого пользователя нету открытых накладных", reply_markup=menu)

    if len(orders) == 4:
        await Repo().set_all_records_close(user_id=a)
        orders = []
        if orders == [] or orders is None:
            return await message.answer("У этого пользователя нету открытых накладных", reply_markup=menu)
        return
    # elif len(orders) > 4:
    #         await Repo().set_all_records_close(user_id=a)
    #         orders = []
    #         if orders == [] or orders is None:
    #             return await message.answer("У этого пользователя нету открытых накладных", reply_markup=menu)
    #         return

    for order in orders:
        try:
            media_group = []

            if order[3] is not None:
                media_group.append(InputMediaPhoto(media=FSInputFile(order[3])))

            if order[4] is not None:
                media_group.append(InputMediaPhoto(media=FSInputFile(order[4])))

            if media_group:
                await message.answer_media_group(media_group)
        except TypeError:
            continue

        if order[-3] is None:
            await message.answer(text="Без текста")
        else:
            await message.answer(text=order[-3])


@search_router.message(GetClose.user)
async def get_close(message: Message, state: FSMContext, bot: Bot):
    try:
        int(message.text)
    except KeyError:
        return await message.answer(text="Айди некоректный")
    orders = await Repo().get_all_records(open_=False, id=int(message.text))
    if orders == [] or orders is None:
        return await message.answer("У этого пользователя нету закрытых накладных", reply_markup=menu)
    for order in orders:
        try:
            media_group = []

            if order[3] is not None:
                media_group.append(InputMediaPhoto(media=FSInputFile(order[3])))

            if order[4] is not None:
                media_group.append(InputMediaPhoto(media=FSInputFile(order[4])))

            if media_group:
                await message.answer_media_group(media_group)
        except TypeError:
            continue
        if order[-3] is None:
            await message.answer(text="Без текста")
        else:
            await message.answer(text=order[-3])