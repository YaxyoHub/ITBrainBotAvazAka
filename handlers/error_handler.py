from aiogram import F, Router
from aiogram.types import Message

error_router = Router()

@error_router.message(F.text)
async def error_cmd(message: Message):
    await message.reply("⚠️ Iltimos botga to'g'ridan-to'g'r xabar yubormang")
