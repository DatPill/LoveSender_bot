from random import choice
import re
import requests

from data.config import COMPLIMENT_API_URL


def init_compliment_history():  # fixme
    compliment_history: list = []

    def inner(compliment: str) -> bool:
        nonlocal compliment_history

        if compliment in compliment_history:
            return False
        else:
            compliment_history.append(compliment)
            if len(compliment_history) > 10:
                compliment_history.pop(0)
            return True
    return inner


is_new = init_compliment_history()


def get_raw_compliment() -> str:
    """Get raw compliment by ``COMPLIMENT_API_URL`` from ``.env``."""
    compliment_dict: dict = requests.get(COMPLIMENT_API_URL, params={"type": 2}).json()
    compliment_text: str = compliment_dict["text"]

    while not is_new(compliment_text):
        compliment_dict: dict = requests.get(COMPLIMENT_API_URL, params={"type": 2}).json()
        compliment_text: str = compliment_dict["text"]

    return compliment_text


def get_emoji() -> str:
    """Get emoji with whitespase before it if needed."""
    use_emoji = choice([0, 1, 1, 2])
    emojis = {
        "first": [
            "\U0001F609",
            "\U0001F60A",
            "\U0001F970",
            "\U0001F618",
            "\U0001F61A",
            "\U0001F60F",
            "\U0001F60E",
            "\U0001F92D",
            "\U0001F440",
            "\U0001F975",
        ],
        "second": [
            "\U0001F48B",
            "\U0001FAE6",
            "\U0001F4AB",
            "\U0001F31F",
            "\U00002728",
            "\U00002764",
            "\U0001FA77",
            "\U0001F9E1",
            "\U0001F49B",
            "\U0001F49A",
            "\U0001F499",
            "\U0001FA75",
            "\U0001F49C",
            "\U0001F90D",
            "\u2763\uFE0F",
            "\U0001F495",
            "\U0001F49E",
            "\U0001F493",
            "\U0001F497",
            "\U0001F496",
            "\U0001F498",
        ],
    }
    emoji = " "

    if use_emoji == 1:
        emoji += choice(emojis["first"])
    elif use_emoji == 2:
        emoji += choice(emojis["first"])
        emoji += choice(emojis["second"])

    return emoji


def get_name(compliment) -> str:
    """Choose name (silly or great) according on the ``compliment`` tone."""
    is_formal: re.Match[str] | None = (
        re.match(r"\b[Вв]ы\b", compliment)
        or re.match(r"\w*ите.*", compliment)
        or re.match(r"\b[Вв]аш.*", compliment)
    )

    names = {
        "great": ["Камилла", "Mademoiselle", "M'Lady"],
        "silly": ["Ками", "Кис", "Кисулькен", "Камилла"],
    }

    if is_formal:
        return choice(names["silly"])
    else:
        return choice(names["great"])


def get_compliment() -> str:
    """Get formatted compliment."""
    # Get raw compliment and make first letter lowercase
    raw_compliment = get_raw_compliment()
    compliment_body = raw_compliment[0].lower() + raw_compliment[1:]

    name = get_name(raw_compliment)
    emoji = get_emoji()

    return f'{name}, {compliment_body}{emoji}'
