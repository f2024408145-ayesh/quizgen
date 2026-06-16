"""
Quiz Screen — presents MCQ questions, records answers, submits.
By "Malik Abdul Moeed Khan"
"""

import tkinter as tk
from tkinter import messagebox
from utils.styles import *


class QuizScreen(tk.Frame):
    NAME = "quiz"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DARK)
        self.app = app
        self._q_index = 0
        self._selected = {}   # index → "A"|"B"|"C"|"D"
        self._opt_buttons = {}
        self._build()

    # ── Build ─────────────────────────────────────────────────────────────

    def _build(self):
        # Top bar
        topbar = tk.Frame(self, bg=BG_CARD, pady=10)
        topbar.pack(fill="x")
        tk.Button(topbar, text="← Home", font=FONT_BODY,
                  bg=BG_CARD, fg=TEXT_SECONDARY, bd=0,
                  activebackground=BORDER, cursor="hand2",
                  command=self._back_home).pack(side="left", padx=PAD)
        self._title_lbl = tk.Label(topbar, text="Quiz", font=FONT_BODY_B,
                                   bg=BG_CARD, fg=TEXT_PRIMARY)
        self._title_lbl.pack(side="left")
        self._prog_lbl = tk.Label(topbar, text="", font=FONT_BODY,
                                  bg=BG_CARD, fg=TEXT_SECONDARY)
        self._prog_lbl.pack(side="right", padx=PAD)

        # Progress bar
        self._prog_frame = tk.Frame(self, bg=BORDER, height=4)
        self._prog_frame.pack(fill="x")
        self._prog_bar = tk.Frame(self._prog_frame, bg=ACCENT, height=4)
        self._prog_bar.place(x=0, y=0, relheight=1.0)

        # Scrollable content
        canvas = tk.Canvas(self, bg=BG_DARK, highlightthickness=0)
        scroll = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

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

        self._canvas = canvas

        # Content frames (built once, reused)
        content = tk.Frame(self._inner, bg=BG_DARK, padx=PAD*2, pady=PAD*2)
        content.pack(fill="both", expand=True)

        # Question number / topic
        self._q_num_lbl = tk.Label(content, text="", font=FONT_SMALL,
                                   bg=BG_DARK, fg=ACCENT)
        self._q_num_lbl.pack(anchor="w")

        # Question text
        self._q_text = tk.Label(content, text="", font=FONT_QUESTION,
                                bg=BG_DARK, fg=TEXT_PRIMARY,
                                wraplength=700, justify="left")
        self._q_text.pack(anchor="w", pady=(6, PAD))
        content.bind("<Configure>",
                     lambda e: self._q_text.config(wraplength=max(200, e.width - 40)))

        # Options
        self._opt_frame = tk.Frame(content, bg=BG_DARK)
        self._opt_frame.pack(fill="x")

        for key in ("A", "B", "C", "D"):
            btn = tk.Button(
                self._opt_frame, text="", font=FONT_OPTION,
                bg=OPTION_BG, fg=TEXT_PRIMARY, bd=0,
                padx=16, pady=14, anchor="w", wraplength=700,
                cursor="hand2", activebackground=OPTION_HOVER,
                command=lambda k=key: self._select(k)
            )
            btn.pack(fill="x", pady=4)
            self._opt_buttons[key] = btn

        # Navigation
        nav = tk.Frame(content, bg=BG_DARK, pady=PAD*2)
        nav.pack(fill="x")
        self._prev_btn = tk.Button(nav, text="← Previous", font=FONT_BODY,
                                   bg=BORDER, fg=TEXT_PRIMARY, bd=0,
                                   padx=20, pady=10, cursor="hand2",
                                   activebackground=ACCENT,
                                   command=self._prev_q)
        self._prev_btn.pack(side="left")
        self._next_btn = tk.Button(nav, text="Next →", font=FONT_BODY,
                                   bg=ACCENT, fg="white", bd=0,
                                   padx=20, pady=10, cursor="hand2",
                                   activebackground=ACCENT_HOVER,
                                   command=self._next_q)
        self._next_btn.pack(side="right")

        # Answer map grid
        self._map_label = tk.Label(content, text="Question Map",
                                   font=FONT_BODY_B, bg=BG_DARK, fg=TEXT_SECONDARY)
        self._map_label.pack(anchor="w", pady=(PAD, 4))
        self._map_frame = tk.Frame(content, bg=BG_DARK)
        self._map_frame.pack(anchor="w")

    # ── Screen activation ─────────────────────────────────────────────────

    def on_show(self, **kwargs):
        self._q_index = 0
        self._selected = dict(self.app.user_answers)
        questions = self.app.quiz_data.get("questions", [])
        topic = self.app.quiz_data.get("topic", "Quiz")
        self._title_lbl.config(text=topic[:60])
        self._build_map(len(questions))
        self._render(self._q_index)
        self._canvas.yview_moveto(0)

    def _build_map(self, n):
        for w in self._map_frame.winfo_children():
            w.destroy()
        self._map_btns = []
        for i in range(n):
            b = tk.Button(self._map_frame, text=str(i+1),
                          font=FONT_SMALL, width=3, height=1,
                          bg=BORDER, fg=TEXT_SECONDARY, bd=0,
                          cursor="hand2",
                          command=lambda idx=i: self._jump(idx))
            b.grid(row=i // 10, column=i % 10, padx=2, pady=2)
            self._map_btns.append(b)

    # ── Render ────────────────────────────────────────────────────────────

    def _render(self, idx):
        questions = self.app.quiz_data.get("questions", [])
        n = len(questions)
        if not questions:
            return
        q = questions[idx]

        self._q_num_lbl.config(text=f"Question {idx+1} of {n}")
        self._prog_lbl.config(text=f"{idx+1} / {n}")
        self._q_text.config(text=q["question"])

        for key, btn in self._opt_buttons.items():
            text = f"  {key}.  {q['options'][key]}"
            btn.config(text=text, wraplength=700)
            if self._selected.get(idx) == key:
                btn.config(bg=OPTION_SEL, fg=ACCENT_HOVER)
            else:
                btn.config(bg=OPTION_BG, fg=TEXT_PRIMARY)

        # Prev/Next state
        self._prev_btn.config(state="normal" if idx > 0 else "disabled")
        is_last = (idx == n - 1)
        if is_last:
            self._next_btn.config(text="✅  Submit Quiz", bg=SUCCESS,
                                   activebackground="#16A34A")
        else:
            self._next_btn.config(text="Next →", bg=ACCENT,
                                   activebackground=ACCENT_HOVER)

        # Update progress bar
        pct = (idx + 1) / n
        self._prog_frame.update_idletasks()
        self._prog_bar.place(x=0, y=0, relheight=1.0,
                              width=self._prog_frame.winfo_width() * pct)

        # Update map
        for i, b in enumerate(self._map_btns):
            if i == idx:
                b.config(bg=ACCENT, fg="white")
            elif i in self._selected:
                b.config(bg=SUCCESS, fg="white")
            else:
                b.config(bg=BORDER, fg=TEXT_SECONDARY)

    # ── Interaction ───────────────────────────────────────────────────────

    def _select(self, key):
        self._selected[self._q_index] = key
        self._render(self._q_index)

    def _prev_q(self):
        if self._q_index > 0:
            self._q_index -= 1
            self._render(self._q_index)
            self._canvas.yview_moveto(0)

    def _next_q(self):
        n = len(self.app.quiz_data.get("questions", []))
        if self._q_index < n - 1:
            self._q_index += 1
            self._render(self._q_index)
            self._canvas.yview_moveto(0)
        else:
            self._submit()

    def _jump(self, idx):
        self._q_index = idx
        self._render(self._q_index)
        self._canvas.yview_moveto(0)

    def _submit(self):
        n = len(self.app.quiz_data.get("questions", []))
        unanswered = n - len(self._selected)
        if unanswered:
            ok = messagebox.askyesno(
                "Unanswered Questions",
                f"You have {unanswered} unanswered question(s). Submit anyway?"
            )
            if not ok:
                return
        self.app.user_answers = dict(self._selected)
        self.app.show_screen("results")

    def _back_home(self):
        if messagebox.askyesno("Go Home?",
                                "Going home will abandon your current quiz."):
            self.app.show_screen("home")
