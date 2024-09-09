from aiogram.types import URLInputFile

import requests
from data.config import CATPICS_API_URL, DOGPICS_API_URL, FOXPICS_API_URL


def get_catpic_url() -> str:
    """Returns URL of cat picture"""
    result: requests.Response = requests.get(CATPICS_API_URL)

    while result.status_code != 200:
        print('===')
        print('inner')
        print('===')
        result: requests.Response = requests.get(CATPICS_API_URL)

    catpic_url: str = result.json()[0]['url']
    return catpic_url


def get_dogpic_url() -> str:
    """Returns URL of dog picture"""
    result: requests.Response = requests.get(DOGPICS_API_URL)

    while result.status_code != 200:
        result: requests.Response = requests.get(DOGPICS_API_URL)

    dogpic_url: str = result.json()['url']
    return dogpic_url


def get_foxpic_url() -> str:
    """Returns URL of fox picture"""
    result: requests.Response = requests.get(FOXPICS_API_URL)

    while result.status_code != 200:
        result: requests.Response = requests.get(FOXPICS_API_URL)

    dogpic_url: str = result.json()['image']
    return dogpic_url


async def get_animal_url(animal: str) -> URLInputFile | None:
    ... # TODO
