from aiogram.dispatcher import FSMContext
from aiogram import types
from keyboards.default.adding_keyboards import viloyatlar_keyboard
from data.config import BASE_DIR, get_admins, add_admin_to_dotenv, remove_admin
from loader import dp, db, bot
from states.adding_states import AddBinoState, AddingAdmin, AddExamInfos, DelAdmin
import pandas as pd


@dp.message_handler(commands=['users'])
async def get_info_exam(message: types.Message):
    infos = await db.select_all_users()
    lists = []
    for i in range(len(infos)):
        username = infos[i][1]
        telegram_id = infos[i][3]
        mentioned = await bot.get_chat(int(telegram_id))
        lists.append((username, telegram_id))
    df = pd.DataFrame(lists, columns=['username', 'telegram_id'])
    await message.answer(text=str(df))


@dp.message_handler(commands=['imtihon_malumotlari'])
async def get_info_exam(message: types.Message):
    infos = await db.get_info_about_exam()
    text = ""
    viloyat_nomi = infos[0][1]
    student_present = infos[0][2]
    student_absent = infos[0][3]
    student_removed = infos[0][4]
    supervisor_present = infos[0][5]
    supervisor_absent = infos[0][6]
    text += f"Viloyat:  <b>{viloyat_nomi}</b>\nQatnashgan talabalar: <b>{student_present}</b>\n" \
            f"Qatnashmagan talabalar soni: <b>{student_absent}</b>\nChetlatilgan talabar soni: <b>{student_removed}</b>\n" \
            f"Nazoratchilar soni: <b>{supervisor_present}</b>\n Qatnashmagan nazoratchilar soni: <b>{supervisor_absent}</b>"
    await message.answer(text=text)


@dp.message_handler(commands=['add_info_exam'])
async def add_info_exam(message: types.Message):
    await message.answer("Viloyatni kiriting", reply_markup=viloyatlar_keyboard())
    await AddExamInfos.viloyat.set()


@dp.message_handler(state=AddExamInfos.viloyat)
async def add_info_exam(message: types.Message, state: FSMContext):
    viloyat_nomi = message.text
    await state.update_data({
        'viloyat_nomi': viloyat_nomi
    })
    await message.answer("Nechta talaba keldi:", reply_markup=types.ReplyKeyboardRemove())
    await AddExamInfos.student_present.set()


@dp.message_handler(state=AddExamInfos.student_present)
async def add_info_exam(message: types.Message, state: FSMContext):
    student_present = message.text
    await state.update_data({
        'student_present': student_present
    })
    await message.answer("Nechta talaba kelmadi: ")
    await AddExamInfos.student_absent.set()


@dp.message_handler(state=AddExamInfos.student_absent)
async def add_info_exam(message: types.Message, state: FSMContext):
    student_absent = message.text
    await state.update_data({
        'student_absent': student_absent
    })
    await message.answer("Nechta talaba chetlashtirildi: ")
    await AddExamInfos.student_removed.set()


@dp.message_handler(state=AddExamInfos.student_removed)
async def add_info_exam(message: types.Message, state: FSMContext):
    student_removed = message.text
    await state.update_data({
        'student_removed': student_removed
    })
    await message.answer("Nechta nazoratchi qatnashdi?")
    await AddExamInfos.supervisor_present.set()


@dp.message_handler(state=AddExamInfos.supervisor_present)
async def add_info_exam(message: types.Message, state: FSMContext):
    supervisor_present = message.text
    await state.update_data({
        'supervisor_present': supervisor_present
    })
    await message.answer("Nechta nazoratchi qatnashmadi")
    await AddExamInfos.supervisor_absent.set()


@dp.message_handler(state=AddExamInfos.supervisor_absent)
async def add_info_exam(message: types.Message, state: FSMContext):
    supervisor_absent = message.text
    await state.update_data({
        'supervisor_absent': supervisor_absent
    })
    # Getting data from update
    data = await state.get_data()
    viloyat_nomi = data.get('viloyat_nomi')
    student_present = data.get('student_present')
    student_absent = data.get('student_absent')
    student_removed = data.get("student_removed")
    supervisor_present = data.get('supervisor_present')
    supervisor_absent = data.get('supervisor_absent')

    try:
        await db.add_info_about_exam(
            viloyat_nomi=viloyat_nomi,
            student_present=student_present,
            student_absent=student_absent,
            student_removed=student_removed,
            supervisor_present=supervisor_present,
            supervisor_absent=supervisor_absent
        )
        await message.answer('Muvaffaqiyatli kiritildi!')
    except:
        await message.answer("Ma'lumotlarni kiritishda xatolik yuz berdi!")
    await state.finish()


@dp.message_handler(commands=['add_admin'])
async def add_admin(message: types.Message):
    await message.answer("Admin idsini kiriting:")
    await AddingAdmin.admin_id.set()


@dp.message_handler(state=AddingAdmin.admin_id)
async def handle_admin_id(message: types.Message, state: FSMContext):
    admin_id = message.from_user.id
    if admin_id in get_admins():
        await message.answer("Allaqachon kiritilgan!")
    else:
        if admin_id.isdigit() and len(admin_id) == 10:
            add_admin_to_dotenv(str(admin_id))
            await message.answer("Admin muvaffaqiyatli qo'shildi!")
        else:
            await message.answer("Noto'g'ri id kiritildi!")
    await state.finish()


@dp.message_handler(commands=["yangi_bino"])
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
                             "Iltimos, nomlarni kiritishda tugmalardan foydalaning.",
                             reply_markup=viloyatlar_keyboard())

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


# Displaying admins
@dp.message_handler(commands=['adminlar'])
async def show_admins(message: types.Message):
    text = ""
    admins = get_admins()
    for index, i in enumerate(admins, start=1):
        try:
            user = await bot.get_chat(int(i))
            text += f"{str(index)}. {user.get_mention(name=user.full_name, as_html=True)} {i}\n"
        except:
            pass
    await message.answer(text=text)


@dp.message_handler(commands=['del_admin'])
async def del_admin(message: types.Message):
    await show_admins(message)
    await message.answer(text="Admin idsini kiriting")
    await DelAdmin.admin_id.set()


@dp.message_handler(state=DelAdmin.admin_id)
async def delete_admin(message: types.Message, state: FSMContext):
    admin_id = str(message.from_user.id)
    admins = get_admins()
    if admin_id in admins:
        remove_admin(admin_id)
        await message.answer("Muvaffaqiyatli o'chirildi!")
    else:
        await message.answer('Admin idsi noto\'ri kiritildi!')
    await state.finish()
