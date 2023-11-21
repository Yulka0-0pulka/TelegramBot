import asyncio
from itertools import count
import re

from setuptools import Command
from data.maping import channels
from model.models import Replay, Topic
from parser.asa import get_download_content
from states.state_pizza import PizzaFsm
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from model.engine import insert_image, session
from loader import bot
from datetime import datetime, timedelta
from sqlalchemy import delete


@dp.message_handler(commands=['photo'])
async def taking_order_handler(message: types.Message):
    is_sent: dict[int, bool] = {x: False for x in channels}
    while True:
        for chanel in channels:
            if not is_sent.get(chanel):
                object = session.query(Topic).filter(
                    Topic.chanel_id == str(chanel)
                ).first()
                try:
                    insert_image(
                        url=object.url, content_type=object.content_type,
                        model=Replay, chanel_id=object.chanel_id
                    )
                except:
                    pass
                session.delete(object)
                session.commit()
                try:
                    if object.content_type in ['image/jpeg', 'image/png']:
                        await bot.send_photo(object.chanel_id, object.url)
                    elif object.content_type == "video/mp4":
                        await bot.send_video(object.chanel_id, object.url)
                    is_sent[chanel] = True
                except Exception as e:
                    print("-----------------------------------")
                    print(e)
                    print(chanel)
                    print("-----------------------------------")
                    continue
        d = datetime.now() - timedelta(days=30)
        stmt = delete(Replay).where(Replay.date_update <= d)
        session.execute(stmt)
        session.commit()
        if all(is_sent.values()):
            for chanel in channels:
                count = session.query(Topic).filter(
                    Topic.chanel_id == str(chanel)
                ).count()
                if count < 20:
                    get_download_content(chanel)
                is_sent[chanel] = False

            await asyncio.sleep(100)

