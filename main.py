import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# Загружаем скрытые переменные из файла .env
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Создаем одну красивую кнопку
keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❤️ Получить комплимент")]],
    resize_keyboard=True
)

# Список комплиментов
COMPLIMENTS = [
    "Ты самая невероятная и красивая! 😍",
    "Твоя улыбка делает любой день лучше. ✨",
    "Мне безумно повезло, что ты у меня есть! ❤️",
    "Ты моё самое любимое солнышко ☀️",
    "Рядом с тобой я самый счастливый человек на свете! 🥰"
]

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет, любимая! 😘 Нажимай на кнопку ниже!", reply_markup=keyboard)

@dp.message(lambda msg: msg.text == "❤️ Получить комплимент")
async def give_compliment(message: types.Message):
    await message.answer(random.choice(COMPLIMENTS))

@dp.message()
async def echo_message(message: types.Message):
    await message.answer(f"Ты написала: \"{message.text}\", а я просто люблю тебя! ❤️")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот успешно запущен на компьютере!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())