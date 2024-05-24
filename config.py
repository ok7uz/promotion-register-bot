from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN', None)
DB_NAME = getenv('DB_NAME', None)
ADMIN_USERNAME = 'chikako_admin_1'

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
