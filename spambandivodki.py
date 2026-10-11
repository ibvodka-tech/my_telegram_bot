import os
import threading
import time
from dotenv import load_dotenv
import telebot

# 1. Принудительно подгружаем .env
load_dotenv(override=True)

# 2. Ищем токен spambandivodki_TOKEN или TOKEN
TOKEN = os.getenv("spambandivodki_TOKEN") or os.getenv("TOKEN")

if not TOKEN:
  raise ValueError(
      "❌ Ошибка: Токен не найден! Проверь, что в файле .env прописан"
      " spambandivodki_TOKEN=..."
  )

bot = telebot.TeleBot(TOKEN)

# Флаг для контроля работы спамера
is_spamming = False


def spam_loop(chat_id, text, delay):
  global is_spamming
  while is_spamming:
    try:
      bot.send_message(chat_id, text)
      time.sleep(delay)
    except Exception as e:
      print(f"Ошибка при отправке: {e}")
      time.sleep(1)


@bot.message_handler(commands=["start"])
def start_cmd(message):
  bot.reply_to(
      message,
      "🤖 **Спам-бот на связи!**\n\n"
      "Команды:\n"
      "`/spam <текст>` — запустить спам\n"
      "`/stop` — остановить спам",
      parse_mode="Markdown",
  )


@bot.message_handler(commands=["spam"])
def start_spam(message):
  global is_spamming

  if is_spamming:
    bot.reply_to(message, "⚠️ Спамер уже работает! Сначала напиши /stop")
    return

  # Получаем текст после команды /spam
  text_to_send = message.text.replace("/spam", "").strip()

  if not text_to_send:
    bot.reply_to(
        message,
        "❌ Укажи текст для спама!\nПример: `/spam Привет всем`",
        parse_mode="Markdown",
    )
    return

  is_spamming = True
  bot.reply_to(
      message,
      f"🚀 **Спам запущен!**\nТекст: `{text_to_send}`\nНапиши /stop для отмены.",
      parse_mode="Markdown",
  )

  # Запускаем спам в отдельном потоке, чтобы бот не зависал и откликался на /stop
  threading.Thread(
      target=spam_loop, args=(message.chat.id, text_to_send, 1.0), daemon=True
  ).start()


@bot.message_handler(commands=["stop"])
def stop_spam(message):
  global is_spamming

  if not is_spamming:
    bot.reply_to(message, "ℹ️ Спамер и так выключен.")
    return

  is_spamming = False
  bot.reply_to(message, "🛑 **Спам успешно остановлен!**")


print("=" * 50)
print("[SPAMBOT] Спам-бот успешно запущен и готов к бою!")
print("=" * 50)

if __name__ == "__main__":
  bot.infinity_polling(skip_pending=True)