"""
Results Screen — score summary, per-question review with explanations.
and implented by touseef
"""

import tkinter as tk
from tkinter import messagebox
from utils.styles import *
from utils.database import save_quiz_result


class ResultsScreen(tk.Frame):
    NAME = "results"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DARK)
        self.app = app
        self._build()

    def _build(self):
        # Top bar
        topbar = tk.Frame(self, bg=BG_CARD, pady=10)
        topbar.pack(fill="x")
        tk.Button(topbar, text="🏠 Home", font=FONT_BODY,
                  bg=BG_CARD, fg=TEXT_SECONDARY, bd=0,
                  cursor="hand2", activebackground=BORDER,
                  command=lambda: self.app.show_screen("home")
                  ).pack(side="left", padx=PAD)
        tk.Button(topbar, text="📋 History", font=FONT_BODY,
                  bg=BG_CARD, fg=TEXT_SECONDARY, bd=0,
                  cursor="hand2", activebackground=BORDER,
                  command=lambda: self.app.show_screen("history")
                  ).pack(side="right", padx=PAD)
        tk.Label(topbar, text="Results", font=FONT_BODY_B,
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack(side="left")

        # Scrollable area
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

        questions = self.app.quiz_data.get("questions", [])
        answers = self.app.user_answers
        topic = self.app.quiz_data.get("topic", "Quiz")
        n = len(questions)
        score = sum(
            1 for i, q in enumerate(questions)
            if answers.get(i) == q["answer"]
        )
        pct = round(score / n * 100) if n else 0

        # Save to DB
        try:
            save_quiz_result(topic, n, score, n, questions, {str(k): v for k, v in answers.items()})
        except Exception:
            pass

        self._build_content(questions, answers, topic, score, n, pct)
        self._canvas.yview_moveto(0)

    def _build_content(self, questions, answers, topic, score, n, pct):
        p = self._inner
        wrap = 720

        # Score card
        score_card = tk.Frame(p, bg=BG_CARD, padx=PAD*2, pady=PAD*2)
        score_card.pack(fill="x", padx=PAD*2, pady=(PAD*2, PAD))

        color = SUCCESS if pct >= 70 else WARNING if pct >= 40 else DANGER
        tk.Label(score_card, text=f"{pct}%", font=("Segoe UI", 48, "bold"),
                 bg=BG_CARD, fg=color).pack()
        tk.Label(score_card, text=f"{score} out of {n} correct",
                 font=FONT_SUBHEAD, bg=BG_CARD, fg=TEXT_PRIMARY).pack()
        tk.Label(score_card, text=topic, font=FONT_BODY,
                 bg=BG_CARD, fg=TEXT_SECONDARY).pack(pady=(4, 0))

        grade_msg = (
            "🎉 Excellent!" if pct >= 90
            else "👍 Good job!" if pct >= 70
            else "📚 Keep practising!" if pct >= 40
            else "💡 Review the material and try again."
        )
        tk.Label(score_card, text=grade_msg, font=FONT_BODY_B,
                 bg=BG_CARD, fg=color).pack(pady=(8, 0))

        # Action buttons
        btn_row = tk.Frame(score_card, bg=BG_CARD)
        btn_row.pack(pady=(PAD, 0))
        tk.Button(btn_row, text="🔁 Retry Same Quiz", font=FONT_BODY,
                  bg=ACCENT, fg="white", bd=0, padx=16, pady=10,
                  cursor="hand2", activebackground=ACCENT_HOVER,
                  command=self._retry).pack(side="left", padx=6)
        tk.Button(btn_row, text="🏠 New Quiz", font=FONT_BODY,
                  bg=BORDER, fg=TEXT_PRIMARY, bd=0, padx=16, pady=10,
                  cursor="hand2", activebackground=ACCENT,
                  command=lambda: self.app.show_screen("home")
                  ).pack(side="left", padx=6)

        # Divider
        tk.Frame(p, bg=BORDER, height=1).pack(fill="x", padx=PAD*2, pady=PAD)

        tk.Label(p, text="Review Answers", font=FONT_SUBHEAD,
                 bg=BG_DARK, fg=TEXT_PRIMARY).pack(anchor="w", padx=PAD*2)

        # Per-question review
        for i, q in enumerate(questions):
            user_ans = answers.get(i)
            correct = q["answer"]
            is_right = user_ans == correct

            card = tk.Frame(p, bg=BG_CARD, padx=PAD, pady=PAD)
            card.pack(fill="x", padx=PAD*2, pady=(PAD_SM, 0))

            # Header
            hdr = tk.Frame(card, bg=BG_CARD)
            hdr.pack(fill="x")
            icon = "✅" if is_right else "❌"
            tk.Label(hdr, text=f"{icon} Q{i+1}.", font=FONT_BODY_B,
                     bg=BG_CARD, fg=SUCCESS if is_right else DANGER
                     ).pack(side="left")

            # Question
            tk.Label(card, text=q["question"], font=FONT_BODY_B,
                     bg=BG_CARD, fg=TEXT_PRIMARY,
                     wraplength=wrap, justify="left"
                     ).pack(anchor="w", pady=(4, 8))

            # Options
            for key in ("A", "B", "C", "D"):
                opt_text = f"  {key}.  {q['options'][key]}"
                if key == correct:
                    bg, fg = "#14532D", SUCCESS
                elif key == user_ans and not is_right:
                    bg, fg = "#450A0A", DANGER
                else:
                    bg, fg = BG_DARK, TEXT_MUTED
                tk.Label(card, text=opt_text, font=FONT_OPTION,
                         bg=bg, fg=fg, anchor="w",
                         wraplength=wrap, justify="left"
                         ).pack(fill="x", pady=1, ipady=4, padx=4)

            if user_ans is None:
                tk.Label(card, text="⚠️  Not answered",
                         font=FONT_SMALL, bg=BG_CARD, fg=WARNING
                         ).pack(anchor="w", pady=(6, 0))

            # Explanation
            if q.get("explanation"):
                tk.Label(card, text="💡 " + q["explanation"],
                         font=FONT_SMALL, bg=BG_CARD, fg=TEXT_SECONDARY,
                         wraplength=wrap, justify="left"
                         ).pack(anchor="w", pady=(8, 0))

        # Bottom spacer
        tk.Frame(p, bg=BG_DARK, height=PAD*3).pack()

    def _retry(self):
        self.app.user_answers = {}
        self.app.show_screen("quiz")
