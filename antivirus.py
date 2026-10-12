import asyncio
import hashlib
import logging
import os
import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from dotenv import load_dotenv

# 1. Загружаем переменные из .env принудительно
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

if not TELEGRAM_BOT_TOKEN or not VIRUSTOTAL_API_KEY:
    raise ValueError("❌ Переменные не найдены в окружении Railway!")
# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


# ----------------- ПРОВЕРКА ССЫЛОК -----------------
def check_url_vt(url: str) -> str:
    """Проверка URL через VirusTotal API v3"""
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}

    try:
        scan_req = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url},
            timeout=10,
        )

        if scan_req.status_code != 200:
            return "⚠️ Ошибка при отправке URL на сканирование."

        analysis_id = scan_req.json()["data"]["id"]

        analysis_req = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
            headers=headers,
            timeout=10,
        )

        if analysis_req.status_code != 200:
            return "⚠️ Не удалось получить результаты анализа."

        stats = analysis_req.json()["data"]["attributes"]["stats"]
        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        harmless = stats.get("harmless", 0)
        undetected = stats.get("undetected", 0)

        if malicious > 0 or suspicious > 0:
            return (
                f"🚨 **Внимание, опасность!**\n\n"
                f"🔴 Обнаружено угроз: {malicious}\n"
                f"⚠️ Подозрительных вердиктов: {suspicious}\n"
                f"🟢 Безопасных откликов: {harmless + undetected}"
            )
        else:
            return (
                f"✅ **Ссылка чиста!**\n\n"
                f"Ни один антивирус не обнаружил угроз.\n"
                f"🟢 Безопасных вердиктов: {harmless + undetected}"
            )
    except Exception as e:
        return f"⚠️ Ошибка запроса к VirusTotal: {e}"


# ----------------- ПРОВЕРКА ФАЙЛОВ -----------------
def check_file_vt(file_bytes: bytes) -> str:
    """Проверка файла по SHA-256 хэшу или прямая загрузка в VirusTotal"""
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    file_hash = hashlib.sha256(file_bytes).hexdigest()

    try:
        hash_req = requests.get(
            f"https://www.virustotal.com/api/v3/files/{file_hash}",
            headers=headers,
            timeout=10,
        )

        if hash_req.status_code == 200:
            stats = hash_req.json()["data"]["attributes"]["last_analysis_stats"]
        else:
            files = {"file": ("scanned_file", file_bytes)}
            upload_req = requests.post(
                "https://www.virustotal.com/api/v3/files",
                headers=headers,
                files=files,
                timeout=30,
            )

            if upload_req.status_code != 200:
                return "⚠️ Ошибка при загрузке файла на VirusTotal."

            analysis_id = upload_req.json()["data"]["id"]

            analysis_req = requests.get(
                f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
                headers=headers,
                timeout=10,
            )
            if analysis_req.status_code != 200:
                return "⚠️ Файл загружен, но результаты ещё формируются. Попробуйте позже."

            stats = analysis_req.json()["data"]["attributes"]["stats"]

        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        harmless = stats.get("harmless", 0)
        undetected = stats.get("undetected", 0)

        if malicious > 0 or suspicious > 0:
            return (
                f"🚨 **Внимание, файл опасен!**\n\n"
                f"🔴 Обнаружено угроз: {malicious}\n"
                f"⚠️ Подозрительных вердиктов: {suspicious}\n"
                f"🟢 Безопасных откликов: {harmless + undetected}\n\n"
                f"🔑 SHA-256: `{file_hash}`"
            )
        else:
            return (
                f"✅ **Файл чист!**\n\n"
                f"Ни один антивирус не обнаружил угроз.\n"
                f"🟢 Безопасных вердиктов: {harmless + undetected}\n\n"
                f"🔑 SHA-256: `{file_hash}`"
            )
    except Exception as e:
        return f"⚠️ Ошибка при обработке файла: {e}"


# ----------------- ХЕНДЛЕРЫ КОМАНД -----------------
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет, Сэр! Я твой защитный бот.\n\n"
        "• Отправь мне **ссылку** (`http://` или `https://`)\n"
        "• Или отправь **файл/документ** (до 32 МБ)\n\n"
        "Я проверю их через VirusTotal!"
    )


@dp.message(Command("link"))
async def cmd_link(message: types.Message):
    await message.answer(
        "🔗 **Проверка ссылок:**\n\n"
        "Просто отправь мне любую URL-ссылку в чат (начинающуюся с `http://` или `https://`), "
        "и я проверю её по базам VirusTotal на наличие фишинга и малвари."
    )


@dp.message(Command("file"))
async def cmd_file(message: types.Message):
    await message.answer(
        "📁 **Проверка файлов:**\n\n"
        "Прикрепи и отправь мне файл или документ (до 32 МБ). "
        "Бот проверит его по SHA-256 хэшу и отсканирует антивирусами."
    )


# ----------------- ХЕНДЛЕРЫ ДАННЫХ -----------------
@dp.message(F.text)
async def handle_text(message: types.Message):
    text = message.text.strip()

    if text.startswith("http://") or text.startswith("https://"):
        await message.answer("🔍 Сканирую ссылку через VirusTotal, подождите...")

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, check_url_vt, text)

        await message.answer(result, parse_mode="Markdown")
    else:
        await message.answer(
            "Отправь корректную ссылку (`http://` / `https://`) или документ для проверки."
        )


@dp.message(F.document)
async def handle_document(message: types.Message):
    max_size = 32 * 1024 * 1024  # 32 МБ

    if message.document.file_size > max_size:
        await message.answer("⚠️ Файл слишком большой. Максимальный размер — 32 МБ.")
        return

    await message.answer("📥 Скачиваю и проверяю файл через VirusTotal...")

    try:
        file_info = await bot.get_file(message.document.file_id)
        file_bytes = await bot.download_file(file_info.file_path)

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, check_file_vt, file_bytes.read())

        await message.answer(result, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка при загрузке файла: {e}")


# ----------------- ЗАПУСК -----------------
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())