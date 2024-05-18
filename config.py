from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN', None)
DB_NAME = getenv('DB_NAME', None)

CHANNELS = [
    {
        'name': 'Sport TV',
        'link': 'https://t.me/SportTV'
    },
    {
        'name': 'Chikako',
        'link': 'https://t.me/Chikako'
    }
]
