from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.get_sql import get_lesson

user_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📝 Mavzular ro'yxati", callback_data="list_lesson")],
        [InlineKeyboardButton(text="❔ Ustozga savol", callback_data="question_admin")]
    ]
)

def lesson_menu():
    buttons = []
    lessons = get_lesson()  # [(1, "Python"), (2, "Django")]

    for lesson_id, title in lessons:
        buttons.append([
            InlineKeyboardButton(
                text=f"📚 {title}",
                callback_data=f"select_{lesson_id}"
            )
        ])

    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)



def ortga_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="go_back")]
    ])


cancel_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='❌ Bekor qilish', callback_data='cancel')]
    ]
)

