from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from states.states import Admin, DELETEadmin
from database.sqlite3 import add_admin_sql, delete_admin_sql, check_admin, get_admin
from data.needfull_funcs import IsAdmin
from admin_buttons.reply import admin_menu

add_admin_router = Router()

# Inline tugmalar
admin_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Admin qo'shish", callback_data="admin_add"),
            InlineKeyboardButton(text="➖ Admin o'chirish", callback_data="admin_del")
        ],
        [InlineKeyboardButton(text="📝 Adminlar ro'yxati", callback_data="admin_list")],
        [InlineKeyboardButton(text='🔙 Orqaga', callback_data='back')]
    ]
)

back_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='🔙 Ortga', callback_data='back_admin')]]
)

# "Admin qo'shish" kommandasi
@add_admin_router.message(F.text == "➕ Admin qo'shish", IsAdmin())
async def admin_panel(message: Message):
    await message.reply("Admin qo'shish yoki o'chirish", reply_markup=admin_button)

# ➕ Admin qo‘shish
@add_admin_router.callback_query(F.data == "admin_add")
async def add_admin_step_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Admin ismini kiriting:")
    await state.set_state(Admin.admin_name)

@add_admin_router.message(Admin.admin_name)
async def add_admin_step_2(message: Message, state: FSMContext):
    await state.update_data(admin_name=message.text)
    await message.answer("Endi admin usernameni kiriting (masalan: @username):")
    await state.set_state(Admin.admin_username)

@add_admin_router.message(Admin.admin_username)
async def add_admin_step_3(message: Message, state: FSMContext):
    await state.update_data(admin_username=message.text)
    await message.answer("Endi admin ID sini kiriting (raqam bo‘lishi kerak):")
    await state.set_state(Admin.admin_id)

@add_admin_router.message(Admin.admin_id)
async def add_admin_finish(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("⚠️ Admin ID raqam bo‘lishi kerak!")
    
    admin_id = int(message.text)
    if check_admin(admin_id):
        await state.clear()
        return await message.answer("⚠️ Bu ID bilan admin allaqachon mavjud!", reply_markup=admin_button)

    await state.update_data(admin_id=admin_id)
    data = await state.get_data()
    add_admin_sql(data['admin_name'], data['admin_username'], data['admin_id'])
    await message.answer("✅ Admin muvaffaqiyatli qo‘shildi!", reply_markup=admin_button)
    await state.clear()

# ➖ Admin o‘chirish
@add_admin_router.callback_query(F.data == "admin_del")
async def delete_admin_step_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("O‘chirish uchun admin ID sini kiriting:")
    await state.set_state(DELETEadmin.admin_id)

@add_admin_router.message(DELETEadmin.admin_id)
async def delete_admin_finish(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("⚠️ Admin ID faqat raqamlardan iborat bo‘lishi kerak!")

    admin_id = int(message.text)
    if not check_admin(admin_id):
        await message.answer("❌ Bunday IDga ega admin topilmadi!", reply_markup=admin_button)
    else:
        delete_admin_sql(admin_id)
        await message.answer("🗑️ Admin muvaffaqiyatli o‘chirildi!", reply_markup=admin_button)
    await state.clear()

# 📝 Adminlar ro‘yxati
@add_admin_router.callback_query(F.data == "admin_list")
async def show_admin_list(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except Exception as e:
        print("❌ Xabarni o‘chirishda xatolik:", e)

    admins = get_admin()
    if not admins:
        return await callback.message.answer("👥 Adminlar topilmadi.", reply_markup=back_button)

    text = "👥 <b>Adminlar ro'yxati:</b>\n\n"
    for index, admin in enumerate(admins, start=1):
        name = admin[1]
        username = admin[2]
        tg_id = admin[3]
        text += f"{index}. <b>{name}</b> | {username} — <code>{tg_id}</code>\n"

    await callback.message.answer(text, parse_mode="HTML", reply_markup=back_button)

# 🔙 Orqaga tugmalari
@add_admin_router.callback_query(F.data == "back")
async def back_to_main_admin(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer("🔧 Admin panelga qaytdingiz", reply_markup=admin_menu)

@add_admin_router.callback_query(F.data == "back_admin")
async def back_to_admin_menu(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except Exception as e:
        print("❌ back_admin delete xatosi:", e)
    await callback.message.answer("Admin qo'shish yoki o'chirish", reply_markup=admin_button)
