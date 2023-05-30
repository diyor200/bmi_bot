import logging

from aiogram.dispatcher import FSMContext
from aiogram import types
from keyboards.default.adding_keyboards import viloyatlar_keyboard, get_bino_keyboard
from keyboards.inline.inline_keyboards import reason_markup
from loader import dp, db
from states.adding_states import AddOutcasts, OutcastsState, EditOutcastState


# chetlatilganlarni bazaga qo'shish
@dp.message_handler(commands=['chetlatildi'])
async def add_region_id(message: types.Message):
    await message.answer("Viloyatni tanlang:", reply_markup=await viloyatlar_keyboard())
    await AddOutcasts.viloyat.set()


@dp.message_handler(state=AddOutcasts.viloyat)
async def add_outcasts(message: types.Message, state: FSMContext):
    viloyat_id = await db.get_region_id(message.text)
    await state.update_data({
        "viloyat_id": viloyat_id[0]
    })
    markup = await get_bino_keyboard(message.text)
    if markup == None:
        await message.answer("Bino mavjud emas!\nKiritish uchun: /yangi_bino", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer("Binoni kiriting:", reply_markup=markup)
        await AddOutcasts.bino.set()


@dp.message_handler(state=AddOutcasts.bino)
async def add_outcasts(message: types.Message, state: FSMContext):
    bino_id = await db.get_building_id(message.text)
    await state.update_data({
        "bino_id": bino_id[0]
    })
    await message.answer("Ism familyasini kiriting:")
    await AddOutcasts.ismi.set()


@dp.message_handler(state=AddOutcasts.ismi)
async def get_name(message: types.Message, state: FSMContext):
    ismi = message.text
    await state.update_data({
        'ismi': ismi
    })
    await message.answer("Sababini kiriting:")
    await AddOutcasts.sababi.set()


@dp.message_handler(state=AddOutcasts.sababi)
async def get_reason(message: types.Message, state: FSMContext):
    sababi = message.text
    data = await state.get_data()
    viloyat_id = data.get('viloyat_id')
    bino_id = data.get("bino_id")
    ismi = data.get('ismi')
    try:
        await db.add_info_outcasts(viloyat_id, bino_id, ismi, sababi)
        await message.answer("Muvaffaqiyatli qo'shildi")
    except:
        await message.answer("Ma'lumotlarni kiritishda xatolik yuz berdi!")
    await state.finish()


# chetlatilganlar jadvalidan ma'lumot olish
@dp.message_handler(commands=['chetlatilganlar'])
async def get_info_about_outcasts(message: types.Message):
    await message.answer("Viloyatni kiriting:", reply_markup=await viloyatlar_keyboard())
    await OutcastsState.viloyat.set()


@dp.message_handler(state=OutcastsState.viloyat)
async def outcasts_info(message: types.Message, state: FSMContext):
    viloyat = message.text
    try:
        viloyat_id = await db.get_region_id(viloyat)
        await state.update_data({
            "viloyat_id": int(viloyat_id[0]),
            'viloyat_nomi': viloyat
        })
        await OutcastsState.bino.set()
        markup = await get_bino_keyboard(viloyat)
        print(type(markup))
        print(markup)
        if markup == None:
            await message.answer("Bino mavjud emas!\nKiritish uchun: /new_building", reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
        else:
            await message.answer("Binoni kiriting", reply_markup=markup)
    except:
        await message.answer("Viloyat nomi noto'g'ri kiritildi. Iltimos tugmalardan foydalaning.")
        await state.finish()


@dp.message_handler(state=OutcastsState.bino)
async def outcasts_infos(message: types.Message, state: FSMContext):
    bino_nomi = message.text
    try:
        bino_id = await db.get_building_id(bino_nomi)
        await state.update_data({
            'bino_id': bino_id[0]
        })
        await message.answer("Ma'lumotlar olinmoqda...", reply_markup=types.ReplyKeyboardRemove())
    except:
        await message.answer("Bino nomi noto'g'ri kiritildi!", reply_markup=types.ReplyKeyboardRemove())

    data = await state.get_data()
    viloyat_id = data.get('viloyat_id')
    viloyat_nomi = data.get('viloyat_nomi')
    bino_id = data.get('bino_id')
    infos = await db.get_info_outcasts_by_region_building_count(viloyat_id, bino_id)
    # page_url = await add_to_telegraph(info)
    # sababi = f"<a href='{page_url}'>Sababi</a>"
    markup = reason_markup(viloyat_id, bino_id)
    await message.answer(f"Viloyat: <b><u>{viloyat_nomi}</u></b>\n"
                         f"Bino: <b><u>{bino_nomi}</u></b>\n"
                         f"Chetlatilganlar soni: <b><u>{infos[0]}</u></b>", parse_mode="HTML",
                         reply_markup=markup)
    await state.finish()


@dp.callback_query_handler()
async def callback_handle(call: types.CallbackQuery):
    # print(call.data)
    call_list = call.data.split(',')
    # print(len(call_list))
    text = ""
    if len(call_list) == 2:
        viloyat_id = int(call_list[0])
        bino_id = int(call_list[1])
        info = await db.get_info_outcasts_by_region_building(viloyat_id, bino_id)
        if len(info) == 0:
            text = "Chetlatilgan talabalar mavjud emas!"
            info = None
        else:
            for num, i in enumerate(info, start=1):
                text += f"{num}. {i[0]}\n" + f"{i[1]}\n" + f"{i[2]}\n" + f"{i[3]}\n" + f"{i[4]}\n\n"
    else:
        viloyat_id = call_list[0]
        info = await db.get_info_outcasts_by_region(int(viloyat_id))
        if len(info) == 0:
            text = "Chetlatilgan talabalar mavjud emas!"
            info = None
        else:
            for num, i in enumerate(info, start=1):
                text += f"{num}. {i[0]}\n" + f"{i[1]}\n" + f"{i[2]}\n" + f"{i[3]}\n\n"
    # print(info)

    await call.answer(text=text, show_alert=True)
    # await call.message.answer(reply_markup=)


@dp.message_handler(commands=['edit_outcast'])
async def edit_outcast(message: types.Message, state: FSMContext):
    markup = await viloyatlar_keyboard()
    if markup != []:
        await message.answer('Viloyatni tanlang:', reply_markup=markup)
        await EditOutcastState.viloyat.set()
    else:
        await message.answer("Bunday viloyat mavjud emas!\nQo'shish uchun: /new_region")


async def get_outcasts(viloyat_id, bino_id):
    result = ""
    outcasts = await db.get_all_outcasts_by_building(viloyat_id, bino_id)
    if outcasts != []:
        for i in outcasts:
            result += f"{i[0]}. {i[3]}\n"
        return result
    return False


@dp.message_handler(state=EditOutcastState.viloyat)
async def get_region(message: types.Message, state: FSMContext):
    viloyat_nomi = message.text
    try:
        viloyat_id = await db.get_region_id(viloyat_nomi)
        markup = await get_bino_keyboard(viloyat_nomi)
        print(markup)
        if markup is not None:
            await state.update_data({'viloyat_id': viloyat_id})
            await message.answer('Binoni kiriting:', reply_markup=markup)
            await EditOutcastState.bino.set()
        else:
            await message.answer('Bino kiritilmagan. Kiritish uchun: /new_building')
            await state.finish()
    except:
        await message.answer("Bunday Viloyat mavjud emas")
        await state.finish()


@dp.message_handler(state=EditOutcastState.bino)
async def get_building(message: types.Message, state: FSMContext):
    bino = message.text
    try:
        bino_id = await db.get_building_id(bino)
        print(bino_id[1])
        data = await state.get_data()
        viloyat_id = data.get('viloyat_id')
        print(viloyat_id)
        text = await get_outcasts(viloyat_id, bino_id)
        print(text)
        await message.answer(f"{text}Raqamini kiriting:")
        await state.update_data({'bino_id': bino_id})
        await EditOutcastState.id.set()
    except:
        await message.answer('Bunday bino mavjud emas! Qo\'shish uchun: /new_building')
        await state.finish()


@dp.message_handler(state=EditOutcastState.viloyat)
async def get_id(message: types.Message, state: FSMContext):
    id = int(message.text)
    if id:
        await state.update_data({'id': id})
        data = await state.get_data()
        vid = data.get('viloyat_id')
        bid = data.get('bino_id')
        reason = await db.get_outcast_reason(vid, bid, id)
        if reason != []:
            await message.answer(f'Eski sababi: <i>{reason[1]}</i>.\nYangi sababini kiriting:')
            await EditOutcastState.reason.set()
    else:
        await message.answer("Id ni noto'g'ri kiritdingiz!")
        await state.finish()


@dp.message_handler(state=EditOutcastState.viloyat)
async def edit_outcast(message: types.Message, state: FSMContext):
    reason = message.text
    data = await state.get_data()
    vid = data.get('viloyat_id')
    bid = data.get('bino_id')
    id = data.get('id')
    try:
        await db.edit_outcast_reason(vid, bid, id, reason)
        await message.answer("Muvaffaqiyatli o'zgartirildi!")
    except:
        await message.answer("Ma'lumotlarni kiritishda xatolik yuz berdi...")
    await state.finish()
