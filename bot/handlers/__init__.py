from aiogram import Dispatcher

from .block_user import router
from .commands import command_router
from .registration import registration_router
from .promo import promo_router
from .send_message import message_router


async def setup(dp: Dispatcher):
    dp.include_routers(
        command_router,
        registration_router,
        promo_router,
        router,
        message_router
    )
