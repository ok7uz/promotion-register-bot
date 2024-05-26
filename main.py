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
    try:
        await bot.set_my_commands(USER_COMMANDS, scope=BotCommandScopeDefault())
        for admin_user_id in ADMINS:
            await bot.set_my_commands(ADMIN_COMMANDS, scope=BotCommandScopeChat(chat_id=admin_user_id))
        logger.info("Commands set successfully")
    except Exception as e:
        logger.error(f"Error setting commands: {e}")


async def on_startup():
    try:
        await logging.setup_logging()
        logger.info("Configuring database ...")
        await database.setup()
        logger.info("Configuring handlers ...")
        await handlers.setup(dp)
        logger.info("Startup complete")
    except Exception as e:
        logger.error(f"Error during startup: {e}")


async def on_shutdown():
    try:
        logger.info("Shutting down ...")
        await database.close()
        logger.info("Shutdown complete")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    logger.debug("Settings commands ...")
    await set_commands(bot)
    logger.debug("Start polling ...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
