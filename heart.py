import math
import turtle

# Настройка экрана сюрприза
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("For my girl")

# Настройка рисовальщика (черепашки)
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.color("#ffb6c1")  # Нежно-розовый неоновый цвет
pen.speed(0)          # Максимальная скорость, чтобы не лагало

# Цикл отрисовки сердца слоями из надписей
for scale in range(11, 17):
    for i in range(120):
        t = i * math.tau / 120
        # Математическая формула кардиоиды (сердца)
        x = 16 * math.sin(t) ** 3
        y = (13 * math.cos(t) - 5 * math.cos(2 * t) 
             - 2 * math.cos(3 * t) - math.cos(4 * t))
        
        # Перемещаем курсор в точку и пишем текст
        pen.goto(x * scale, y * scale)
        pen.write("I love you", align="center", font=("Arial", 8, "bold"))

# Финальная крупная надпись в самом центре сердца
pen.goto(0, -20)
pen.color("#ffffff")  # Белый цвет для контраста
pen.write("С Днём Рождения Нуря! ❤️", align="center", font=("Arial", 24, "bold"))

# Чтобы окно не закрывалось само по себе
turtle.done()
