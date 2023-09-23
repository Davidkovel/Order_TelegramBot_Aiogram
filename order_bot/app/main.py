import asyncio
from aiogram import Bot, Dispatcher
from handlers.basic import basic_router
from handlers.shipping_invoice import shipping_invoice_router
from handlers.payment import payment_receipt_router
from handlers.search import search_router
from handlers.nova_post_ttn import post_router
from handlers.recipent import recipent_router
from db.db import Repo
from config import TOKEN


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(basic_router)
    dp.include_router(shipping_invoice_router)
    dp.include_router(payment_receipt_router)
    dp.include_router(post_router)
    dp.include_router(search_router)
    dp.include_router(recipent_router)
    await Repo().create_table()
    await dp.start_polling(bot)
    


if __name__ == "__main__":
    asyncio.run(main())