import pytz
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()

dp["started_at"] = datetime.now(pytz.timezone('Europe/Moscow')).astimezone(pytz.timezone('Asia/Almaty')).strftime("%d.%m.%Y, %H:%M")


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(text="""
Я - <b>«Копирайчу»,</b> ваш <b>личный ассистент!</b> 🤖

Чем займемся прямо сейчас?
""")


@dp.message(Command("info"))
async def info(message: types.Message, started_at: str):
    await message.answer(text=started_at)



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
