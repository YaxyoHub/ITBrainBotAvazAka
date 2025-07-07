import asyncio, logging
from loader import dp, bot

from handlers.start_handler import start_router
from handlers.question_handler import question_router
from handlers.lessons_handler import lesson_router

from admin_handlers.add_lessons import admin_lesson_router
from admin_handlers.admin_panel import admin_router
from admin_handlers.del_lesson import delete_lesson_router
from admin_handlers.add_user_baza import add_user_router
from admin_handlers.add_admin_baza import add_admin_router
from admin_handlers.send_message_users import send_ads_router


dp.include_router(start_router)
dp.include_router(question_router)
dp.include_router(lesson_router)

dp.include_router(admin_lesson_router)
dp.include_router(admin_router)
dp.include_router(delete_lesson_router)
dp.include_router(add_user_router)
dp.include_router(add_admin_router)
dp.include_router(send_ads_router)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Bot is running...")
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
