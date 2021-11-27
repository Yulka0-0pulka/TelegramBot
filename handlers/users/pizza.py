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
            users_queue[user].machine.set_state('Ждем заказ')
            await message.answer("Какую вы хотите пиццу? Большую или маленькую?")


@dp.message_handler(commands=['cancel'])
async def cmd_reset(message: types.Message):
    for user in users_queue:
        if message.from_user.id == user:
            users_queue[user].machine.set_state('Ждем заказ')
            await message.answer("Заказ отменен! Чтобы заказать снова, нажмите /pizza")


@dp.message_handler()
async def order_handler(message: types.Message):
    for user in users_queue:
        try:
            if message.from_user.id == user:
                if message.text.capitalize() not in users_queue[user].command:
                    await message.answer('Нет такой команды, попробуйте снова')

                if message.text.capitalize() == 'Большую':
                    users_queue[user].big()
                    users_queue[user].size = users_queue[user].state
                    await message.answer('Как вы будете платить, наличкой или банковской картой?')
                elif message.text.capitalize() == 'Маленькую':
                    users_queue[user].small()
                    users_queue[user].size = users_queue[user].state
                    await message.answer('Как вы будете платить, наличкой или банковской картой?')

                if message.text.capitalize() == 'Наличкой':
                    users_queue[user].cash()
                    users_queue[user].payment = users_queue[user].state
                    await message.answer(
                        f'Вы хотите {users_queue[user].size} пиццу, оплата - {users_queue[user].payment}?')
                elif message.text.capitalize() in ['Картой', 'Банковской картой']:
                    users_queue[user].with_card()
                    users_queue[user].payment = users_queue[user].state
                    await message.answer(
                        f'Вы хотите {users_queue[user].size} пиццу, оплата - {users_queue[user].payment}?')
                if message.text.capitalize() == 'Да':
                    users_queue[user].yes()
                    await message.answer('Спасибо за заказ! Чтобы заказать снова, нажмите /pizza')

                elif message.text.capitalize() == 'Нет':
                    users_queue[user].no()
                    await message.answer('Заказ отменен! Чтобы заказать снова, нажмите /pizza')
        except:
            await message.answer('Продолжите или отмените заказ /cancel')
