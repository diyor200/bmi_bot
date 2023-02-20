from aiogram.dispatcher.filters.state import StatesGroup, State


class AddBinoState(StatesGroup):
    qaysi_viloyatda = State()
    bino_nomi = State()
    bino_manzili = State()
    bino_sigimi = State()
    masul_shaxs = State()
    telefon_raqami = State()
    telegram_id = State()


class AddingAdmin(StatesGroup):
    admin_id = State()
