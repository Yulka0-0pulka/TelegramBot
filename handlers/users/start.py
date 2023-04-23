from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message) -> None:
    await message.answer(f"Привет, {message.from_user.full_name}! для заказа пиццы /pizza")
