from tortoise import Tortoise

from config import DB_NAME

TORTOISE_ORM = {
    "connections": {
        "default": f"sqlite://{DB_NAME}"
    },
    "apps": {
        "models": {
            "models": ["bot.models"],
            "default_connection": "default",
        },
    },
}


async def setup():
    await Tortoise.init(TORTOISE_ORM)
    await Tortoise.generate_schemas()
