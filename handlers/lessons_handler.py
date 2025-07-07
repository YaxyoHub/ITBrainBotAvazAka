import os
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile

from buttons.inline import lesson_menu, ortga_button, user_menu
from data.needfull_funcs import IsUser
from database.get_sql import get_lesson_by_id, get_lesson

lesson_router = Router()

@lesson_router.callback_query(F.data == "list_lesson", IsUser())
async def lesson_cmd(callback: CallbackQuery):
    await callback.message.delete()

    lessons = get_lesson()
    if not lessons:
        return await callback.message.answer("📭 Hozircha hech qanday dars mavjud emas.", reply_markup=user_menu)

    await callback.message.answer("📝 Marhamat mavzular ro'yxati:", reply_markup=lesson_menu())


@lesson_router.callback_query(F.data.startswith("select_"))
async def select_lesson(callback: CallbackQuery):
    l_id = int(callback.data.split("_")[1])
    lesson = get_lesson_by_id(l_id)

    if lesson:
        title, content, file_id, file_type = lesson  # <-- yangilangan

        await callback.message.delete()

        text = f"📚 <b>{title}</b>\n\n{content}"

        if file_type == "video":
            await callback.message.answer_video(file_id, caption=text, parse_mode="HTML", reply_markup=ortga_button())
        elif file_type == "photo":
            await callback.message.answer_photo(file_id, caption=text, parse_mode="HTML", reply_markup=ortga_button())
        elif file_type == "document":
            await callback.message.answer_document(file_id, caption=text, parse_mode="HTML", reply_markup=ortga_button())
        elif file_type == "audio":
            await callback.message.answer_audio(file_id, caption=text, parse_mode="HTML", reply_markup=ortga_button())
        else:
            await callback.message.answer(text, parse_mode="HTML", reply_markup=ortga_button())

    else:
        await callback.message.answer("❌ Dars topilmadi.")

@lesson_router.callback_query(F.data == 'go_back')
async def ortga(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Marhamat", reply_markup=lesson_menu())

@lesson_router.callback_query(F.data == "back_menu")
async def ortga_menu(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Marhamat", reply_markup=user_menu)