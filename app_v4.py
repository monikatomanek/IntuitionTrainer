import tkinter as tk
from tkinter import ttk
import random
import winsound

root = tk.Tk()
root.title("Intuition Trainer")
root.geometry("400x450")
root.configure(bg="#111")

sound_on = tk.BooleanVar(value=True)
difficulty = tk.StringVar(value="Easy")
mode = tk.StringVar(value="Think")
streak = 0

ranges = {"Easy": (1, 10), "Medium": (1, 30), "Hard": (1, 60), "Expert": (1, 99)}
affirmations = [
    "Trust your inner knowing.",
    "Your intuition is growing stronger.",
    "You already know the answer.",
    "Calm mind, clear vision.",
    "Let your inner voice guide you."
]

# Frames
frame_intro = tk.Frame(root, bg="#111")
frame_breath = tk.Frame(root, bg="#111")
frame_game = tk.Frame(root, bg="#111")
frame_end = tk.Frame(root, bg="#111")

# ===== Intro Screen =====
tk.Label(frame_intro, text="Intuition Trainer", font=("Arial", 20), fg="white", bg="#111").pack(pady=20)
tk.Label(frame_intro, text="Choose difficulty:", font=("Arial", 12), fg="gray", bg="#111").pack()

for level in ranges.keys():
    tk.Radiobutton(frame_intro, text=level, variable=difficulty, value=level,
                   fg="white", bg="#111", selectcolor="#222", font=("Arial", 11)).pack(pady=2)

tk.Checkbutton(frame_intro, text="Sound on", variable=sound_on,
               fg="white", bg="#111", selectcolor="#222").pack(pady=10)

tk.Label(frame_intro, text="Choose mode:", font=("Arial", 12), fg="gray", bg="#111").pack(pady=(15, 0))
tk.Radiobutton(frame_intro, text="Think of a number", variable=mode, value="Think",
               fg="white", bg="#111", selectcolor="#222", font=("Arial", 11)).pack(pady=2)
tk.Radiobutton(frame_intro, text="Input a number", variable=mode, value="Input",
               fg="white", bg="#111", selectcolor="#222", font=("Arial", 11)).pack(pady=2)

tk.Button(frame_intro, text="Continue", font=("Arial", 12), bg="#5cd3ff", fg="black",
          activebackground="#77e6ff", command=lambda: start_breathing_intro()).pack(pady=30)

# ===== Breathing Screen =====
canvas_breath = tk.Canvas(frame_breath, width=400, height=300, bg="#111", highlightthickness=0)
label_affirm = tk.Label(frame_breath, text="", font=("Arial", 14), fg="white", bg="#111", wraplength=380)
label_start_training = tk.Label(frame_breath, text="", font=("Arial", 14), fg="#5cd3ff", bg="#111")

# ===== Game Screen =====
canvas_game = tk.Canvas(frame_game, width=400, height=300, bg="#111", highlightthickness=0)
label_info = tk.Label(frame_game, text="", font=("Arial", 16), fg="white", bg="#111")
entry_guess = tk.Entry(frame_game, font=("Arial", 14), justify="center")

# New: End button
btn_end = tk.Button(frame_game, text="End Session", font=("Arial", 11),
                    bg="#444", fg="white", activebackground="#666",
                    command=lambda: end_game())

def play_tone(freq):
    if sound_on.get():
        winsound.Beep(freq, 200)

# ===== Intro Breathing (unchanged) =====
radius = 50
max_radius = 120
min_radius = 50

def draw_circle(canvas, r, text="", color="#5cd3ff"):
    canvas.delete("all")
    x0, y0 = 200 - r, 150 - r
    x1, y1 = 200 + r, 150 + r
    canvas.create_oval(x0, y0, x1, y1, fill=color, outline="")
    if text:
        canvas.create_text(200, 150, text=text, fill="white", font=("Arial", 16))

def start_breathing_intro():
    frame_intro.pack_forget()
    frame_breath.pack(fill="both", expand=True)
    label_affirm.config(text=random.choice(affirmations))
    label_affirm.pack(pady=10)
    canvas_breath.pack(pady=10)
    label_start_training.pack(pady=10)
    run_intro_breath_cycle()

def run_intro_breath_cycle():
    steps = 40
    duration = 4000 // steps

    def inhale(i=0):
        if i <= steps:
            r = min_radius + (max_radius - min_radius) * (i / steps)
            draw_circle(canvas_breath, r, "Inhale")
            root.after(duration, inhale, i + 1)
        else:
            pause1()

    def pause1(t=0):
        if t < 4000:
            draw_circle(canvas_breath, max_radius, "Pause")
            root.after(100, pause1, t + 100)
        else:
            exhale()

    def exhale(i=0):
        if i <= steps:
            r = max_radius - (max_radius - min_radius) * (i / steps)
            draw_circle(canvas_breath, r, "Exhale")
            root.after(duration, exhale, i + 1)
        else:
            pause2()

    def pause2(t=0):
        if t < 4000:
            draw_circle(canvas_breath, min_radius, "Pause")
            root.after(100, pause2, t + 100)
        else:
            end_intro_breathing()

    inhale()

def end_intro_breathing():
    canvas_breath.delete("all")
    label_affirm.config(text="")
    label_start_training.config(text="Let's start the training")
    tk.Button(frame_breath, text="Start", font=("Arial", 12), bg="#5cd3ff", fg="black",
              activebackground="#77e6ff", command=start_game).pack(pady=10)

# ===== Game Logic =====
def start_game():
    frame_breath.pack_forget()
    frame_game.pack(fill="both", expand=True)
    canvas_game.pack(pady=20)
    label_info.pack(pady=5)
    btn_end.pack(pady=10)  # show end button
    next_round()

def next_round():
    color = random.choice(["#5cd3ff", "#00bfa5", "#66e0ff"])
    draw_circle(canvas_game, 80, "", color=color)
    prepare_guess()

def prepare_guess():
    if mode.get() == "Think":
        label_info.config(text="Think of a number...")
        root.after(3000, show_number)
    else:
        label_info.config(text="Type your number and press Enter")
        entry_guess.pack(pady=5)
        entry_guess.delete(0, tk.END)
        entry_guess.bind("<Return>", check_guess)

def show_number():
    global streak
    low, high = ranges[difficulty.get()]
    num = random.randint(low, high)
    label_info.config(text=f"The number was {num}")
    play_tone(600)
    streak += 1
    root.after(2000, next_round)

def check_guess(event=None):
    global streak
    low, high = ranges[difficulty.get()]
    try:
        guess = int(entry_guess.get())
    except ValueError:
        label_info.config(text="Enter a valid number")
        return
    num = random.randint(low, high)
    entry_guess.pack_forget()
    if guess == num:
        label_info.config(text=f"Correct! The number was {num}")
        play_tone(800)
        streak += 1
    else:
        label_info.config(text=f"The number was {num}")
        play_tone(400)
    root.after(2000, next_round)

def end_game():
    frame_game.pack_forget()
    frame_end.pack(fill="both", expand=True)
    tk.Label(frame_end, text=f"Session Ended", font=("Arial", 18), fg="#5cd3ff", bg="#111").pack(pady=20)
    tk.Label(frame_end, text=f"Your streak: {streak}", font=("Arial", 16), fg="white", bg="#111").pack(pady=10)
    tk.Button(frame_end, text="Close", font=("Arial", 12), bg="#5cd3ff", fg="black",
              command=root.destroy).pack(pady=15)

frame_intro.pack(fill="both", expand=True)
root.mainloop()
