import os
from urllib.parse import quote

class Config(object):
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
    DATABASE_URI = os.environ.get('DATABASE_URL', "")
    WEBSITE_URL = os.environ.get('WEBSITE_URL', '')