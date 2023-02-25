from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .check_admin import AdminFilterMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(AdminFilterMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
