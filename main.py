"""
Quiz Generator from PDF/Text
OSSD Final Term Project
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from screens.home_screen import HomeScreen
from screens.quiz_screen import QuizScreen
from screens.results_screen import ResultsScreen
from screens.history_screen import HistoryScreen
from utils.database import init_db


class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QuizGen — AI Quiz Generator")
        self.geometry("950x700")
        self.minsize(800, 600)
        self.configure(bg="#0F172A")

        # Initialize database
        init_db()

        # Shared state
        self.quiz_data = {}       # generated questions
        self.user_answers = {}    # user's chosen answers
        self.topic_text = ""      # source text

        # Container frame
        self.container = tk.Frame(self, bg="#0F172A")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Screens dict
        self.screens = {}
        self._build_screens()
        self.show_screen("home")

    def _build_screens(self):
        for ScreenClass in (HomeScreen, QuizScreen, ResultsScreen, HistoryScreen):
            name = ScreenClass.NAME
            frame = ScreenClass(self.container, self)
            self.screens[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_screen(self, name, **kwargs):
        screen = self.screens[name]
        if hasattr(screen, "on_show"):
            screen.on_show(**kwargs)
        screen.tkraise()


if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
