from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, URLInputFile
from emoji import emojize

from db.requests import change_daily, get_user_animal
from utils.compliments import get_compliment
from utils.get_pic import get_catpic_url, get_dogpic_url, get_foxpic_url


router = Router()

@router.message(Command('love'))    # TODO check if in db
async def process_love_cmd(message: Message) -> None:
    bot = message.bot
    compliment = get_compliment()
    user_animal = await get_user_animal(message.from_user.id) # type: ignore
    photo_url = None

    if user_animal == 'cat':
        await bot.send_chat_action(chat_id=message.chat.id, action='upload_photo')
        photo_url = get_catpic_url()
    elif user_animal == 'dog':
        await bot.send_chat_action(chat_id=message.chat.id, action='upload_photo')
        photo_url = get_dogpic_url()
    elif user_animal == 'fox':
        await bot.send_chat_action(chat_id=message.chat.id, action='upload_photo')
        photo_url = get_foxpic_url()

    if photo_url:
        photo = URLInputFile(photo_url)
        await message.answer_photo(photo=photo, caption=compliment)
    else:
        await message.answer(compliment)




@router.message(Command('compliment'))
async def process_compliment_cmd(message: Message) -> None:
    compliment = get_compliment()
    await message.answer(compliment)


@router.message(Command('daily'))
async def process_daily_cmd(message: Message) -> None:
    daily_status: bool = await change_daily(message.from_user.id) # type: ignore

    if daily_status:
        reply_text: str = ('Теперь ты будешь получать комплименты и фотки с котиками каждый день '
                           ':OK_hand:\n\n'
                           '<i>(чтобы отключить - введи команду <b>/daily</b>)</i>')

    else:
        reply_text: str = ('Теперь бот не будет отсылать комплименты '
                           '(а вот лично я - вполне себе буду :winking_face:)\n\n'
                           '<i>(чтобы включить обратно - введи команду <b>/daily</b>)</i>')



    await message.answer(emojize(reply_text))
