import socket
import sys
from datetime import datetime

# 1. НАСТРОЙКА ЦЕЛИ (Что будем сканировать)
# Для теста возьмем официальный безопасный сайт-мишень.
# МОЖЕШЬ ЗАМЕНИТЬ НА ЛЮБОЙ ДРУГОЙ САЙТ (например: 'google.com' или 'yandex.ru')
TARGET_HOST = 'bakimektebleri.edu.az' 

# Превращаем красивое имя сайта (домен) в реальный цифровой IP-адрес
try:
    target_ip = socket.gethostbyname(TARGET_HOST)
except socket.gaierror:
    print(f"[❌ ОШИБКА] Не удалось разрешить имя хоста {TARGET_HOST}. Проверь интернет!")
    sys.exit()

# Список портов, которые мы хотим проверить (самые популярные в КБ)
PORTS_TO_SCAN = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080]

print("\n" + "="*60)
print(f"[🕶️ СКАНИРОВАНИЕ ЗАПУЩЕНО]  цель определена!")
print(f"🎯 Хост: {TARGET_HOST}")
print(f"🌐 IP-адрес цели: {target_ip}")
print(f"⏰ Время старта: {datetime.now().strftime('%H:%M:%S')}")
print("="*60 + "\n")

# 2. ЦИКЛ СКАНИРОВАНИЯ (Стучимся в порты)
try:
    for port in PORTS_TO_SCAN:
        # Создаем сетевой сокет (AF_INET - работаем с IPv4, SOCK_STREAM - протокол TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # КБ-фишка: ставим таймаут 1 секунду. 
        # Если порт не ответит за 1 сек, мы не будем ждать вечно, а пойдем дальше
        s.settimeout(1.0)
        
        # Пытаемся подключиться к IP-адресу и конкретному порту
        # Метод connect_ex возвращает код ответа: 0 - успех (порт открыт), любое другое число - закрыт
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            print(f"🔥 [ОТКРЫТ] Порт {port} доступен! Найдена потенциальная лазейка.")
        else:
            print(f"🔒 [закрыт] Порт {port}")
            
        # Обязательно закрываем соединение после проверки, чтобы не спалиться и не вешать сеть
        s.close()

except KeyboardInterrupt:
    print("\n[⛔ АВАРИЯ] Сканирование принудительно остановлено пользователем (Ctrl+C).")
    sys.exit()

print("\n" + "="*60)
print(f"[📜 ОТЧЕТ] Сканирование портов завершено успешно.")
print("="*60 + "\n") 