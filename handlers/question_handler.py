from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from data.needfull_funcs import IsUser

from loader import bot, ADMIN_ID


from states.states import ContactForm
from buttons.inline import cancel_button, user_menu
from buttons.reply import phone_btn

question_router = Router()

@question_router.callback_query(F.data == "cancel")
async def boglanish(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("❌ Adminga so'rov bekor qilindi\n"
                                  "Marhamat Siz ushbu botdan foydalanashingiz mumkin", reply_markup=user_menu)

@question_router.callback_query(F.data == "question_admin", IsUser())
async def call_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Admin bilan bog'lanish:\nAgar hohlasangiz ismingizni kiriting:", reply_markup=cancel_button)
    await state.set_state(ContactForm.name)

@question_router.message(ContactForm.name)
async def get_name(message: Message, state: FSMContext):
    if len(message.text.strip()) < 3:
        return await message.answer("❗ Ismingiz juda qisqa. Qayta kiriting:")
    await state.update_data(name=message.text.strip())
    await message.answer("Telefon raqamingizni kiriting (masalan: +998901234567):", reply_markup=phone_btn)
    await state.set_state(ContactForm.phone)


@question_router.message(ContactForm.phone)
async def get_phone_contact(message: Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number
        if not phone.startswith("+"):
            phone = f"+{phone}"

        await state.update_data(phone=phone)
    else:
        text = message.text.strip()

        if len(text) == 13 and text.startswith('+998') and text[1:].isdigit():
            await state.update_data(phone=text)
        else:
            return await message.answer("❌ Telefon raqam noto‘g‘ri. Iltimos, +998 bilan kiriting.")
    
    await message.answer("Adminga yozma shaklda so'rovingiz yozib yuboring")
    await state.set_state(ContactForm.question)

@question_router.message(ContactForm.question)
async def get_question(message: Message, state: FSMContext):
    await state.update_data(question=message.text)

    data = await state.get_data()
    await message.answer("✅ So'rovingiz yuborildi. Admin tomonidan tez orada ko'rib chiqiladi", reply_markup=user_menu)
    msg = (
        f"📥 O'quvchidan so'rov:\n\n"
        f"👤 Ismi: {data['name']}\n"
        f"📞 Telefon: {data['phone']}\n"
        f"🇺🇿 Telegram: @{message.from_user.username or 'yo‘q'}\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"So'rov:\n\n"
        f"{data['question']}"
    )

    for i in ADMIN_ID:
        await bot.send_message(chat_id=i, text=msg)

    await state.clear()
