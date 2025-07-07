from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from data.needfull_funcs import IsAdmin
from states.states import AdsState
from database.get_sql import get_all_users
from loader import bot  # bu yerda bot = Bot(token=...) bo'lishi kerak
from admin_buttons.reply import admin_menu

send_ads_router = Router()

@send_ads_router.message(F.text == "✍️ Talabalarga xabar yuborish", IsAdmin())
async def start_ads(message: Message, state: FSMContext):
    await message.answer("📨 Yubormoqchi bo‘lgan xabaringizni\n\n✅Matn\n✅Rasm\n✅Video\n✅Audio\n✅Dokument\n✅Lokatsiya\n\nYuboring...")
    await state.set_state(AdsState.waiting_ads)

@send_ads_router.message(AdsState.waiting_ads)
async def send_to_all_users(message: Message, state: FSMContext):
    user_ids = get_all_users()
    success, failed = 0, 0

    for user_id in user_ids:
        tg_id = user_id[3]
        try:
            if message.text:
                await bot.send_message(tg_id, "🗞 Admindan yangi xabar")
                await bot.send_message(tg_id, message.text)
            elif message.photo:
                await bot.send_message(tg_id, "🗞 Admindan yangi xabar")
                await bot.send_photo(tg_id, message.photo[-1].file_id, caption=message.caption)
            elif message.video:
                await bot.send_message(tg_id, "🗞 Admindan yangi xabar")
                await bot.send_video(tg_id, message.video.file_id, caption=message.caption)
            elif message.audio:
                await bot.send_message(tg_id, "🗞 Admindan yangi xabar")
                await bot.send_audio(tg_id, message.audio.file_id, caption=message.caption)
            elif message.voice:
                await bot.send_message(tg_id, "🗞 Admindan yangi xabar")
                await bot.send_voice(tg_id, message.voice.file_id, caption=message.caption)
            elif message.location:
                await bot.send_message(tg_id, "🗞 Admindan yangi xabar")
                await bot.send_location(tg_id, latitude=message.location.latitude, longitude=message.location.longitude)
            elif message.document:
                await bot.send_message(tg_id, "🗞 Admindan yangi xabar")
                await bot.send_document(tg_id, message.document.file_id, caption=message.caption)
            else:
                failed += 1
                continue
            success += 1
        except Exception as e:
            print(f"❌ [{user_id}] ga yuborilmadi: {e}")
            failed += 1

    await message.answer(f"✅ {success} foydalanuvchiga yuborildi\n❌ {failed} foydalanuvchiga yuborilmadi.", reply_markup=admin_menu)
    await state.clear()
