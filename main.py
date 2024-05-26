import asyncio
from aiogram import Bot
from aiogram.types import BotCommandScopeDefault, BotCommandScopeChat
from loguru import logger
from dotenv import load_dotenv

from config import ADMIN_COMMANDS, ADMINS, USER_COMMANDS

load_dotenv()

from bot import handlers, database, logging
from bot.misc import dp, bot


async def set_commands(bot: Bot):
    await bot.set_my_commands(USER_COMMANDS, scope=BotCommandScopeDefault())

    for admin_user_id in ADMINS:
        await bot.set_my_commands(ADMIN_COMMANDS, scope=BotCommandScopeChat(chat_id=admin_user_id))


async def on_startup():
    await logging.setup()
    logger.info("Configure database ...")
    await database.setup()
    logger.info("Configure handlers ...")
    await handlers.setup(dp)


async def on_shutdown():
    logger.info("Shutting down ...")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    logger.debug("Settings commands ...")
    await set_commands(bot)
    logger.debug("Start polling ...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
