# Intuition Trainer — PyQt5 Full Glow-Up Edition (No Sound)

import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QRadioButton, QButtonGroup, QLineEdit, QStackedLayout
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer

class IntuitionTrainer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Intuition Trainer")
        self.setFixedSize(400, 450)

        # Background setup
        self.background = QLabel(self)
        pixmap = QPixmap("trainer.jpg")
        if pixmap.isNull():
            raise FileNotFoundError("trainer.jpg not found.")
        self.background.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding))
        self.background.setGeometry(0, 0, 400, 450)
        self.background.lower()

        # State variables
        self.difficulty = "Easy"
        self.mode = "Think"
        self.streak = 0
        self.ranges = {
            "Easy": (1, 10),
            "Medium": (1, 30),
            "Hard": (1, 60),
            "Expert": (1, 99)
        }
        self.affirmations = [
            "Trust your inner knowing.",
            "Your intuition is growing stronger.",
            "You already know the answer.",
            "Calm mind, clear vision.",
            "Let your inner voice guide you."
        ]

        # Stack layout to swap screens
        self.stack = QStackedLayout()
        self.setLayout(self.stack)

        self.init_intro_screen()
        self.init_breathing_screen()
        self.init_game_screen()
        self.init_end_screen()

        self.stack.setCurrentWidget(self.intro_screen)

    def styled_label(self, text, size=12, bold=False, color="white"):
        label = QLabel(text)
        font = QFont("Helvetica", size)
        font.setBold(bold)
        label.setFont(font)
        label.setStyleSheet(f"color: {color}; background-color: rgba(0,0,0,120);")
        label.setAlignment(Qt.AlignCenter)
        return label

    def init_intro_screen(self):
        self.intro_screen = QWidget()
        layout = QVBoxLayout(self.intro_screen)
        layout.setAlignment(Qt.AlignTop)

        layout.addWidget(self.styled_label("Intuition Trainer", 20, bold=True, color="#5cd3ff"))

        layout.addWidget(self.styled_label("Choose difficulty:"))
        difficulty_group = QButtonGroup(self.intro_screen)
        for level in self.ranges:
            btn = QRadioButton(level)
            btn.setStyleSheet("color: white;")
            if level == "Easy":
                btn.setChecked(True)
            btn.toggled.connect(lambda checked, l=level: self.set_difficulty(l) if checked else None)
            layout.addWidget(btn)
            difficulty_group.addButton(btn)

        layout.addWidget(self.styled_label("Choose mode:"))
        think_rb = QRadioButton("Think of a number")
        input_rb = QRadioButton("Input a number")
        think_rb.setChecked(True)
        think_rb.setStyleSheet("color: white;")
        input_rb.setStyleSheet("color: white;")
        think_rb.toggled.connect(lambda checked: setattr(self, 'mode', "Think" if checked else "Input"))

        layout.addWidget(think_rb)
        layout.addWidget(input_rb)

        cont_btn = QPushButton("Continue")
        cont_btn.clicked.connect(self.start_breathing_intro)
        layout.addWidget(cont_btn)

        self.stack.addWidget(self.intro_screen)

    def init_breathing_screen(self):
        self.breath_screen = QWidget()
        self.breath_layout = QVBoxLayout(self.breath_screen)

        self.breath_label = self.styled_label("", 16, bold=True, color="#5cd3ff")
        self.breath_affirmation = self.styled_label("", 12, color="white")
        self.breath_phase = self.styled_label("", 18, bold=True, color="#66e0ff")

        self.breath_layout.addWidget(self.breath_affirmation)
        self.breath_layout.addWidget(self.breath_phase)
        self.breath_layout.addWidget(self.breath_label)

        self.stack.addWidget(self.breath_screen)

    def init_game_screen(self):
        self.game_screen = QWidget()
        self.game_layout = QVBoxLayout(self.game_screen)

        self.game_label = self.styled_label("", 14, color="white")
        self.guess_entry = QLineEdit()
        self.guess_entry.setPlaceholderText("Enter your number")
        self.guess_entry.setStyleSheet("background-color: white; color: black;")
        self.guess_entry.returnPressed.connect(self.check_guess)

        self.end_button = QPushButton("End Session")
        self.end_button.clicked.connect(self.end_game)

        self.game_layout.addWidget(self.game_label)
        self.game_layout.addWidget(self.guess_entry)
        self.game_layout.addWidget(self.end_button)

        self.stack.addWidget(self.game_screen)

    def init_end_screen(self):
        self.end_screen = QWidget()
        layout = QVBoxLayout(self.end_screen)
        self.end_label = self.styled_label("Session Ended", 18, bold=True, color="#5cd3ff")
        self.streak_label = self.styled_label("", 14)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(lambda: sys.exit())

        layout.addWidget(self.end_label)
        layout.addWidget(self.streak_label)
        layout.addWidget(close_btn)

        self.stack.addWidget(self.end_screen)

    def set_difficulty(self, level):
        self.difficulty = level

    def start_breathing_intro(self):
        self.stack.setCurrentWidget(self.breath_screen)
        self.breath_affirmation.setText(random.choice(self.affirmations))
        self.run_breath_cycle()

    def run_breath_cycle(self):
        self.breath_label.setText("")
        self.animate_breath("Inhale", 4000, lambda: self.pause("Pause", 4000, lambda: self.animate_breath("Exhale", 4000, lambda: self.pause("Pause", 4000, self.end_intro_breathing))))

    def animate_breath(self, phase, duration, on_complete):
        self.breath_phase.setText(phase)
        QTimer.singleShot(duration, on_complete)

    def pause(self, text, duration, on_complete):
        self.breath_phase.setText(text)
        QTimer.singleShot(duration, on_complete)

    def end_intro_breathing(self):
        self.breath_label.setText("Let's start the training")
        start_btn = QPushButton("Start")
        start_btn.clicked.connect(self.start_game)
        self.breath_layout.addWidget(start_btn)

    def start_game(self):
        self.stack.setCurrentWidget(self.game_screen)
        self.next_round()

    def next_round(self):
        self.guess_entry.hide()
        if self.mode == "Think":
            self.game_label.setText("Think of a number...")
            QTimer.singleShot(3000, self.show_number)
        else:
            self.game_label.setText("Type your number and press Enter")
            self.guess_entry.show()
            self.guess_entry.setFocus()

    def show_number(self):
        low, high = self.ranges[self.difficulty]
        num = random.randint(low, high)
        self.game_label.setText(f"The number was {num}")
        self.streak += 1
        QTimer.singleShot(2000, self.next_round)

    def check_guess(self):
        low, high = self.ranges[self.difficulty]
        try:
            guess = int(self.guess_entry.text())
        except ValueError:
            self.game_label.setText("Enter a valid number")
            return

        cheat_chance = 0.15
        num = guess if random.random() < cheat_chance else random.randint(low, high)
        self.guess_entry.clear()
        self.guess_entry.hide()

        if guess == num:
            self.game_label.setText(f"Correct! The number was {num}")
            self.streak += 1
        else:
            self.game_label.setText(f"The number was {num}")
        QTimer.singleShot(2000, self.next_round)

    def end_game(self):
        self.streak_label.setText(f"Your streak: {self.streak}")
        self.stack.setCurrentWidget(self.end_screen)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    trainer = IntuitionTrainer()
    trainer.show()
    sys.exit(app.exec_())