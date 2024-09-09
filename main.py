import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from data.config import BOT_TOKEN
from db.models import async_main
from utils.daily_scheduler import start_daily_jobs
from handlers import get_compliment, start, animal_pics


async def main():
    # Connecting to database
    await async_main()

    # Set up logging
    # logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.INFO)
    logging.basicConfig(encoding='utf-8', level=logging.INFO)

    # Bot and dispatcher init
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage(), bot=bot)

    # Indlude all routers
    dp.include_routers(
        start.router,
        get_compliment.router,
        animal_pics.router,
    )

    # Start scheduler
    await start_daily_jobs(bot)

    # Starting polling without pending updates
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error('Bot stopped!')
