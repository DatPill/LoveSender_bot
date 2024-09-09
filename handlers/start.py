from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from emoji import emojize
from asyncio import sleep

from db.requests import create_user
from keyboards.simple_row import make_row_keyboard
from states.user_states import UserCreation


router = Router()


@router.message(CommandStart())
async def process_start_cmd(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.set_state(UserCreation.setting_daily_compliment)
    await state.update_data(tg_id=message.from_user.id)

    greeting = emojize(
        'Привет, кис! :eyes:\n'
        '\n'
        'Я чета посидел, посидел, и родил вот такую штуку - этого вот бота.\n'
        'Этот бот может отправлять тебе комплименты, например, когда я занят. Или просто когда тебе '
        'захочется. Делать это он может как <b>по запросу</b> (команда <b>/love</b>), так и '
        '<b>ежедневно</b> в случайное время (вкл/выкл командой <b>/daily</b>).\n'
    )
    await message.answer(greeting)
    await bot.send_sticker(
        chat_id=message.from_user.id,
        sticker='CAACAgEAAxkBAAEqDcFl6HF7QSIqDI6U2KeSZuktuBeo_AAC1AIAAjGR2UUOiF9SNv04CDQE'
    )
    await sleep(2.4)
    await message.answer(
        'Хочешь получать ежедневные комплименты?',
        reply_markup=make_row_keyboard(['Да', 'Нет'], 'Хочешь получать ежедневные комплименты?')
    )


@router.message(UserCreation.setting_daily_compliment, F.text.casefold().in_({'да', 'нет'}))
async def daily_compliment_state(message: Message, state: FSMContext) -> None:
    send_daily: bool = True if message.text.casefold() == 'да' else False
    await state.update_data(send_daily=send_daily)

    await state.set_state(UserCreation.choosing_animal)
    await message.answer('Отличненько! Это настроили, идём дальше)', reply_markup=ReplyKeyboardRemove())
    await sleep(1)
    await message.answer('Помимо сообщений этот бот может присылать ещё и картинки каких-нибудь животных. '
                         'Чтобы выбрать животное - возпользуйся кнопками ниже!',
                         reply_markup=make_row_keyboard(['Кисун', 'Собакен', 'Лиса', 'Не хочу получать животных >:['], 'Выбери свое животное:')
    )


@router.message(UserCreation.setting_daily_compliment)
async def daily_state_incorrect(message: Message, state: FSMContext) -> None:
    await message.reply('Я тебя не понимаю :(\n\n'
                         'Лучше используй кнопки снизу!',
                         reply_markup=make_row_keyboard(['Да', 'Нет'], 'Хочешь получать ежедневные комплименты?')
    )


@router.message(UserCreation.choosing_animal, F.text.casefold().in_({'кисун', 'собакен', 'лиса', 'не хочу получать животных >:['}))
async def animal_choosing_state(message: Message, state: FSMContext) -> None:
    message_animal: str = message.text.casefold()
    if message_animal == 'кисун':
        animal = 'cat'
    elif message_animal == 'собакен':
        animal = 'dog'
    elif message_animal == 'лиса':
        animal = 'fox'
    else:
        animal = None

    await state.update_data(animal=animal)

    user_data: dict = await state.get_data()
    await create_user(user_data['tg_id'], user_data['send_daily'], user_data['animal'])

    registration_end_text = emojize(
        f'Отлично! На этом регистрация закончена! :smiling_face_with_sunglasses:\n\n'
        f'Ты {'не' if not user_data['send_daily'] else ''} будешь получать комплименты каждый день!'
    )
    if animal:
        registration_end_text += f'\n\nТвоё животное сейчас: <i>{message_animal}</i> ;)'

    await message.answer(registration_end_text, reply_markup=ReplyKeyboardRemove())
    await sleep(1.1)
    await message.answer('Чтобы включить/выключить ежедневный комплимент - просто напиши <b><i>/daily</i></b>\n'
                         'Чтобы изменить или убрать животное - используй команду <b><i>/animal</i></b>'
    )
    await state.clear()

@router.message(UserCreation.choosing_animal)
async def animal_state_incorrect(message: Message, state: FSMContext) -> None:
    await message.reply('Я тебя не понимаю :(\n\n'
                         'Лучше используй кнопки снизу!',
                         reply_markup=make_row_keyboard(['Кисун', 'Собакен', 'Лиса', 'Не хочу получать животных >:['], 'Выбери свое животное:')
    )
