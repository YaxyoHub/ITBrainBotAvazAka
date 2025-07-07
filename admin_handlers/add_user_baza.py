from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from admin_buttons.reply import admin_menu
from data.needfull_funcs import IsAdmin
from states.states import AddUser, DELETEuser
from database.get_sql import add_user, delete_user, check_user, get_all_users

add_user_router = Router()

# Tugmalar
user_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Foydalanuvchi qo'shish", callback_data="user_add"),
            InlineKeyboardButton(text="➖ Foydalanuvchi o'chirish", callback_data="user_del")
        ],
        [InlineKeyboardButton(text="📝 Foydalanuvchilar ro'yxati", callback_data="user_list")],
        [InlineKeyboardButton(text='🔙 Orqaga', callback_data='back')]
    ]
)

back_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='🔙 Ortga', callback_data='back_user')]]
)

# /start qo'shish
@add_user_router.message(F.text == "➕ Foydalanuvchi qo'shish", IsAdmin())
async def user_panel(message: Message):
    await message.reply("Foydalanuvchi qo'shish yoki o'chirish", reply_markup=user_button)

# ➕ Foydalanuvchi qo‘shish
@add_user_router.callback_query(F.data == "user_add")
async def add_user_step_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Foydalanuvchi ismini kiriting:")
    await state.set_state(AddUser.waiting_name)

@add_user_router.message(AddUser.waiting_name)
async def add_user_step_2(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Foydalanuvchi usernameni kiriting (masalan: @username):")
    await state.set_state(AddUser.waiting_username)

@add_user_router.message(AddUser.waiting_username)
async def add_user_step_3(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Foydalanuvchi ID sini kiriting:")
    await state.set_state(AddUser.waiting_id)

@add_user_router.message(AddUser.waiting_id)
async def add_user_finish(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("⚠️ ID faqat raqamlardan iborat bo'lishi kerak!")

    tg_id = int(message.text)
    if check_user(tg_id):
        await state.clear()
        return await message.answer("⚠️ Bu ID bilan foydalanuvchi mavjud!", reply_markup=user_button)

    data = await state.get_data()
    add_user(data['name'], data['username'], tg_id)
    await message.answer("✅ Foydalanuvchi muvaffaqiyatli qo‘shildi!", reply_markup=user_button)
    await state.clear()

# ➖ Foydalanuvchini o‘chirish
@add_user_router.callback_query(F.data == "user_del")
async def delete_user_step_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("O‘chirish uchun foydalanuvchi ID sini kiriting:")
    await state.set_state(DELETEuser.user_id)

@add_user_router.message(DELETEuser.user_id)
async def delete_user_finish(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("⚠️ ID raqamdan iborat bo‘lishi kerak!")

    tg_id = int(message.text)
    if not check_user(tg_id):
        await message.answer("❌ Bunday IDga ega foydalanuvchi topilmadi!", reply_markup=user_button)
    else:
        delete_user(tg_id)
        await message.answer("🗑️ Foydalanuvchi muvaffaqiyatli o‘chirildi!", reply_markup=user_button)
    await state.clear()

# 📝 Foydalanuvchilar ro‘yxati
@add_user_router.callback_query(F.data == "user_list")
async def show_user_list(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except Exception as e:
        print("❌ Xabarni o‘chirishda xatolik:", e)

    users = get_all_users()
    if not users:
        return await callback.message.answer("👤 Foydalanuvchilar topilmadi.", reply_markup=back_button)

    text = "👤 <b>Foydalanuvchilar ro'yxati:</b>\n\n"
    for index, user in enumerate(users, start=1):
        name = user[1]
        username = user[2]
        tg_id = user[3]
        text += f"{index}. <b>{name}</b> | {username} — <code>{tg_id}</code>\n"

    await callback.message.answer(text, parse_mode="HTML", reply_markup=back_button)

# 🔙 Orqaga tugmalar
@add_user_router.callback_query(F.data == "back")
async def back_to_main(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer("🔧 Admin panelga qaytdingiz", reply_markup=admin_menu)

@add_user_router.callback_query(F.data == "back_user")
async def back_to_user_menu(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except Exception as e:
        print("❌ back_user delete xatosi:", e)
    await callback.message.answer("Foydalanuvchi qo'shish yoki o'chirish", reply_markup=user_button)
