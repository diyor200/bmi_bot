import asyncpg
import telegraph
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db, bot
from data.config import ADMINS, ACCESS_TOKEN

telegraph_api = telegraph.api.Telegraph(ACCESS_TOKEN)


content = [
    {
        'tag': 'h2',
        'children': ["Sabablar:\n"]
    }
]


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)

    await message.answer("Xush kelibsiz!")
    info = await db.get_info_outcasts_by_region(1)
    print(info)
    for i in info:
        l = []
        l += [f"{i[0]}\n"] + [f"{i[1]}\n"] + [f"{i[2]}\n"] + [f"{i[3]}\n"]
        content.append({'tag': 'p',
                        'children': l})
    page = telegraph_api.create_page('Test Page', content=content)
    page_url = 'https://telegra.ph/{}'.format(page['path'])
    sababi = f"<a href='{page_url}'>Sababi</a>"
    await message.reply(f'Hi! Here is your page: {sababi}', parse_mode="HTML")
    # ADMINGA xabar beramiz
    count = await db.count_users()
    msg = f"{user[1]} {user[3]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    await bot.send_message(chat_id=ADMINS[0], text=msg)
