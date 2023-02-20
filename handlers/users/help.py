from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(content_types=types.ContentType.TEXT, is_forwarded=True)
async def forwarder(message: types.Message):
    user_id = message.forward_from.id
    await message.answer(f"Message {user_id} dan yuborildi")


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam")
    
    await message.answer("\n".join(text))