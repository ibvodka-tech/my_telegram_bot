import telebot
import time

# СЮДА ВСТАВЛЯЙ ТОКЕН ИЗ BOTFATHER
TOKEN = '8601249175:AAE7oWZYzDq_izIBDHCOIBSaIa2c1ntLRQI'
bot = telebot.TeleBot(TOKEN)

# 📋 ВАЙТ-ЛИСТ: Сюда через запятую вставляй числовые ID кентов, которым разрешён спам.
# Твой личный ID тоже обязательно добавь сюда!
WHITELIST_IDS = [
    8547599215,
    8038612348,
    5546716281,
    6558087689,
    7332580044,
]

STOPPED_CHATS = []


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Проверяем, есть ли пользователь в вайт-листе
    if message.from_user.id not in WHITELIST_IDS:
        bot.reply_to(message, "❌ **Доступ закрыт.** Тебя нет в банде!")
        return

    help_text = (
        "😈 **ПРИВАТНЫЙ ПУЛЕМЕТНЫЙ БЕЗЛИМИТ** 😈\n\n"
    
        "🔥 _Доступ только для своих. Обойма не ограничена!_"
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['stop'])
def stop_my_spam(message):
    if message.from_user.id not in WHITELIST_IDS:
        return
    if message.chat.id not in STOPPED_CHATS:
        STOPPED_CHATS.append(message.chat.id)
    bot.reply_to(message, "**твой спам остановлен**")

@bot.message_handler(commands=['spam'])
def start_hardcore_spam(message):
    # Жесткая проверка прав перед запуском пулемета
    if message.from_user.id not in WHITELIST_IDS:
        bot.reply_to(message, "❌ **Ошибка:** У тебя нет прав на использование этой команды!")
        return

    args = message.text.split()
    
    if len(args) < 3:
        bot.reply_to(message, "❌ Пиши: `/spam [кол-во] [текст]`")
        return

    count_str = args[1]
    if not count_str.isdigit():
        bot.reply_to(message, "❌ Количество должно быть числом!")
        return
        
    count = int(count_str)
    spam_text = " ".join(args[2:])

        # ⚡ УМНОЕ ОПРЕДЕЛЕНИЕ СКОРОСТИ
    if message.chat.type == 'private':
        delay = 0.0  # В личке лупим на абсолютном максимуме скорости!
        print(f"[!] Кент ID {message.from_user.id} (@{message.from_user.username}) запустил пулемет в ЛС на {count} соо.")
    else:
        delay = 0.1  # В группе притормаживаем до 0.15 сек, чтобы обходить ошибку 429
        print(f"[!] Кент ID {message.from_user.id} (@{message.from_user.username}) запустил пулемет в ГРУППЕ на {count} соо.")

    # Погнал чистый флуд
    if message.chat.id in STOPPED_CHATS:
        STOPPED_CHATS.remove(message.chat.id)
    for i in range(count):
        if message.chat.id in STOPPED_CHATS:
            break
        try:
            bot.send_message(message.chat.id, f"{spam_text}")
            if delay > 0:
                time.sleep(delay)  # Спим только если мы в группе
        except telebot.apihelper.ApiTelegramException as e:
            if e.error_code == 429:
                retry_after = e.result_json.get('parameters', {}).get('retry_after', 3)
                print(f"[WAIT] Сервер ТГ словил флуд. Авто-пауза {retry_after} сек...")
                time.sleep(retry_after)
            else:
                print(f"[ERROR] Ошибка API: {e}")
                break
        except Exception as error:
            print(f"[ERROR] Сбой: {error}")
            break

            
    bot.send_message(message.chat.id, "✅ Обойма выпущена! Спам окончен.")

print("=" * 50)
print("[MACHINE GUN] Приватный спамер успешно запущен!")
print("=" * 50)

bot.infinity_polling()
