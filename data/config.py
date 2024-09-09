from typing import Final

from dotenv import dotenv_values


config = dotenv_values()

BOT_TOKEN: Final[str] = str(config['BOT_TOKEN'])

COMPLIMENT_API_URL: Final[str] = str(config['COMPLIMENT_API_URL'])
CATPICS_API_URL: Final[str] = str(config['CATPICS_API_URL'])
DOGPICS_API_URL: Final[str] = str(config['DOGPICS_API_URL'])
FOXPICS_API_URL: Final[str] = str(config['FOXPICS_API_URL'])

DB_URL: Final[str] = str(config['DB_URL'])
