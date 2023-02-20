import asyncio
from aiogram.dispatcher import FSMContext
from aiogram import types
from keyboards.default.adding_keyboards import viloyatlar_keyboard
from data.config import ADMINS
from loader import dp, db, bot
from states.adding_states import AddBinoState, AddingAdmin


def get_admin_list():
    with open('admins.txt', 'r', encoding='utf-8') as f:
        admins = f.read().split(',')
    return admins


@dp.message_handler(chat_id=get_admin_list(), commands=['add_admin'])
async def add_admin(message: types.Message):
    await message.answer("Admin idsini kiriting:")
    await AddingAdmin.admin_id.set()


@dp.message_handler(state=AddingAdmin.admin_id)
async def handle_admin_id(message: types.Message, state: FSMContext):
    admin_id = message.text
    # await l.add_element(admin_id)
    if admin_id not in get_admin_list():
        if admin_id.isdigit() and len(admin_id) == 10:
            with open('admins.txt', 'a', encoding='utf-8') as f:
                f.write(f",{admin_id}")
                await message.answer("Admin muvaffaqiyatli qo'shildi!")
        else:
            await message.answer("Noto'g'ri id kiritildi!")
    await state.finish()


@dp.message_handler(chat_id=ADMINS, commands=["yangi_bino"])
async def add_region(message: types.Message, state: FSMContext):
    await message.answer("Viloyatni tanlang: ", reply_markup=viloyatlar_keyboard())
    await AddBinoState.qaysi_viloyatda.set()


@dp.message_handler(state=AddBinoState.qaysi_viloyatda)
async def add_region(message: types.Message, state: FSMContext):
    qaysi_viloyatda = message.text
    await message.answer("Bino nomini kiriting: ", reply_markup=types.ReplyKeyboardRemove())
    await AddBinoState.bino_nomi.set()
    await state.update_data({
        "qaysi_viloyatda": qaysi_viloyatda
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
        await db.add_building(qaysi_viloyatda, bino_nomi, bino_manzili,
                          bino_sigimi, masul_shaxs, telefon_raqami, "")

        await message.answer("Siz yangi bino qo'shdingiz!")
    except:
        await message.answer("Viloyat nomi noto'gri kiritilgan. "
                             "Iltimos, nomlarni kiritishda tugmalardan foydalaning.", reply_markup=viloyatlar_keyboard())

        @dp.message_handler(lambda message: True)
        async def region(message: types.Message):
            qaysi_viloyatda = message.text
            try:
                await db.add_building(qaysi_viloyatda, bino_nomi, bino_manzili,
                                  bino_sigimi, masul_shaxs, "", "")
                await message.answer("qo'shildi", reply_markup=types.ReplyKeyboardRemove())
                await state.finish()
            except:
                await message.answer("Yana notogri kiritingiz", reply_markup=viloyatlar_keyboard())
    await state.finish()


@dp.message_handler(text="/reklama", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    users = await db.select_all_users()
    for user in users:
        # print(user[3])
        user_id = user[3]
        await bot.send_message(chat_id=user_id, text="@SariqDev kanaliga obuna bo'ling!")
        await asyncio.sleep(0.05)