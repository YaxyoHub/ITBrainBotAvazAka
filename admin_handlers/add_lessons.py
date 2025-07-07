import os
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.states import AddLessonState
from data.needfull_funcs import IsAdmin
from database.sqlite3 import add_lesson
from admin_buttons.reply import admin_menu

admin_lesson_router = Router()

@admin_lesson_router.message(F.text == "➕ Dars qo‘shish", IsAdmin())
async def start_adding(message: Message, state: FSMContext):
    await message.answer("📥 Fayllarni yuboring (video, rasm, audio, hujjat). Tugatgach `/done` deb yozing.")
    await state.set_state(AddLessonState.waiting_for_files)
    await state.update_data(files=[])


@admin_lesson_router.message(F.document | F.video | F.photo | F.audio, AddLessonState.waiting_for_files)
async def handle_each_file(message: Message, state: FSMContext):
    await message.answer("📥 Fayl qabul qilindi. Saqlanmoqda...")

    file_info = {}

    if message.document:
        file_info = {
            "file_id": message.document.file_id,
            "file_name": message.document.file_name,
            "file_type": "document"
        }
    elif message.video:
        file_info = {
            "file_id": message.video.file_id,
            "file_name": f"{message.video.file_id}.mp4",
            "file_type": "video"
        }
    elif message.photo:
        file_info = {
            "file_id": message.photo[-1].file_id,
            "file_name": f"{message.photo[-1].file_id}.jpg",
            "file_type": "photo"
        }
    elif message.audio:
        file_info = {
            "file_id": message.audio.file_id,
            "file_name": f"{message.audio.file_id}.mp3",
            "file_type": "audio"
        }

    data = await state.get_data()
    data['files'].append(file_info)
    await state.update_data(files=data['files'])

    await message.answer(f"✅ Fayl saqlandi: {file_info['file_name']}")


@admin_lesson_router.message(F.text == "/done", AddLessonState.waiting_for_files)
async def done_adding_files(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data['files']:
        return await message.answer("🚫 Hech qanday fayl yuborilmadi.")

    await message.answer("✏️ Endi dars sarlavhasini kiriting:")
    await state.set_state(AddLessonState.waiting_for_title)


@admin_lesson_router.message(AddLessonState.waiting_for_title)
async def get_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddLessonState.waiting_for_content)
    await message.answer("📝 Endi dars matnini kiriting:")


@admin_lesson_router.message(AddLessonState.waiting_for_content)
async def get_content(message: Message, state: FSMContext):
    data = await state.get_data()

    for file_info in data['files']:
        add_lesson(
            title=data['title'],
            content=message.text,
            file_id=file_info['file_id'],
            file_type=file_info['file_type']
        )

    await message.answer("✅ Darslar file_id orqali bazaga saqlandi.", reply_markup=admin_menu)
    await state.clear()
