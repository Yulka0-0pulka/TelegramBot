from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from setuptools import Command
from data.maping import channels
from datetime import datetime, timedelta
from keyboards.bot_keyboards import genmarkup


from loader import dp, bot


@dp.message_handler(CommandStart())
async def process_command_1(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Все категории', reply_markup=genmarkup())


@dp.callback_query_handler(lambda x: True)
async def process_callback_button1(callback_query: types.CallbackQuery):
    for chanel in channels:
        if channels[chanel]['callback'] == callback_query.data:
            expire_date = datetime.now() + timedelta(days=1)
            link = await bot.create_chat_invite_link(chanel, expire_date.timestamp, 1)
            await bot.send_message(callback_query.from_user.id, link.invite_link)
