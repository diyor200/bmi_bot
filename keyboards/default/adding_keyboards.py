from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db


async def viloyatlar_keyboard():
    regions = await db.get_viloyatlar_nomi()
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for i in regions:
        markup.insert(KeyboardButton(text=i[0]))
    return markup


async def get_bino_keyboard(viloyat_nomi):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    bino_nomi = await db.get_bino_nomi_by_region(viloyat_nomi)
    print(f"bino: {bino_nomi}")
    if bino_nomi != []:
        for i in bino_nomi:
            markup.insert(KeyboardButton(text=f"{i[0]}"))
        print("Bino borakan")
    else:
        print("Bino yogakan")
        return None
    return markup
