from os import getenv
from dotenv import load_dotenv
from aiogram.types import BotCommand

from bot.texts import *

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN', None)
DB_NAME = getenv('DB_NAME', None)
ADMINS = list(map(int, getenv('ADMINS', '').split(',')))
ADMIN_USERNAME = 'chikako_admin_1'

USER_COMMANDS = [
    BotCommand(command="/start", description=START_COMMAND_DESCRIPTION),
    BotCommand(command="/mypromos", description=MYPROMOS_COMMAND_DESCRIPTION),
    BotCommand(command="/help", description=HELP_COMMAND_DESCRIPTION),
]

ADMIN_COMMANDS = [
    BotCommand(command="/start", description=START_COMMAND_DESCRIPTION),
    BotCommand(command="/mypromos", description=MYPROMOS_COMMAND_DESCRIPTION),
    BotCommand(command="/help", description=HELP_COMMAND_DESCRIPTION),
    BotCommand(command="/export", description=EXPORT_COMMAND_DESCRIPTION),
    BotCommand(command="/block", description=BLOCK_COMMAND_DESCRIPTION),
]

CHANNELS = [
    {
        'name': 'Telegram',
        'link': 'https://t.me/Orikzor_supermarket'
    },
    {
        'name': 'Instagram',
        'link': 'https://www.instagram.com/chikako_bukhara?igsh=bGhlcHM5amUxdmwx'
    }
]
