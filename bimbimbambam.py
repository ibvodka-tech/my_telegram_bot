import os
import time
from dotenv import load_dotenv
import telebot

# 1. Загружаем переменные из .env
load_dotenv(override=True)

# 2. Ищем токен для эхо-бота (bimbimbambam_TOKEN или BOT_TOKEN)
TOKEN = os.getenv("bimbimbambam_TOKEN") or os.getenv("BOT_TOKEN")

if not TOKEN:
  raise ValueError(
      "❌ Ошибка: Токен для bimbimbambam не найден в .env! Проверь переменные."
  )

bot = telebot.TeleBot(TOKEN)

print("=" * 50)
print("[ECHO BOT] Бот Севиль / Bimbimbambam успешно запущен!")
print("=" * 50)


# Обработчик команд /start и /help
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
  bot.reply_to(
      message, "Привет! Я бот Севиль. Напиши мне что-нибудь, и я повторю!"
  )


# Эхо-обработчик (повторяет входящие тексты)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
  bot.reply_to(message, message.text)


if __name__ == "__main__":
  bot.infinity_polling(skip_pending=True)