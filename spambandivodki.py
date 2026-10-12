import os
import threading
import time
from dotenv import load_dotenv
import telebot

# 1. Принудительно подгружаем .env
load_dotenv(override=True)

# 2. Ищем токен
TOKEN = os.getenv("spambandivodki_TOKEN") or os.getenv("TOKEN")

if not TOKEN:
    raise ValueError(
        "❌ Ошибка: Токен не найден! Проверь, что в файле .env прописан spambandivodki_TOKEN=..."
    )

bot = telebot.TeleBot(TOKEN)

# 📋 ВАЙТ-ЛИСТ: ID тех, кому разрешен пулемет
WHITELIST_IDS = [
    8547599215,
    8038612348,
    5546716281,
    6558087689,
    7332580044,
]

# Словарь для отслеживания активных задач по чатам: {chat_id: True/False}
active_spams = {}


def spam_loop(chat_id, text, delay):
    global active_spams
    while active_spams.get(chat_id, False):
        try:
            bot.send_message(chat_id, text)
            if delay > 0:
                time.sleep(delay)
        except telebot.apihelper.ApiTelegramException as e:
            if e.error_code == 429:
                retry_after = e.result_json.get('parameters', {}).get('retry_after', 3)
                print(f"[WAIT] Лимит запросов. Пауза {retry_after} сек...")
                time.sleep(retry_after)
            else:
                print(f"[ERROR] Ошибка API: {e}")
                break
        except Exception as error:
            print(f"[ERROR] Сбой: {error}")
            break


@bot.message_handler(commands=["start", "help"])
def start_cmd(message):
    if message.from_user.id not in WHITELIST_IDS:
        bot.reply_to(message, "❌ **Доступ закрыт.** Тебя нет в банде!")
        return

    bot.reply_to(
        message,
        "😈 **ПРИВАТНЫЙ ПУЛЕМЕТНЫЙ БЕЗЛИМИТ** 😈\n\n"
        "Команды:\n"
        "`/spam [текст]` — запустить бесконечный пулемет\n"
        "`/stop` — остановить спам",
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["spam"])
def start_spam(message):
    global active_spams

    if message.from_user.id not in WHITELIST_IDS:
        bot.reply_to(message, "❌ **Ошибка:** У тебя нет прав на использование этой команды!")
        return

    chat_id = message.chat.id

    if active_spams.get(chat_id, False):
        bot.reply_to(message, "⚠️ В этом чате спамер уже работает! Сначала напиши /stop")
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

    # ⚡ Скорость: в ЛС максимум, в группе с микропаузой от антифлуда
    if message.chat.type == 'private':
        delay = 0.05
        print(f"[!] Кент ID {message.from_user.id} запустил бесконечный пулемет в ЛС.")
    else:
        delay = 0.15
        print(f"[!] Кент ID {message.from_user.id} запустил бесконечный пулемет в ГРУППЕ.")

    active_spams[chat_id] = True
    bot.reply_to(
        message,
        f"🚀 **Спам запущен!**\nТекст: `{text_to_send}`\nНапиши /stop для отмены.",
        parse_mode="Markdown",
    )

    # Запускаем в отдельном потоке, чтобы бот не зависал и сразу ловил /stop
    threading.Thread(
        target=spam_loop, args=(chat_id, text_to_send, delay), daemon=True
    ).start()


@bot.message_handler(commands=["stop"])
def stop_spam(message):
    global active_spams

    if message.from_user.id not in WHITELIST_IDS:
        return

    chat_id = message.chat.id
    if not active_spams.get(chat_id, False):
        bot.reply_to(message, "ℹ️ Спамер в этом чате и так выключен.")
        return

    active_spams[chat_id] = False
    bot.reply_to(message, "🛑 **Спам успешно остановлен!**")


print("=" * 50)
print("[MACHINE GUN] Бесконечный спам-бот с вайтлистами готов к бою!")
print("=" * 50)

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)