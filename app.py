from aiogram import executor

from loader import dp
import filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from handlers.users.help import bot_help
from handlers.users.content import taking_order_handler


async def on_startup(dispatcher):

    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

