from aiogram.dispatcher import FSMContext
from aiogram import types
from keyboards.default.adding_keyboards import viloyatlar_keyboard, get_bino_keyboard
from loader import dp, db, bot
from states.adding_states import GetInfosExam, AddExamInfos


@dp.message_handler(commands=['imtihon_malumotlari'])
async def get_info_exam(message: types.Message):
    text = "Viloyatni tanlang:"
    await message.answer(text, reply_markup=await viloyatlar_keyboard())
    await GetInfosExam.viloyat.set()


@dp.message_handler(state=GetInfosExam.viloyat)
async def get_info_exam(message: types.Message, state: FSMContext):
    viloyat = message.text
    await state.update_data({
        "viloyat_nomi": viloyat
    })
    await message.answer("Binoni kiriting: ", reply_markup=await get_bino_keyboard(viloyat))
    await GetInfosExam.bino_nomi.set()


@dp.message_handler(state=GetInfosExam.bino_nomi)
async def get_bino(message: types.Message, state: FSMContext):
    bino_nomi = message.text
    await state.update_data({
        'bino_nomi': bino_nomi
    })
    data = await state.get_data()
    viloyat_nomi = data.get('viloyat_nomi')
    bino_nomi = data.get('bino_nomi')
    infos = await db.get_info_about_exam(viloyat_nomi, bino_nomi)
    for i in infos:
        viloyat_nomi = i[0]
        bino_nomi = i[1]
        student_present = i[2]
        student_absent = i[3]
        student_removed = i[4]
        supervisor_present = i[5]
        supervisor_absent = i[6]
        text = ""
        text += f"Viloyat:  <b><u>{viloyat_nomi}</u></b>\nBino nomi:  <b><u>{bino_nomi}</u></b>\nQatnashgan talabalar:  <b><u>{student_present}</u></b>\n" \
                f"Qatnashmagan talabalar soni:  <b><u>{student_absent}</u></b>\nChetlatilgan talabar soni:  <b><u>{student_removed}</u></b>\n" \
                f"Nazoratchilar soni:  <b><u>{supervisor_present}</u></b>\nQatnashmagan nazoratchilar soni:  <b><u>{supervisor_absent}</u></b>"
        await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(commands=['add_info_exam'])
async def add_info_exam(message: types.Message):
    await message.answer("Viloyatni kiriting", reply_markup=await viloyatlar_keyboard())
    await AddExamInfos.viloyat.set()


@dp.message_handler(state=AddExamInfos.viloyat)
async def add_info_exam(message: types.Message, state: FSMContext):
    viloyat_nomi = message.text
    viloyat_id = await db.get_region_id(viloyat_nomi)
    print(viloyat_id)
    await state.update_data({
        'viloyat_nomi': viloyat_id[0]
    })
    await message.answer("Bino nomini kiriting:", reply_markup=await get_bino_keyboard(viloyat_nomi))
    await AddExamInfos.bino_nomi.set()


@dp.message_handler(state=AddExamInfos.bino_nomi)
async def add_info_exam(message: types.Message, state: FSMContext):
    bino_nomi = message.text
    bino_id = await db.get_building_id(bino_nomi)
    print(bino_id)
    await state.update_data({
        'bino_nomi': bino_id[0]
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
    viloyat_id = data.get('viloyat_nomi')
    bino_nomi = data.get('bino_nomi')
    student_present = data.get('student_present')
    student_absent = data.get('student_absent')
    student_removed = data.get("student_removed")
    supervisor_present = data.get('supervisor_present')
    supervisor_absent = data.get('supervisor_absent')
    try:
        await db.add_info_about_exam(
            viloyat_nomi=int(viloyat_id),
            bino_nomi=int(bino_nomi),
            student_present=int(student_present),
            student_absent=int(student_absent),
            student_removed=int(student_removed),
            supervisor_present=int(supervisor_present),
            supervisor_absent=int(supervisor_absent)
        )
        await message.answer('Muvaffaqiyatli kiritildi!')
    except:
        await message.answer("Ma'lumotlarni kiritishda xatolik yuz berdi!")
    await state.finish()
