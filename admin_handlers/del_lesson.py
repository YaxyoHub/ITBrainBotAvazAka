from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from admin_buttons.reply import admin_menu
from states.states import DeleteLessonState
from data.needfull_funcs import IsAdmin
from database.get_sql import get_lesson, get_lesson_by_id
from database.sqlite3 import delete_lesson_by_id

delete_lesson_router = Router()


@delete_lesson_router.message(F.text == "🗑 Dars o‘chirish", IsAdmin())
async def delete_lesson_start(message: Message, state: FSMContext):
    lessons = get_lesson()
    if not lessons:
        return await message.answer("📭 Hozircha hech qanday dars yo‘q.")

    buttons = []
    for l_id, title in lessons:
        buttons.append([InlineKeyboardButton(text=f"❌ {title}", callback_data=f"delete_{l_id}")])

    buttons.append([InlineKeyboardButton(text="🔙 Ortga", callback_data="back_to_lessons_list")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Qaysi darsni o‘chirmoqchisiz?", reply_markup=keyboard)
    await state.set_state(DeleteLessonState.choosing)


@delete_lesson_router.callback_query(F.data.startswith("delete_"), DeleteLessonState.choosing)
async def delete_selected(callback: CallbackQuery, state: FSMContext):
    l_id = int(callback.data.split("_")[1])
    lesson = get_lesson_by_id(l_id)

    if lesson:
        title = lesson[0]  # faqat sarlavha olish kifoya
        delete_lesson_by_id(l_id)

        await callback.message.edit_text(f"🗑 <b>{title}</b> darsi o‘chirildi.", parse_mode="HTML")
        await callback.message.answer("Marhamat", reply_markup=admin_menu)
    else:
        await callback.message.answer("❌ Dars topilmadi.")

    await state.clear()



@delete_lesson_router.callback_query(F.data == "back_to_lessons_list")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Marhamat", reply_markup=admin_menu)
