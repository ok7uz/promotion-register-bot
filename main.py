import asyncio
import logging

from aiogram import Bot
from bot import handlers, database
from aiogram.types import BotCommand
from bot.misc import dp, bot
from bot.texts import START_COMMAND_DESCRIPTION


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description=START_COMMAND_DESCRIPTION),
        BotCommand(command="/list", description="Get help information"),
    ]
    await bot.set_my_commands(commands)


async def on_startup():
    await database.setup()
    logging.info("Configure handlers ...")
    await handlers.setup(dp)


async def on_shutdown():
    logging.info("Shutting down ...")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
