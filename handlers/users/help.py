from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from keyboards.inline.inline_keyboards import reason_markup
from loader import dp, db


@dp.message_handler(content_types=types.ContentType.TEXT, is_forwarded=True)
async def forwarder(message: types.Message):
    user_id = message.forward_from.id
    await message.answer(f"Message {user_id} dan yuborildi")


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam",
            "\n",
            "/new_region - Yangi viloyat qo'shish",
            "/new_building - Yangi bino qo'shish",
            "/add_info_exam - Imtihon ma'lumotlarini kiritish",
            "\n",
            "/exam_info - Imtihon ma'lumotlarini olish",
            "/exam_info_by_building - imtihon ma'lumotlari viloyat bino bo'yicha olish",
            "\n",
            "/chetlatildi - chetlatilgan talabani kiritish",
            "/chetlatilganlar - Chetlatilganlar jadvalidan ma'lumot olish",
            "/edit_outcast - chetlatilgan talabani sababini o'zgartirish/o'chirish",
            "\n",
            "/admins - Adminlar ro'yhatini olish",
            "/add_admin - Yangi admin qo'shish",
            "/del_admin - Adminni o'chirish",
            )

    await message.answer("\n".join(text))
