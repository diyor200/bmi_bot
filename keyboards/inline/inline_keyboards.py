from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db


async def viloyatlar_inline_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    viloyatlar = await db.get_viloyatlar_nomi()
    for num, i in enumerate(viloyatlar, start=1):
        markup.insert(InlineKeyboardButton(i[0], callback_data=str(num)))
    if len(viloyatlar) < 13:
        markup.insert(InlineKeyboardButton(text="+", callback_data="Add_new_viloyat"))
    return markup
