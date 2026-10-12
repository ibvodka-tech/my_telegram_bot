import time
import pyperclip
import pyautogui

print("у тя 15 секунд беги переходить в чат")
time.sleep(15)

print("погнали спамить.....")

for i in range(30):
    text = "тебе пизда"
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    time.sleep(0.2)



    print("Готово")