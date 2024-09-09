from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, URLInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from utils.get_pic import get_catpic_url, get_dogpic_url, get_foxpic_url
from db.requests import change_user_animal
from keyboards.simple_row import make_row_keyboard
from states.user_states import UserEditing


router = Router()

@router.message(Command('cat'))
async def process_cat_cmd(message: Message) -> None:
    await message.bot.send_chat_action(chat_id=message.chat.id, action='upload_photo')

    photo_url = get_catpic_url()
    photo = URLInputFile(photo_url)

    await message.answer_photo(photo)


@router.message(Command('dog'))
async def process_dog_cmd(message: Message) -> None:
    await message.bot.send_chat_action(chat_id=message.chat.id, action='upload_photo')

    photo_url = get_dogpic_url()
    photo = URLInputFile(photo_url)

    await message.answer_photo(photo)


@router.message(Command('fox'))
async def process_fox_cmd(message: Message) -> None:
    await message.bot.send_chat_action(chat_id=message.chat.id, action='upload_photo')

    photo_url = get_foxpic_url()
    photo = URLInputFile(photo_url)

    await message.answer_photo(photo)


@router.message(Command('animal'))
async def process_animal_cmd(message: Message, state: FSMContext) -> None:
    await state.set_state(UserEditing.changing_animal)
    await message.answer('Выбери животное, которое хочешь получать:',
                         reply_markup=make_row_keyboard(['Кисун', 'Собакен', 'Лиса', 'Не хочу получать животных >:[', 'Отмена'], 'Выбери свое животное:')
    )


@router.message(UserEditing.changing_animal, F.text.casefold() == 'отмена')
async def cancel_animal_change(message: Message, state: FSMContext) -> None:
    await message.answer('Отмена изменения животного...', reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(UserEditing.changing_animal, F.text.casefold().in_({'кисун', 'собакен', 'лиса', 'не хочу получать животных >:['}))
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

    if animal:
        answer_text: str = f'Отлично! Животное успешно изменено. Сейчас твой выбор - <i>{message_animal}</i>.'
    else:
        answer_text: str = f'Животное успешно сброшено ;)'
    await message.answer(answer_text, reply_markup=ReplyKeyboardRemove())
    await change_user_animal(message.from_user.id, animal)
    await state.clear()


@router.message(UserEditing.changing_animal)
async def editing_anial_incorrect(message: Message) -> None:
    await message.reply('Я тебя не понимаю :(\n\n'
                        'Лучше используй кнопки снизу!',
                         reply_markup=make_row_keyboard(['Кисун', 'Собакен', 'Лиса', 'Не хочу получать животных >:['], 'Выбери свое животное:')
    )
