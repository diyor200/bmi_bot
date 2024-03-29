from aiogram.dispatcher import FSMContext
from aiogram import types
from keyboards.default.adding_keyboards import viloyatlar_keyboard
from data.config import get_admins, add_admin_to_dotenv, remove_admin
from loader import dp, db, bot
from states.adding_states import AddBinoState, AddingAdmin, DelAdmin, AddNewRegion


# yangi viloyat qo'shish
@dp.message_handler(commands=['new_region'])
async def add_new_region(message: types.Message):
    await message.answer('Viloyat nomi kiriting:')
    await AddNewRegion.RegionName.set()


@dp.message_handler(state=AddNewRegion.RegionName)
async def region_name(message: types.Message, state: FSMContext):
    viloyat_nomi = message.text
    await state.update_data({
        'viloyat_nomi': viloyat_nomi
    })
    await message.answer("Mas'ul shaxsni kiriting:")
    await AddNewRegion.ResponsiblePerson.set()


@dp.message_handler(state=AddNewRegion.ResponsiblePerson)
async def responsible_person(message: types.Message, state: FSMContext):
    person = message.text
    await state.update_data({
        'person': person
    })
    await message.answer("Telefon raqamini kiriting:")
    await AddNewRegion.PhoneNumber.set()


@dp.message_handler(state=AddNewRegion.PhoneNumber)
async def phone_number(message: types.Message, state: FSMContext):
    phone = message.text
    await state.update_data({
        'phone': phone
    })
    # getting data from state
    data = await state.get_data()
    viloyat_nomi = data.get('viloyat_nomi')
    person = data.get('person')
    phone = data.get('phone')
    try:
        await db.add_region_name(viloyat_nomi, person, phone)
        await message.answer("Siz yangi viloyat qo'shdingiz!")
    except:
        await message.answer("Ma'lumotlarni kiritishda xatolik yuz berdi. Iltimos qaytadan urinib ko'ring!")
    await state.finish()


# /no qo'shish
@dp.message_handler(commands=["new_building"])
async def add_region(message: types.Message):
    await message.answer("Viloyatni tanlang: ", reply_markup=await viloyatlar_keyboard())
    await AddBinoState.qaysi_viloyatda.set()


@dp.message_handler(state=AddBinoState.qaysi_viloyatda)
async def add_region(message: types.Message, state: FSMContext):
    qaysi_viloyatda = message.text
    viloyat_id = await db.get_region_id(qaysi_viloyatda)
    await message.answer("Bino nomini kiriting: ", reply_markup=types.ReplyKeyboardRemove())
    await AddBinoState.bino_nomi.set()
    await state.update_data({
        "qaysi_viloyatda": viloyat_id[0]
    })


@dp.message_handler(state=AddBinoState.bino_nomi)
async def add_region(message: types.Message, state: FSMContext):
    bino_nomi = message.text
    await message.answer("Bino manzilini kiriting: ")
    await AddBinoState.bino_manzili.set()
    await state.update_data({
        "bino_nomi": bino_nomi
    })


@dp.message_handler(state=AddBinoState.bino_manzili)
async def add_region(message: types.Message, state: FSMContext):
    bino_manzili = message.text
    await message.answer("Bino sig'imini kiriting: ")
    await AddBinoState.bino_sigimi.set()
    await state.update_data({
        "bino_manzili": bino_manzili,
    })


@dp.message_handler(state=AddBinoState.bino_sigimi)
async def add_region(message: types.Message, state: FSMContext):
    bino_sigimi = message.text
    await message.answer("Mas'ul shaxsni kiriting: ")
    await AddBinoState.masul_shaxs.set()
    await state.update_data({
        "bino_sigimi": bino_sigimi,
    })


@dp.message_handler(state=AddBinoState.masul_shaxs)
async def add_region(message: types.Message, state: FSMContext):
    masul_shaxs = message.text
    await state.update_data({
        "masul_shaxs": masul_shaxs,
    })
    await AddBinoState.telefon_raqami.set()
    await message.answer("Telefon raqamini kiriting: ")


@dp.message_handler(state=AddBinoState.telefon_raqami)
async def add_region(message: types.Message, state: FSMContext):
    telefon_raqami = message.text
    await state.update_data({
        "telefon_raqami": telefon_raqami
    })
    data = await state.get_data()
    qaysi_viloyatda = data.get("qaysi_viloyatda")
    bino_nomi = data.get("bino_nomi")
    bino_manzili = data.get("bino_manzili")
    bino_sigimi = data.get("bino_sigimi")
    masul_shaxs = data.get("masul_shaxs")
    telefon_raqami = data.get("telefon_raqami")

    try:
        await db.add_building(int(qaysi_viloyatda), bino_nomi, bino_manzili,
                              int(bino_sigimi), masul_shaxs, telefon_raqami)

        await message.answer("Siz yangi bino qo'shdingiz!")
    except:
        await message.answer("Ma'lumotlarni kiritishda xatolik yuz berdi!")
    await state.finish()



