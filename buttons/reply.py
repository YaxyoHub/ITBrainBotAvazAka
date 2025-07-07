from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Telefon raqam ulashish", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)