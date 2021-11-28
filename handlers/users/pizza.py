import re
from states.state_pizza import PizzaFsm
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp

# code smell
users_queue = {}


@dp.message_handler(commands=['pizza'])
async def taking_order_handler(message: types.Message):
    # Добавляем юзера в очередь если его нет в списске
    if message.from_user.id not in users_queue:
        # side effect
        users_queue[message.from_user.id] = PizzaFsm()
    for user in users_queue:
        # Отправляем юзерам в сочереди первое сообщение
        if message.from_user.id == user:
            await message.answer(users_queue[user].message)


@dp.message_handler(commands=['reset'])
async def cmd_reset(message: types.Message):
    for user in users_queue:
        # Переопределение класса стейт машины
        if message.from_user.id == user:
            users_queue[message.from_user.id] = PizzaFsm()
            await message.answer("Какую вы хотите пиццу? Большую или маленькую?")


@dp.message_handler(commands=['cancel'])
async def cmd_reset(message: types.Message):
    # При закрытии заказа удаляем юзера из очереди
    for user in users_queue:
        if message.from_user.id == user:
            # side effect
            # changed size during iteration
            del users_queue[user]
            await message.answer("Заказ отменен! Чтобы заказать снова, нажмите /pizza")


@dp.message_handler()
async def order_handler(message: types.Message):
    for user in users_queue:
        try:
            if message.from_user.id == user:
                # Проверяем валидность команд
                if message.text.capitalize() not in users_queue[user].command:
                    await message.answer('Нет такой команды, попробуйте снова')

                elif message.text.capitalize() in users_queue[user].command:
                    users_queue[user].trigger(message.text.capitalize())
                    await message.answer(users_queue[user].message)
                # При совершенном или отмененном заказе на последней стадии удаляем юзера из очереди
                if users_queue[user].state == 'Конец заказа':
                    # side effect
                    # changed size during iteration
                    del users_queue[user]
        # Перехватываем все ошибки при валидных командах но неправильном движении по логике
        except:
            await message.answer('Продолжите или отмените заказ /cancel '
                                 'Перезаказать /reset')
