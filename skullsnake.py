import tkinter as tk
import random


class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Змейка с черепами")
        self.window.resizable(False, False)

        # Настройки игры
        self.cell_size = 25
        self.grid_width = 25
        self.grid_height = 25
        self.speed = 120

        # Создание холста
        self.canvas = tk.Canvas(
            self.window,
            width=self.grid_width * self.cell_size,
            height=self.grid_height * self.cell_size,
            bg="black"
        )
        self.canvas.pack()

        # Создание счета
        self.score = 0
        self.score_label = tk.Label(
            self.window,
            text=f"Счет: {self.score}",
            font=("Arial", 16),
            fg="white",
            bg="black"
        )
        self.score_label.pack()

        # Инструкция
        self.instruction_label = tk.Label(
            self.window,
            text="Управление: Стрелки ←↑↓→ | Перезапуск: R",
            font=("Arial", 10),
            fg="gray",
            bg="black"
        )
        self.instruction_label.pack()

        # Инициализация игры
        self.reset_game()

        # Привязка клавиш
        self.window.bind("<KeyPress>", self.on_key_press)
        self.window.focus_set()

    def reset_game(self):
        # Позиция змейки
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = "Right"
        self.next_direction = "Right"

        # Создание черепа
        self.create_skull()

        self.score = 0
        self.score_label.config(text=f"Счет: {self.score}")
        self.game_over = False
        self.speed = 120

    def create_skull(self):
        while True:
            x = random.randint(2, self.grid_width - 3)
            y = random.randint(2, self.grid_height - 3)
            if (x, y) not in self.snake:
                self.skull_pos = (x, y)
                break

    def on_key_press(self, event):
        if self.game_over and event.keysym == "r":
            self.reset_game()
            return

        key = event.keysym
        if key in ["Up", "Down", "Left", "Right"]:
            # Запрет движения в противоположном направлении
            if (key == "Up" and self.direction != "Down") or \
                    (key == "Down" and self.direction != "Up") or \
                    (key == "Left" and self.direction != "Right") or \
                    (key == "Right" and self.direction != "Left"):
                self.next_direction = key

    def move_snake(self):
        if self.game_over:
            return

        self.direction = self.next_direction

        # Получаем текущую позицию головы
        head_x, head_y = self.snake[0]

        # Вычисляем новую позицию головы
        if self.direction == "Up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "Left":
            new_head = (head_x - 1, head_y)
        elif self.direction == "Right":
            new_head = (head_x + 1, head_y)

        # Проверка столкновения со стенами
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or
                new_head[1] < 0 or new_head[1] >= self.grid_height):
            self.game_over = True
            return

        # Проверка столкновения с собой
        if new_head in self.snake:
            self.game_over = True
            return

        # Добавляем новую голову
        self.snake.insert(0, new_head)

        # Проверка съедания черепа
        if new_head == self.skull_pos:
            self.score += 1
            self.score_label.config(text=f"Счет: {self.score}")
            self.create_skull()

            # Увеличиваем скорость каждые 5 очков
            if self.score % 5 == 0 and self.speed > 50:
                self.speed -= 10
        else:
            # Удаляем хвост, если не съели череп
            self.snake.pop()

    def draw_skull(self, x, y):
        size = self.cell_size
        center_x = x * size + size // 2
        center_y = y * size + size // 2
        radius = size // 3

        # Череп (белый круг)
        self.canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill="white",
            outline="gray",
            width=2
        )

        # Глазницы
        eye_radius = radius // 3
        self.canvas.create_oval(
            center_x - radius // 2 - eye_radius,
            center_y - radius // 3 - eye_radius,
            center_x - radius // 2 + eye_radius,
            center_y - radius // 3 + eye_radius,
            fill="black"
        )
        self.canvas.create_oval(
            center_x + radius // 2 - eye_radius,
            center_y - radius // 3 - eye_radius,
            center_x + radius // 2 + eye_radius,
            center_y - radius // 3 + eye_radius,
            fill="black"
        )

        # Нос (треугольник)
        nose_size = radius // 2
        self.canvas.create_polygon(
            center_x - nose_size // 2, center_y,
            center_x + nose_size // 2, center_y,
            center_x, center_y + nose_size,
            fill="black"
        )

        # Улыбка
        smile_y = center_y + radius // 3
        self.canvas.create_arc(
            center_x - radius // 2,
            smile_y - radius // 4,
            center_x + radius // 2,
            smile_y + radius // 4,
            start=0,
            extent=-180,
            style=tk.ARC,
            width=2
        )

    def draw(self):
        self.canvas.delete("all")

        if not self.game_over:
            # Рисуем змейку
            for i, (x, y) in enumerate(self.snake):
                if i == 0:  # Голова
                    color = "green"
                    # Добавляем глаза на голову
                    size = self.cell_size
                    self.canvas.create_rectangle(
                        x * size, y * size,
                        (x + 1) * size, (y + 1) * size,
                        fill=color, outline="white"
                    )
                    # Глаза змейки
                    eye_size = size // 6
                    self.canvas.create_oval(
                        x * size + size // 3 - eye_size,
                        y * size + size // 3 - eye_size,
                        x * size + size // 3 + eye_size,
                        y * size + size // 3 + eye_size,
                        fill="black"
                    )
                    self.canvas.create_oval(
                        x * size + 2 * size // 3 - eye_size,
                        y * size + size // 3 - eye_size,
                        x * size + 2 * size // 3 + eye_size,
                        y * size + size // 3 + eye_size,
                        fill="black"
                    )
                else:  # Тело
                    color = "#00FF00" if i % 2 == 0 else "#00CC00"
                    self.canvas.create_rectangle(
                        x * self.cell_size,
                        y * self.cell_size,
                        (x + 1) * self.cell_size,
                        (y + 1) * self.cell_size,
                        fill=color,
                        outline="white"
                    )

            # Рисуем череп
            self.draw_skull(*self.skull_pos)

        else:
            self.show_game_over()

    def show_game_over(self):
        self.canvas.create_rectangle(
            self.grid_width * self.cell_size // 4,
            self.grid_height * self.cell_size // 3,
            3 * self.grid_width * self.cell_size // 4,
            2 * self.grid_height * self.cell_size // 3,
            fill="darkred",
            outline="red",
            width=3
        )

        self.canvas.create_text(
            self.grid_width * self.cell_size // 2,
            self.grid_height * self.cell_size // 2 - 30,
            text="ИГРА ОКОНЧЕНА!",
            fill="white",
            font=("Arial", 24, "bold"),
            justify=tk.CENTER
        )

        self.canvas.create_text(
            self.grid_width * self.cell_size // 2,
            self.grid_height * self.cell_size // 2,
            text=f"Собрано черепов: {self.score}",
            fill="white",
            font=("Arial", 16),
            justify=tk.CENTER
        )

        self.canvas.create_text(
            self.grid_width * self.cell_size // 2,
            self.grid_height * self.cell_size // 2 + 30,
            text="Нажми R для новой игры",
            fill="yellow",
            font=("Arial", 14),
            justify=tk.CENTER
        )

    def game_loop(self):
        if not self.game_over:
            self.move_snake()
        self.draw()
        self.window.after(self.speed, self.game_loop)

    def start(self):
        self.game_loop()
        self.window.mainloop()


# Создание и запуск игры
game = SnakeGame()
game.start()