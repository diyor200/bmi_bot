from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def viloyatlar_keyboard():
    regions = ("Andijon", "Buxoro", "Farg'ona", "Namangan", "Jizzax", "Navoiy",
               "Qashqadaryo", "Qoraqalpog'iston", "Samarqand", "Sirdaryo", "Surxondaryo",
               "Toshkent shahri", "Toshkent viloyati")
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for i in regions:
        markup.insert(KeyboardButton(text=i))
    return markup
