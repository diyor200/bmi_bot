# import telegraph
# from loader import db
# import asyncio
# telegraph_access_token = '338765955d36ece13eec0185a1708b95363ee58eab6dc79eb1646f13bf91'
# telegraph_api = telegraph.api.Telegraph(telegraph_access_token)
# k = []
#
# content = [
#     {
#         'tag': 'h2',
#         'children': ['Hello, world!']
#     },
#     {
#         'tag': 'p',
#         'children': ['This is a test page created with Telegraph and aiogram.\nSalom', 'Diyorbek Abdulaxatov']
#     }
# ]
#
#
# from aiogram import Bot, types
# from aiogram.dispatcher import Dispatcher
# from aiogram.utils import executor
#
# bot_token = '6280532530:AAGEt3uCpBcmxMk8knSTMHxixfyBZORYum8'
# bot = Bot(token=bot_token)
# dp = Dispatcher(bot)
#
# @dp.message_handler(commands=['start'])
# async def send_welcome(message: types.Message):
#     info = await db.get_info_outcasts_by_region(1)
#     print(info)
#     for i in info:
#         k.append([str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4])])
#     print(k)
#     content.append({'tag': 'p',
#                     'children': k})
#     page = telegraph_api.create_page('Test Page', content=content)
#     page_url = 'https://telegra.ph/{}'.format(page['path'])
#
#     sababi = f"<a href='{page_url}'>Sababi</a>"
#     await message.reply(f'Hi! Here is your page: {sababi}', parse_mode="HTML")
#
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)
