from aiogram.fsm.state import State, StatesGroup

class ContactForm(StatesGroup):
    name = State()
    phone = State()
    question = State()

class AddLessonState(StatesGroup):
    waiting_for_files = State()
    waiting_for_title = State()
    waiting_for_content = State()

class DeleteLessonState(StatesGroup):
    choosing = State()

class AddUser(StatesGroup):
    waiting_name = State()
    waiting_username = State()
    waiting_id = State()

class DELETEuser(StatesGroup):
    user_id = State()

class Admin(StatesGroup):
    admin_name = State()
    admin_username = State()
    admin_id = State()

class DELETEadmin(StatesGroup):
    admin_id =State()


class AdsState(StatesGroup):
    waiting_ads = State()