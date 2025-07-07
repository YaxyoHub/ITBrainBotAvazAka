from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from database.get_sql import check_user
from buttons.inline import user_menu


start_router = Router()

@start_router.message(CommandStart())
async def start_cmd(message: Message):
    result = check_user(message.from_user.id)
    if not result:
        return await message.reply(f"⚠️ Siz ushbu botdan foydalana olmaysiz\n"
                            f"Chunki siz foydalanuvchilar ro'yxatida yo'qsiz")
    await message.reply(f"👋 Salom {message.from_user.first_name}\n\n"
                        "Marhamat 🤗", reply_markup=user_menu)