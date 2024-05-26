from os import getenv
from dotenv import load_dotenv
from aiogram.types import BotCommand
from typing import List, Dict, Any

from bot.texts import (START_COMMAND_DESCRIPTION, MYPROMOS_COMMAND_DESCRIPTION, 
                       HELP_COMMAND_DESCRIPTION, EXPORT_COMMAND_DESCRIPTION, 
                       BLOCK_COMMAND_DESCRIPTION)

load_dotenv()

BOT_TOKEN: str = getenv('BOT_TOKEN')
DB_NAME: str = getenv('DB_NAME')
ADMIN_IDS: str = getenv('ADMINS', '')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables")
if not DB_NAME:
    raise ValueError("DB_NAME is not set in environment variables")

try:
    ADMINS: List[int] = list(map(int, ADMIN_IDS.split(','))) if ADMIN_IDS else []
except ValueError as e:
    raise ValueError("Error converting ADMINS to list of integers") from e

ADMIN_USERNAME: str = 'chikako_admin_1'

USER_COMMANDS: List[BotCommand] = [
    BotCommand(command="/start", description=START_COMMAND_DESCRIPTION),
    BotCommand(command="/mypromos", description=MYPROMOS_COMMAND_DESCRIPTION),
    BotCommand(command="/help", description=HELP_COMMAND_DESCRIPTION),
]

ADMIN_COMMANDS: List[BotCommand] = [
    BotCommand(command="/start", description=START_COMMAND_DESCRIPTION),
    BotCommand(command="/mypromos", description=MYPROMOS_COMMAND_DESCRIPTION),
    BotCommand(command="/help", description=HELP_COMMAND_DESCRIPTION),
    BotCommand(command="/export", description=EXPORT_COMMAND_DESCRIPTION),
    BotCommand(command="/block", description=BLOCK_COMMAND_DESCRIPTION),
]

CHANNELS: List[Dict[str, Any]] = [
    {
        'name': 'Telegram',
        'link': 'https://t.me/Orikzor_supermarket'
    },
    {
        'name': 'Instagram',
        'link': 'https://www.instagram.com/chikako_bukhara?igsh=bGhlcHM5amUxdmwx'
    }
]
