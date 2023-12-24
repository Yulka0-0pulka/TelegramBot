import asyncio
from concurrent.futures import ProcessPoolExecutor
from csv import excel
from functools import partial
from itertools import count
import re

from setuptools import Command
from data.maping import channels
from model.models import Replay, Topic
from parser.parser import get_download_content
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from model.engine import insert_image, session
from loader import bot
from datetime import datetime, timedelta
from sqlalchemy import delete


@dp.message_handler(commands=['photo'])
async def taking_order_handler(message: types.Message):
    loop = asyncio.get_running_loop()
    while True:
        for chanel in channels:
            image_obj = session.query(Topic).filter(
                Topic.chanel_id == str(chanel)
            ).first()
            if image_obj:
                insert_image(
                    url=image_obj.url, content_type=image_obj.content_type,
                    model=Replay, chanel_id=image_obj.chanel_id
                )
            else:
                continue
            session.delete(image_obj)
            session.commit()
            try:
                if image_obj.content_type in ['image/jpeg', 'image/png']:
                    await bot.send_photo(image_obj.chanel_id, image_obj.url)
                elif image_obj.content_type == "video/mp4":
                    await bot.send_video(image_obj.chanel_id, image_obj.url)
            except Exception as e:
                print("-----------------------------------")
                print(e)
                print(chanel)
                print("-----------------------------------")
                continue
        else:
            tasks = []
            with ProcessPoolExecutor() as ex:
                for chanel in channels:
                    count = session.query(Topic).filter(
                        Topic.chanel_id == str(chanel)
                    ).count()
                    if count < 20:
                        tasks.append(asyncio.create_task(
                            download_content(chanel, loop, ex))
                        )
                await asyncio.gather(*tasks)

        d = datetime.now() - timedelta(days=30)
        stmt = delete(Replay).where(Replay.date_update <= d)
        session.execute(stmt)
        session.commit()

        await asyncio.sleep(5)


async def download_content(channel, loop, ex):
    await loop.run_in_executor(ex, partial(get_download_content, channel))
