import os
from dotenv import load_dotenv
from database.get_sql import get_admins
load_dotenv()

ADMIN_ID = [admin[3] for admin in get_admins()]


from aiogram import Dispatcher, Bot

bottoken = os.getenv("API_TOKEN")
bot = Bot(bottoken)

dp = Dispatcher()