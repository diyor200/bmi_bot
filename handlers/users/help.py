from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from .admin import get_admin_list
from loader import dp


@dp.message_handler(content_types=types.ContentType.TEXT, is_forwarded=True)
async def forwarder(message: types.Message):
    user_id = message.forward_from.id
    await message.answer(f"Message {user_id} dan yuborildi")


@dp.message_handler(CommandHelp(), chat_id=get_admin_list())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam",
            "/users - Barcha foydalanuvchilarni chiqarish",
            "/imtihon_malumotlari - Imtihon ma'lumotlarini ko'rish",
            "/add_info_exam - Imtihon ma'lumotlarini kiritish",
            "/add_admin - Yangi admin qo'shish",
            "/yangi_bino - Yangi bino qo'shish",
            "/adminlar - Adminlar ro'yhatini olish",
            "/del_admin - Adminni o'chirish")
    
    await message.answer("\n".join(text))
