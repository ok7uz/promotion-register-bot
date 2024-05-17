from aiogram import Dispatcher

from .commands import command_router
from .registration import registration_router
from .messages import message_router


async def setup(dp: Dispatcher):
    dp.include_routers(
        command_router,
        registration_router,
        message_router
    )
