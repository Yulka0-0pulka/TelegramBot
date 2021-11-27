import re
from states.pizza import PizzaFsm
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp

users_queue = {}


@dp.message_handler(commands=['pizza'])
async def taking_order_handler(message: types.Message):
    if message.from_user.id not in users_queue:
        users_queue[message.from_user.id] = PizzaFsm()
    for user in users_queue:
        if message.from_user.id == user:
            await message.answer('Какую вы хотите пиццу? Большую или маленькую')


@dp.message_handler(commands=['reset'])
async def cmd_reset(message: types.Message):
    for user in users_queue:
        if message.from_user.id == user:
            users_queue[message.from_user.id] = PizzaFsm()
            await message.answer("Какую вы хотите пиццу? Большую или маленькую?")


@dp.message_handler()
async def order_handler(message: types.Message):
    for user in users_queue:
        if message.from_user.id == user:
            if message.text.capitalize() not in users_queue[user].command:
                await message.answer('Нет такой команды, попробуйте снова')

            if message.text.capitalize() == 'Большую':
                users_queue[user].big()
                await message.answer('Как вы будете платить, наличкой или банковской картой?')
            elif message.text.capitalize() == 'Маленькую':
                users_queue[user].small()
                await message.answer('Как вы будете платить, наличкой или банковской картой?')

            if message.text.capitalize() == 'Наличкой':
                users_queue[user].cash()
                await message.answer(f'Вы хотите {users_queue[user].size} пиццу, оплата - {users_queue[user].payment}?')

            elif message.text.capitalize() in ['Картой', 'Банковской картой']:
                users_queue[user].with_card()
                await message.answer(f'Вы хотите {users_queue[user].size} пиццу, оплата - {users_queue[user].payment}?')

            if message.text.capitalize() == 'Да':
                users_queue[user].yes()
                await message.answer(f'Спасибо за заказ! Чтобы заказать снова, нажмите /pizza')
                del users_queue[user]

            elif message.text.capitalize() == 'Нет':
                users_queue[user].no()
                await message.answer(f'Заказ отменен! Чтобы заказать снова, нажмите /pizza')
                del users_queue[user]
