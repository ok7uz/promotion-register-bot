import asyncio
from aiogram import Bot
from aiogram.types import BotCommand
from loguru import logger

from bot import handlers, database, logging
from bot.misc import dp, bot
from bot.texts import *


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description=START_COMMAND_DESCRIPTION),
        BotCommand(command="/mypromos", description=MYPROMOS_COMMAND_DESCRIPTION),
        BotCommand(command="/help", description=HELP_COMMAND_DESCRIPTION),
    ]
    print(commands)
    await bot.set_my_commands(commands)


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
