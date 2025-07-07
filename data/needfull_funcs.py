from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from database.get_sql import get_admins, get_user

class IsAdmin(BaseFilter):
    async def __call__(self, obj: Message | CallbackQuery, bot: Bot) -> bool:
        admins = [admin[3] for admin in get_admins()]
        return obj.from_user.id in admins

class IsUser(BaseFilter):
    async def __call__(self, obj: Message | CallbackQuery, bot: Bot) -> bool:
        users = [user[3] for user in get_user()]
        return obj.from_user.id in users
