from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from admin_buttons.reply import admin_menu
from data.needfull_funcs import IsAdmin

admin_router = Router()

@admin_router.message(Command('admin'), IsAdmin())
async def admin_cmd(message: Message):
    await message.reply("Salom Admin", reply_markup=admin_menu)