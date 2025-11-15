import tkinter as tk
import random
import winsound

# Main window
root = tk.Tk()
root.title("Intuition Trainer")
root.geometry("400x450")
root.configure(bg="#111")

sound_on = tk.BooleanVar(value=True)
difficulty = tk.StringVar(value="Easy")
streak = 0

# Difficulty settings
ranges = {"Easy": (1, 10), "Medium": (1, 30), "Hard": (1, 60), "Expert": (1, 99)}

# Frames
frame_intro = tk.Frame(root, bg="#111")
frame_game = tk.Frame(root, bg="#111")

# Canvas for breathing animation
canvas = tk.Canvas(frame_game, width=400, height=300, bg="#111", highlightthickness=0)
circle = canvas.create_oval(150, 150, 250, 250, fill="#5cd3ff", outline="")

# Labels
label_info = tk.Label(frame_game, text="", font=("Arial", 16), fg="white", bg="#111")
label_result = tk.Label(frame_game, text="", font=("Arial", 16), fg="white", bg="#111")
label_streak = tk.Label(frame_game, text="Streak: 0", font=("Arial", 12), fg="gray", bg="#111")

# Sound
def play_tone(freq):
    if sound_on.get():
        winsound.Beep(freq, 200)

# Breathing animation
radius = 50
max_radius = 120
min_radius = 50
step = 2
phase = "inhale"
animating = False

def breathing_cycle():
    global radius, phase, animating
    if not animating:
        return
    canvas.delete("all")
    x0, y0 = 200 - radius, 150 - radius
    x1, y1 = 200 + radius, 150 + radius
    canvas.create_oval(x0, y0, x1, y1, fill="#5cd3ff", outline="")

    if phase == "inhale":
        radius += step
        if radius >= max_radius:
            phase = "pause_in"
            root.after(1000, breathing_cycle)
            return
    elif phase == "pause_in":
        phase = "exhale"
    elif phase == "exhale":
        radius -= step
        if radius <= min_radius:
            phase = "pause_out"
            root.after(1000, breathing_cycle)
            return
    elif phase == "pause_out":
        phase = "done"
        end_breathing()
        return
    root.after(40, breathing_cycle)

def start_breathing():
    global radius, phase, animating
    radius = min_radius
    phase = "inhale"
    animating = True
    label_info.config(text="Breathe in... relax...")
    breathing_cycle()

def end_breathing():
    global animating
    animating = False
    label_info.config(text="Focus...")
    root.after(1000, show_number)

# Game logic
def show_number():
    global streak
    low, high = ranges[difficulty.get()]
    num = random.randint(low, high)
    label_info.config(text=f"The number is {num}")
    play_tone(600)
    streak += 1
    label_streak.config(text=f"Streak: {streak}")
    root.after(2500, start_breathing)

# Start game
def start_game():
    frame_intro.pack_forget()
    frame_game.pack(fill="both", expand=True)
    canvas.pack(pady=20)
    label_info.pack(pady=5)
    label_result.pack(pady=5)
    label_streak.pack(pady=10)
    start_breathing()

# Intro screen setup
tk.Label(frame_intro, text="Intuition Trainer", font=("Arial", 20), fg="white", bg="#111").pack(pady=20)
tk.Label(frame_intro, text="Choose difficulty:", font=("Arial", 12), fg="gray", bg="#111").pack()

for level in ranges.keys():
    tk.Radiobutton(frame_intro, text=level, variable=difficulty, value=level, 
                   fg="white", bg="#111", selectcolor="#222", font=("Arial", 11)).pack(pady=2)

tk.Checkbutton(frame_intro, text="Sound on", variable=sound_on, fg="white", bg="#111", selectcolor="#222").pack(pady=10)

tk.Button(frame_intro, text="Start", font=("Arial", 12), bg="#5cd3ff", fg="black", 
          activebackground="#77e6ff", command=start_game).pack(pady=30)

frame_intro.pack(fill="both", expand=True)
root.mainloop()
