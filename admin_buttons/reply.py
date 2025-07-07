from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Dars qo‘shish"), KeyboardButton(text="🗑 Dars o‘chirish")],
        [KeyboardButton(text="➕ Foydalanuvchi qo'shish"), KeyboardButton(text="➕ Admin qo'shish")],
        [KeyboardButton(text="✍️ Talabalarga xabar yuborish")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)