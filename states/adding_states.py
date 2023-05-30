from aiogram.dispatcher.filters.state import StatesGroup, State


class AddNewRegion(StatesGroup):
    RegionName = State()
    ResponsiblePerson = State()
    PhoneNumber = State()


class AddOutcasts(StatesGroup):
    viloyat = State()
    bino = State()
    ismi = State()
    sababi = State()


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


class AddExamInfos(StatesGroup):
    viloyat = State()
    bino_nomi = State()
    student_present = State()
    student_absent = State()
    supervisor_present = State()
    supervisor_absent = State()


class DelAdmin(StatesGroup):
    admin_id = State()


class GetInfosExam(StatesGroup):
    viloyat = State()
    bino_nomi = State()


class GetInfosExamByRegion(StatesGroup):
    viloyat = State()


class OutcastsState(StatesGroup):
    viloyat = State()
    bino = State()


class EditOutcastState(StatesGroup):
    viloyat = State()
    bino = State()
    id = State()
    reason = State()
