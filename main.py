# -*- coding: utf-8 -*-

"""
This is an image processing bot.
It process an image sent to it.
And sends back the size of an image.
"""

import logging
import asyncio
import numpy as np
import cv2


from aiogram import Bot, Dispatcher, executor, types

from logics.car_plate_number import extract_plate_number
from logics.exif_parsing import get_exif
from logics.reverse_geocoding import get_address_of_image
from logics.exif_parsing import get_photo_was_taken_at
from logics.reporting import get_when_description
from settings import API_TOKEN


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
loop = asyncio.get_event_loop()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi! "
                        "I'm car recognition bot! "
                        "Run your own copy with https://github.com/Hiyorimi/car_recognition_bot.")


async def process_file(file_id: str, bot, message):
    """Function for processing image file."""
    file_object = await bot.download_file_by_id(file_id)
    with open('test.jpg', 'wb') as fp:
        fp.write(file_object.read())
    file_object.seek(0)
    file_bytes = np.asarray(bytearray(file_object.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    recognized_car_plate_number = extract_plate_number(img)
    exif_data = get_exif(file_object)
    photo_was_taken_at = get_photo_was_taken_at(exif_data)
    when = get_when_description(photo_was_taken_at)
    image_address = get_address_of_image(exif_data)
    print(recognized_car_plate_number)
    await bot.send_message(
        chat_id=message.chat.id,
        text="""Когда: {when}
Распознаный номер: {recognized_car_plate_number}
Адрес: {image_address}
""".format(
            when=when,
            recognized_car_plate_number=recognized_car_plate_number,
            image_address=image_address,
        ),
    )


@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def photo_handler(message: types.Message):
    """
    Handler will process sent photo.
    """
    print(message)
    await process_file(message['photo'][-1]['file_id'], bot, message)


@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def photo_handler(message: types.Message):
    """
    Handler will process sent file.
    """
    print(message)
    if message['document']['mime_type'] == 'image/jpeg':
        await process_file(message['document']['file_id'], bot, message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)