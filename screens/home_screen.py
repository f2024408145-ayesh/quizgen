"""
Home Screen — Input text or PDF, choose settings, generate quiz.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

from utils.styles import *
from utils.pdf_reader import extract_text_from_pdf
from utils.quiz_generator import generate_quiz


class HomeScreen(tk.Frame):
    NAME = "home"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DARK)
        self.app = app
        self._build()

    # ── Build UI ──────────────────────────────────────────────────────────

    def _build(self):
        # ── Top bar ──
        topbar = tk.Frame(self, bg=BG_CARD, pady=12)
        topbar.pack(fill="x")
        tk.Label(topbar, text="⚡ QuizGen", font=("Segoe UI", 18, "bold"),
                 bg=BG_CARD, fg=ACCENT).pack(side="left", padx=PAD)
        tk.Button(topbar, text="📋 History", font=FONT_BODY,
                  bg=BG_CARD, fg=TEXT_SECONDARY, bd=0, activebackground=BORDER,
                  activeforeground=TEXT_PRIMARY, cursor="hand2",
                  command=lambda: self.app.show_screen("history")
                  ).pack(side="right", padx=PAD)

        # ── Main scroll area ──
        canvas = tk.Canvas(self, bg=BG_DARK, highlightthickness=0)
        scroll = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        inner = tk.Frame(canvas, bg=BG_DARK)
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _resize(e):
            canvas.itemconfig(win_id, width=e.width)
        canvas.bind("<Configure>", _resize)
        inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

        # Mouse-wheel scroll
        def _wheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _wheel)

        self._build_inner(inner)

    def _build_inner(self, parent):
        # Hero
        hero = tk.Frame(parent, bg=BG_DARK, pady=30)
        hero.pack(fill="x", padx=PAD*2)
        tk.Label(hero, text="Generate a Quiz in Seconds",
                 font=("Segoe UI", 26, "bold"), bg=BG_DARK, fg=TEXT_PRIMARY
                 ).pack()
        tk.Label(hero, text="Paste text, type your notes, or upload a PDF — Claude does the rest.",
                 font=FONT_BODY, bg=BG_DARK, fg=TEXT_SECONDARY).pack(pady=(4, 0))

        # ── Input card ──
        card = tk.Frame(parent, bg=BG_CARD, padx=PAD, pady=PAD)
        card.pack(fill="x", padx=PAD*2, pady=(0, PAD))

        # Source tabs
        self._source_var = tk.StringVar(value="text")
        tabs = tk.Frame(card, bg=BG_CARD)
        tabs.pack(fill="x", pady=(0, PAD_SM))
        for label, val in (("✏️  Paste / Type", "text"), ("📄  Upload PDF", "pdf")):
            b = tk.Button(tabs, text=label, font=FONT_BODY,
                          command=lambda v=val: self._switch_source(v),
                          bd=0, cursor="hand2", padx=12, pady=6)
            b.pack(side="left", padx=(0, 6))
            if val == "text":
                self._btn_text = b
            else:
                self._btn_pdf = b

        # Text area
        self._text_frame = tk.Frame(card, bg=BG_CARD)
        self._text_frame.pack(fill="both", expand=True)
        tk.Label(self._text_frame, text="Your text or notes:",
                 font=FONT_BODY_B, bg=BG_CARD, fg=TEXT_SECONDARY
                 ).pack(anchor="w")
        self._text_input = tk.Text(
            self._text_frame, height=12, wrap="word",
            bg=BG_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
            font=FONT_BODY, bd=1, relief="flat",
            highlightbackground=BORDER, highlightcolor=ACCENT, highlightthickness=1
        )
        self._text_input.pack(fill="both", expand=True, pady=(4, 0))
        self._placeholder = "Paste your article, notes, or any text here…"
        self._text_input.insert("1.0", self._placeholder)
        self._text_input.config(fg=TEXT_MUTED)
        self._text_input.bind("<FocusIn>", self._clear_placeholder)
        self._text_input.bind("<FocusOut>", self._restore_placeholder)

        # PDF frame (hidden by default)
        self._pdf_frame = tk.Frame(card, bg=BG_CARD)
        self._pdf_path = tk.StringVar(value="No file selected")
        pdf_row = tk.Frame(self._pdf_frame, bg=BG_CARD)
        pdf_row.pack(fill="x")
        tk.Button(pdf_row, text="Browse PDF…", font=FONT_BODY,
                  bg=ACCENT, fg="white", bd=0, padx=14, pady=8,
                  activebackground=ACCENT_HOVER, cursor="hand2",
                  command=self._browse_pdf).pack(side="left")
        tk.Label(pdf_row, textvariable=self._pdf_path,
                 font=FONT_BODY, bg=BG_CARD, fg=TEXT_SECONDARY
                 ).pack(side="left", padx=PAD_SM)

        self._switch_source("text")

        # ── Settings row ──
        settings = tk.Frame(parent, bg=BG_DARK, padx=PAD*2)
        settings.pack(fill="x", pady=(0, PAD))
        settings.columnconfigure(0, weight=1)
        settings.columnconfigure(1, weight=1)
        settings.columnconfigure(2, weight=1)

        # Num questions
        q_card = self._setting_card(settings, "Number of Questions")
        q_card.grid(row=0, column=0, padx=(0, PAD_SM), sticky="ew")
        self._num_q = tk.IntVar(value=10)
        num_frame = tk.Frame(q_card, bg=BG_CARD)
        num_frame.pack()
        tk.Button(num_frame, text="−", font=FONT_BODY_B, bg=BORDER,
                  fg=TEXT_PRIMARY, bd=0, padx=10, cursor="hand2",
                  activebackground=ACCENT,
                  command=lambda: self._num_q.set(max(3, self._num_q.get()-1))
                  ).pack(side="left")
        tk.Label(num_frame, textvariable=self._num_q,
                 font=FONT_SUBHEAD, bg=BG_CARD, fg=TEXT_PRIMARY, width=4
                 ).pack(side="left")
        tk.Button(num_frame, text="+", font=FONT_BODY_B, bg=BORDER,
                  fg=TEXT_PRIMARY, bd=0, padx=10, cursor="hand2",
                  activebackground=ACCENT,
                  command=lambda: self._num_q.set(min(20, self._num_q.get()+1))
                  ).pack(side="left")

        # Difficulty
        d_card = self._setting_card(settings, "Difficulty")
        d_card.grid(row=0, column=1, padx=PAD_SM//2, sticky="ew")
        self._difficulty = tk.StringVar(value="medium")
        diff_frame = tk.Frame(d_card, bg=BG_CARD)
        diff_frame.pack()
        for label, val in (("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")):
            b = tk.Button(diff_frame, text=label, font=FONT_SMALL,
                          bg=BORDER, fg=TEXT_SECONDARY, bd=0, padx=10, pady=4,
                          cursor="hand2",
                          command=lambda v=val: self._set_diff(v))
            b.pack(side="left", padx=2)
            if val == "medium":
                b.config(bg=ACCENT, fg="white")
                self._diff_buttons = {val: b}
            else:
                if not hasattr(self, "_diff_buttons"):
                    self._diff_buttons = {}
                self._diff_buttons[val] = b

        # Topic label
        t_card = self._setting_card(settings, "Topic Label (optional)")
        t_card.grid(row=0, column=2, padx=(PAD_SM, 0), sticky="ew")
        self._topic_label = tk.Entry(t_card, font=FONT_BODY,
                                     bg=BG_INPUT, fg=TEXT_PRIMARY,
                                     insertbackground=TEXT_PRIMARY,
                                     bd=0, highlightthickness=1,
                                     highlightbackground=BORDER,
                                     highlightcolor=ACCENT)
        self._topic_label.pack(fill="x", ipady=6)

        # ── Generate button ──
        btn_frame = tk.Frame(parent, bg=BG_DARK)
        btn_frame.pack(pady=(0, PAD*2))
        self._gen_btn = tk.Button(
            btn_frame, text="⚡  Generate Quiz",
            font=("Segoe UI", 13, "bold"),
            bg=ACCENT, fg="white", bd=0,
            padx=40, pady=14, cursor="hand2",
            activebackground=ACCENT_HOVER, activeforeground="white",
            command=self._start_generate
        )
        self._gen_btn.pack()

        # Status label
        self._status = tk.StringVar(value="")
        self._status_lbl = tk.Label(btn_frame, textvariable=self._status,
                                    font=FONT_BODY, bg=BG_DARK, fg=TEXT_SECONDARY)
        self._status_lbl.pack(pady=(PAD_SM, 0))

    # ── Helpers ───────────────────────────────────────────────────────────

    def _setting_card(self, parent, title):
        card = tk.Frame(parent, bg=BG_CARD, padx=PAD, pady=PAD)
        tk.Label(card, text=title, font=FONT_SMALL, bg=BG_CARD,
                 fg=TEXT_MUTED).pack(pady=(0, 8))
        return card

    def _switch_source(self, val):
        self._source_var.set(val)
        if val == "text":
            self._pdf_frame.pack_forget()
            self._text_frame.pack(fill="both", expand=True)
            self._btn_text.config(bg=ACCENT, fg="white")
            self._btn_pdf.config(bg=BORDER, fg=TEXT_SECONDARY)
        else:
            self._text_frame.pack_forget()
            self._pdf_frame.pack(fill="both", expand=True)
            self._btn_text.config(bg=BORDER, fg=TEXT_SECONDARY)
            self._btn_pdf.config(bg=ACCENT, fg="white")

    def _browse_pdf(self):
        path = filedialog.askopenfilename(
            title="Select PDF", filetypes=[("PDF Files", "*.pdf")]
        )
        if path:
            self._pdf_path.set(path)

    def _clear_placeholder(self, _event=None):
        if self._text_input.get("1.0", "end-1c") == self._placeholder:
            self._text_input.delete("1.0", "end")
            self._text_input.config(fg=TEXT_PRIMARY)

    def _restore_placeholder(self, _event=None):
        if not self._text_input.get("1.0", "end-1c").strip():
            self._text_input.insert("1.0", self._placeholder)
            self._text_input.config(fg=TEXT_MUTED)

    def _set_diff(self, val):
        self._difficulty.set(val)
        for k, btn in self._diff_buttons.items():
            if k == val:
                btn.config(bg=ACCENT, fg="white")
            else:
                btn.config(bg=BORDER, fg=TEXT_SECONDARY)

    # ── Generate flow ─────────────────────────────────────────────────────

    def _start_generate(self):
        source = self._source_var.get()
        if source == "text":
            text = self._text_input.get("1.0", "end-1c").strip()
            if not text or text == self._placeholder:
                messagebox.showwarning("No Input", "Please enter some text first.")
                return
        else:
            path = self._pdf_path.get()
            if path == "No file selected" or not path:
                messagebox.showwarning("No PDF", "Please select a PDF file first.")
                return
            self._status.set("Extracting PDF text…")
            self.update()
            try:
                text = extract_text_from_pdf(path)
            except Exception as e:
                messagebox.showerror("PDF Error", str(e))
                self._status.set("")
                return

        if len(text.split()) < 50:
            messagebox.showwarning("Too Short",
                                   "Please provide at least 50 words of text.")
            return

        topic = self._topic_label.get().strip() or text[:60].replace("\n", " ") + "…"
        n = self._num_q.get()
        diff = self._difficulty.get()

        self._gen_btn.config(state="disabled", text="Generating…")
        self._status.set("Generating your quiz…")
        self.update()

        self.app.topic_text = text

        def _worker():
            try:
                questions = generate_quiz(text, n, diff)
                self.after(0, lambda q=questions, t=topic: self._on_done(q, t))
            except Exception as ex:
                msg = str(ex)
                self.after(0, lambda m=msg: self._on_error(m))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_done(self, questions, topic):
        self._gen_btn.config(state="normal", text="⚡  Generate Quiz")
        self._status.set("")
        if not questions:
            messagebox.showerror("Error", "No questions were generated. Try more text.")
            return
        self.app.quiz_data = {"topic": topic, "questions": questions}
        self.app.user_answers = {}
        self.app.show_screen("quiz")

    def _on_error(self, msg):
        self._gen_btn.config(state="normal", text="⚡  Generate Quiz")
        self._status.set("")
        messagebox.showerror("Generation Failed", f"Could not generate quiz:\n\n{msg}")

    def on_show(self, **kwargs):
        pass
