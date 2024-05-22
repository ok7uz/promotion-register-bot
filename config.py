from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN', None)
DB_NAME = getenv('DB_NAME', None)
ADMIN_USERNAME = 'admin'

CHANNELS = [
    {
        'name': 'Telegram',
        'link': 'http://t.me/Orikzor_supermarket'
    },
    {
        'name': 'Instagram',
        'link': 'https://www.instagram.com/chikako_bukhara?igsh=bGhlcHM5amUxdmwx'
    }
]
