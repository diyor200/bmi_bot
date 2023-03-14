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
            "/new_region - Yangi viloyat qo'shish",
            "/yangi_bino - Yangi bino qo'shish",
            "/add_info_exam - Imtihon ma'lumotlarini kiritish",
            "/imtihon_malumotlari_viloyat_boyicha - imtihon ma'lumotlari_viloyat bino bo'yicha olish",
            "/imtihon_malumotlari - Imtihon ma'lumotlarini olish",
            "/chetalildi - chetlatilgan talabani kiritish",
            "/chetlatilganlar - Chetlatilganlar jadvalidan ma'lumot olish",
            "/adminlar - Adminlar ro'yhatini olish",
            "/add_admin - Yangi admin qo'shish",
            "/del_admin - Adminni o'chirish",
            )

    await message.answer("\n".join(text))
