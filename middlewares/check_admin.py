from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from dotenv import get_key
from data.config import BASE_DIR
from aiogram.dispatcher.handler import CancelHandler
from loader import db


class AdminFilterMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user_id = update.message.from_user.id
        elif update.callback_query:
            user_id = update.callback_query.from_user.id
        else:
            return

        admins = get_key(f"{BASE_DIR}/.env", 'ADMINS').split(',')
        if str(user_id) not in admins:
            raise CancelHandler()

