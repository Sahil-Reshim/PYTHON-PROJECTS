import tkinter as tk
import random
from tkinter import messagebox

# Game config
WIDTH = 600
HEIGHT = 600
SPEED = 90
SPACE_SIZE = 20
BODY_PARTS = 3
HEAD_COLOR = "#32CD32"
BODY_COLOR = "#66FF66"
FOOD_COLOR = "#FF6347"
BG_COLOR = "#1e1e1e"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for _ in range(self.body_size):
            self.coordinates.append([0, 0])

        for i, (x, y) in enumerate(self.coordinates):
            color = HEAD_COLOR if i == 0 else BODY_COLOR
            square = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=color, outline="")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, outline="", tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    color = HEAD_COLOR
    head = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=color, outline="")
    snake.squares.insert(0, head)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        score_label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_dir):
    global direction
    if new_dir == "left" and direction != "right":
        direction = new_dir
    elif new_dir == "right" and direction != "left":
        direction = new_dir
    elif new_dir == "up" and direction != "down":
        direction = new_dir
    elif new_dir == "down" and direction != "up":
        direction = new_dir

def check_collision(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    canvas.delete("all")
    canvas.create_text(WIDTH/2, HEIGHT/2 - 40, fill="red", font=('Courier New', 30, 'bold'), text="GAME OVER")
    canvas.create_text(WIDTH/2, HEIGHT/2, fill="white", font=('Arial', 20), text=f"Final Score: {score}")
    restart_btn = tk.Button(window, text="Play Again", font=("Arial", 14, "bold"), bg="#444", fg="white", command=restart_game)
    restart_btn.place(x=WIDTH//2 - 60, y=HEIGHT//2 + 30)

def restart_game():
    window.destroy()
    main()

def main():
    global window, canvas, direction, score, score_label

    window = tk.Tk()
    window.title("🐍 Stylish Snake Game")
    window.config(bg="#282c34")
    window.resizable(False, False)

    direction = "right"
    score = 0

    score_label = tk.Label(window, text=f"Score: {score}", font=('Consolas', 18, 'bold'), bg="#282c34", fg="white")
    score_label.pack()

    canvas = tk.Canvas(window, bg=BG_COLOR, width=WIDTH, height=HEIGHT)
    canvas.pack()

    window.update()
    x = (window.winfo_screenwidth() // 2) - (WIDTH // 2)
    y = (window.winfo_screenheight() // 2) - (HEIGHT // 2)
    window.geometry(f"{WIDTH}x{HEIGHT+40}+{x}+{y}")

    snake = Snake()
    food = Food()

    window.bind("<Left>", lambda e: change_direction("left"))
    window.bind("<Right>", lambda e: change_direction("right"))
    window.bind("<Up>", lambda e: change_direction("up"))
    window.bind("<Down>", lambda e: change_direction("down"))

    next_turn(snake, food)
    window.mainloop()

main()