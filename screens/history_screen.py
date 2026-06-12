"""
History Screen — shows all saved quiz sessions.
"""

import tkinter as tk
from tkinter import messagebox
from utils.styles import *
from utils.database import get_all_sessions, get_session_detail, delete_session


class HistoryScreen(tk.Frame):
    NAME = "history"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DARK)
        self.app = app
        self._build()

    def _build(self):
        # Top bar
        topbar = tk.Frame(self, bg=BG_CARD, pady=10)
        topbar.pack(fill="x")
        tk.Button(topbar, text="← Back", font=FONT_BODY,
                  bg=BG_CARD, fg=TEXT_SECONDARY, bd=0,
                  cursor="hand2", activebackground=BORDER,
                  command=lambda: self.app.show_screen("home")
                  ).pack(side="left", padx=PAD)
        tk.Label(topbar, text="Quiz History", font=FONT_BODY_B,
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack(side="left")

        # Scrollable list
        canvas = tk.Canvas(self, bg=BG_DARK, highlightthickness=0)
        scroll = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)
        self._canvas = canvas

        self._inner = tk.Frame(canvas, bg=BG_DARK)
        win_id = canvas.create_window((0, 0), window=self._inner, anchor="nw")

        def _resize(e):
            canvas.itemconfig(win_id, width=e.width)
        canvas.bind("<Configure>", _resize)
        self._inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

        def _wheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _wheel)

    def on_show(self, **kwargs):
        for w in self._inner.winfo_children():
            w.destroy()
        sessions = get_all_sessions()

        header = tk.Frame(self._inner, bg=BG_DARK, padx=PAD*2, pady=PAD)
        header.pack(fill="x")
        tk.Label(header, text="Past Quizzes",
                 font=FONT_HEADING, bg=BG_DARK, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Label(header, text=f"{len(sessions)} session(s) saved",
                 font=FONT_BODY, bg=BG_DARK, fg=TEXT_SECONDARY).pack(anchor="w")

        if not sessions:
            tk.Label(self._inner, text="No quizzes taken yet. Generate one first!",
                     font=FONT_BODY, bg=BG_DARK, fg=TEXT_MUTED
                     ).pack(pady=PAD*3)
            return

        for row in sessions:
            sid, topic, num_q, score, total, pct, created = row
            self._session_card(sid, topic, num_q, score, total, pct, created)

        tk.Frame(self._inner, bg=BG_DARK, height=PAD*2).pack()
        self._canvas.yview_moveto(0)

    def _session_card(self, sid, topic, num_q, score, total, pct, created):
        card = tk.Frame(self._inner, bg=BG_CARD, padx=PAD, pady=PAD_SM+4)
        card.pack(fill="x", padx=PAD*2, pady=(PAD_SM, 0))

        color = SUCCESS if pct >= 70 else WARNING if pct >= 40 else DANGER

        left = tk.Frame(card, bg=BG_CARD)
        left.pack(side="left", fill="both", expand=True)

        tk.Label(left, text=topic[:80],
                 font=FONT_BODY_B, bg=BG_CARD, fg=TEXT_PRIMARY,
                 anchor="w").pack(anchor="w")
        meta = f"{num_q} questions  ·  {created[:16]}"
        tk.Label(left, text=meta, font=FONT_SMALL, bg=BG_CARD,
                 fg=TEXT_MUTED).pack(anchor="w", pady=(2, 0))

        right = tk.Frame(card, bg=BG_CARD)
        right.pack(side="right")

        tk.Label(right, text=f"{pct}%", font=("Segoe UI", 18, "bold"),
                 bg=BG_CARD, fg=color).pack(side="left", padx=(0, 12))
        tk.Label(right, text=f"{score}/{total}", font=FONT_SMALL,
                 bg=BG_CARD, fg=TEXT_SECONDARY).pack(side="left", padx=(0, 12))

        tk.Button(right, text="Review", font=FONT_SMALL,
                  bg=ACCENT, fg="white", bd=0, padx=10, pady=4,
                  cursor="hand2", activebackground=ACCENT_HOVER,
                  command=lambda s=sid: self._review(s)
                  ).pack(side="left", padx=(0, 6))

        tk.Button(right, text="🗑", font=FONT_SMALL,
                  bg=BORDER, fg=DANGER, bd=0, padx=8, pady=4,
                  cursor="hand2", activebackground="#450A0A",
                  command=lambda s=sid: self._delete(s)
                  ).pack(side="left")

    def _review(self, sid):
        detail = get_session_detail(sid)
        if not detail:
            messagebox.showerror("Error", "Session not found.")
            return
        self.app.quiz_data = {
            "topic": detail["topic"],
            "questions": detail["questions"]
        }
        # Reconstruct answers with int keys
        self.app.user_answers = {int(k): v for k, v in detail["answers"].items()}
        self.app.show_screen("results")

    def _delete(self, sid):
        if messagebox.askyesno("Delete?", "Delete this quiz session permanently?"):
            delete_session(sid)
            self.on_show()
