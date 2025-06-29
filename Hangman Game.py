import tkinter as tk
import random

WORDS_WITH_HINTS = [
    ("ALGORITHM", "A step-by-step procedure for solving a problem"),
    ("BATTERY", "Powers your smartphone or laptop"),
    ("COMPUTER", "An electronic device for processing data"),
    ("DATABASE", "Stores large amounts of structured data"),
    ("EMAIL", "Electronic method of communication"),
    ("FIREWALL", "Protects networks from unauthorized access"),
    ("GITHUB", "A platform for code sharing and collaboration"),
    ("HACKER", "Person skilled in exploiting systems"),
    ("INTERNET", "Global system of interconnected computers"),
    ("JAVA", "A popular programming language"),
    ("KEYBOARD", "Input device for typing"),
    ("LAPTOP", "Portable personal computer"),
    ("MONITOR", "Displays visual output from the computer"),
    ("NETWORK", "Group of connected devices"),
    ("OPERATING", "Related to OS in computers"),
    ("PYTHON", "A programming language that's easy to learn"),
    ("QUEUE", "Linear data structure, FIFO"),
    ("ROUTER", "Connects networks and directs data"),
    ("SERVER", "Provides services or resources in a network"),
    ("TABLET", "Touchscreen mobile computing device"),
    ("USB", "Universal connector for storage and devices"),
    ("VARIABLE", "Holds a value in programming"),
    ("WEBSITE", "Collection of web pages"),
    ("XML", "Extensible Markup Language"),
    ("YOUTUBE", "Popular video streaming site"),
    ("ZIP", "Compressed file format"),
    ("NARUTO", "A ninja with a dream to become Hokage"),
    ("ONEPIECE", "Pirate adventure to find the ultimate treasure"),
    ("DEATHNOTE", "A notebook that kills anyone whose name is written"),
    ("GOKU", "Saiyan hero from Dragon Ball"),
    ("TITAN", "Colossal beings from Attack on Titan"),
    ("L", "The mysterious detective from Death Note"),
    ("INUYASHA", "Half-demon warrior with a powerful sword"),
    ("TOTORO", "A big cuddly forest spirit"),
    ("NEZUKO", "Demon girl with a bamboo muzzle"),
    ("ZENITSU", "Scared but lightning-fast swordsman"),
    ("AVENGERS", "Superhero team saving the universe"),
    ("BATMAN", "Dark knight of Gotham"),
    ("FROZEN", "Disney movie featuring Elsa and Anna"),
    ("INCEPTION", "Dreams within dreams"),
    ("MATRIX", "Blue pill or red pill?"),
    ("JOKER", "Gotham’s clown prince of crime"),
    ("HOGWARTS", "Magical school in the Harry Potter universe"),
    ("THANOS", "Snaps half the universe"),
    ("GODZILLA", "Giant monster from Japan"),
    ("SPIDERMAN", "Friendly neighborhood hero"),
    ("ANIME", "Japanese animated shows"),
    ("MOVIE", "You watch it in a theatre or at home"),
    ("MARVEL", "Home to Iron Man and Captain America"),
    ("DEMON", "Type of slayer in popular anime"),
    ("HOKAGE", "Leader of the Hidden Leaf Village"),
    ("TSUKUYOMI", "Itachi's powerful genjutsu"),
]

MAX_TRIES = 6

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("🕴️ Hangman Game with Hints")
        self.master.config(bg="#1e1e1e")
        self.word, self.hint = random.choice(WORDS_WITH_HINTS)
        self.guessed_letters = set()
        self.tries = 0

        self.word_display = tk.StringVar()
        self.update_display()

        self.setup_ui()

    def setup_ui(self):
        self.title = tk.Label(self.master, text="🕹️ Hangman Game", font=("Consolas", 24, "bold"),
                              bg="#1e1e1e", fg="white")
        self.title.pack(pady=10)

        self.hint_label = tk.Label(self.master, text=f"💡 Hint: {self.hint}", font=("Arial", 14),
                                   bg="#1e1e1e", fg="#00CED1")
        self.hint_label.pack(pady=5)

        self.canvas = tk.Canvas(self.master, width=200, height=250, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.draw_gallows()

        self.word_label = tk.Label(self.master, textvariable=self.word_display, font=("Consolas", 22),
                                   bg="#1e1e1e", fg="#00FFCC")
        self.word_label.pack(pady=10)

        self.buttons_frame = tk.Frame(self.master, bg="#1e1e1e")
        self.buttons_frame.pack()

        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            btn = tk.Button(self.buttons_frame, text=letter, width=4, font=("Arial", 12, "bold"),
                            bg="#333", fg="white", command=lambda l=letter: self.guess_letter(l))
            btn.grid(row=i // 9, column=i % 9, padx=2, pady=2)

        self.result_label = tk.Label(self.master, text="", font=("Arial", 16, "bold"),
                                     bg="#1e1e1e", fg="white")
        self.result_label.pack(pady=10)

        self.restart_btn = tk.Button(self.master, text="Restart", font=("Arial", 12, "bold"),
                                     bg="#444", fg="white", command=self.restart)
        self.restart_btn.pack(pady=5)

    def draw_gallows(self):
        self.canvas.create_line(20, 230, 180, 230, fill="white", width=2)
        self.canvas.create_line(50, 230, 50, 20, fill="white", width=2)
        self.canvas.create_line(50, 20, 130, 20, fill="white", width=2)
        self.canvas.create_line(130, 20, 130, 40, fill="white", width=2)

    def draw_hangman(self):
        steps = [
            lambda: self.canvas.create_oval(110, 40, 150, 80, fill="", outline="white", width=2),
            lambda: self.canvas.create_line(130, 80, 130, 150, fill="white", width=2),
            lambda: self.canvas.create_line(130, 100, 100, 130, fill="white", width=2),
            lambda: self.canvas.create_line(130, 100, 160, 130, fill="white", width=2),
            lambda: self.canvas.create_line(130, 150, 100, 190, fill="white", width=2),
            lambda: self.canvas.create_line(130, 150, 160, 190, fill="white", width=2),
        ]
        if self.tries <= MAX_TRIES:
            steps[self.tries - 1]()

    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            return

        self.guessed_letters.add(letter)
        if letter in self.word:
            self.update_display()
            if "_" not in self.word_display.get():
                self.result_label.config(text="🎉 You Win!", fg="lightgreen")
        else:
            self.tries += 1
            self.draw_hangman()
            if self.tries == MAX_TRIES:
                self.result_label.config(text=f"❌ You Lost! Word: {self.word}", fg="red")
                self.reveal_word()

        # Disable used button
        for widget in self.buttons_frame.winfo_children():
            if widget["text"] == letter:
                widget["state"] = "disabled"
                widget["bg"] = "#555"

    def update_display(self):
        display = [l if l in self.guessed_letters else "_" for l in self.word]
        self.word_display.set(" ".join(display))

    def reveal_word(self):
        self.word_display.set(" ".join(self.word))

    def restart(self):
        self.canvas.delete("all")
        self.draw_gallows()
        self.word, self.hint = random.choice(WORDS_WITH_HINTS)
        self.guessed_letters.clear()
        self.tries = 0
        self.update_display()
        self.hint_label.config(text=f"💡 Hint: {self.hint}")
        self.result_label.config(text="", fg="white")
        for widget in self.buttons_frame.winfo_children():
            widget["state"] = "normal"
            widget["bg"] = "#333"

def center_window(win, width=600, height=600):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def main():
    root = tk.Tk()
    center_window(root)
    HangmanGame(root)
    root.mainloop()

main()