import logging

from aiogram import Dispatcher

from config.setting import setting


async def on_startup_notify(dp: Dispatcher):
    for admin in setting.ADMINS:
        try:
            await dp.bot.send_message(admin, "Добро пожаловать!")
        except Exception as err:
            logging.exception(err)
