from random import randint

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot
from aiogram.types import URLInputFile

from db.requests import get_daily_userdata
from utils.compliments import get_compliment
from utils.get_pic import get_catpic_url, get_dogpic_url, get_foxpic_url


async def reschedule_daily_compliment(random_compliment_job: Job):
    hour = randint(0, 23)
    minute = randint(0, 59)

    random_compliment_job.reschedule(trigger='cron',  year='*', month='*', day='*',
                                     hour=hour, minute=minute, second=0)


async def send_daily_love(bot: Bot):
    users_data: list = await get_daily_userdata()
    compliment = get_compliment()

    for user in users_data:
        tg_id = user['tg_id']
        animal = user['animal']
        photo_url = None

        if animal == 'cat':
            photo_url = get_catpic_url()
        elif animal == 'dog':
            photo_url = get_dogpic_url()
        elif animal == 'fox':
            photo_url = get_foxpic_url()

        if photo_url:
            photo = URLInputFile(photo_url)
            await bot.send_photo(chat_id=tg_id, photo=photo, caption=compliment)
        else:
            await bot.send_message(chat_id=tg_id, text=compliment)


async def start_daily_jobs(bot: Bot) -> None:
    """Run all daily jobs for ``Bot`` instance"""
    daily_scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

    # Init daily_random_compliment_job
    daily_random_compliment_job = daily_scheduler.add_job(
        func=send_daily_love, args=(bot,),
        trigger='cron',
        year='*', month='*', day='*',
        hour=str(randint(0, 23)),
        minute=str(randint(0, 59)),
        second='0'
    )

    # Reschedule random_compliment_job every day
    daily_scheduler.add_job(
        func=reschedule_daily_compliment, args=(daily_random_compliment_job,),
        trigger='cron',
        year='*', month='*', day='*',
        hour='0', minute='0', second='0'
    )

    daily_scheduler.start()
