from vkbottle import API, Bot
from vkbottle.bot import BotLabeler
import os


def environ_get(key: str, default=""):
    e = os.environ.get(key, default)
    if not e:
        raise ValueError(f"{key} is not set")
    return e

TOKEN = environ_get("TOKEN")
DB_NAME = environ_get("DB_NAME")
DB_USER = environ_get("DB_USER")
DB_PASSWORD = environ_get("DB_PASSWORD")
DB_HOST = environ_get("DB_HOST")
DB_PORT = environ_get("DB_PORT")
# = environ_get("")

api = API(TOKEN)
labeler = BotLabeler()

bot = Bot(
    api=api,
    labeler=labeler,
)


