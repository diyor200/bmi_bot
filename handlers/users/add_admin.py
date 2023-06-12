from aiogram.dispatcher import FSMContext
from aiogram import types
from data.config import get_admins, add_admin_to_dotenv, remove_admin
from loader import dp, db, bot
from states.adding_states import AddingAdmin, DelAdmin


@dp.message_handler(commands=['add_admin'])
async def add_admin(message: types.Message):
    await message.answer("Admin idsini kiriting:")
    await AddingAdmin.admin_id.set()


@dp.message_handler(state=AddingAdmin.admin_id)
async def handle_admin_id(message: types.Message, state: FSMContext):
    admin_id = message.text
    if admin_id in get_admins():
        await message.answer("Allaqachon kiritilgan!")
    else:
        if admin_id.isdigit():
            add_admin_to_dotenv(str(admin_id))
            await message.answer("Admin muvaffaqiyatli qo'shildi!")
        else:
            await message.answer("Noto'g'ri id kiritildi!")
    await state.finish()


# Displaying admins
@dp.message_handler(commands=['admins'])
async def show_admins(message: types.Message):
    text = ""
    admins = get_admins()
    print(admins)
    for index, i in enumerate(admins, start=1):
        print(i)
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
    admin_id = message.text
    admins = get_admins()
    if admin_id in admins:
        remove_admin(admin_id)
        await message.answer("Muvaffaqiyatli o'chirildi!")
    else:
        await message.answer('Admin idsi noto\'ri kiritildi!')
    await state.finish()
